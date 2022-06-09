from email import message
from lib2to3.pgen2.token import OP
from multiprocessing import connection
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
import requests
from twilio.rest import Client

load_dotenv(find_dotenv())

# basic One Piece info
opTitle = "One Piece"
baseUrl = os.environ.get('BASE_URL')

# MongoDB info
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
CLUSTER_NAME = os.environ.get('CLUSTER_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
connection_string = f"mongodb+srv://nobreakthisweek:{MONGODB_PASSWORD}@nobreakthisweek.dapsuc9.mongodb.net/?retryWrites=true&w=majority"
mongoClient = MongoClient(connection_string)
db = mongoClient[CLUSTER_NAME]
collection = db[COLLECTION_NAME]
collectionID = 0

# twilio info
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
MY_PHONE_NUMBER = os.environ.get('MY_PHONE_NUMBER')
MESSAGING_SERVICE_SID = os.environ.get('MESSAGING_SERVICE_SID')
twilioClient = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def getChapterStatus(opStatusCard):
    """Get the status of the next chapter"""
    return opStatusCard.find(class_="w-full text-center text-white px-2 rounded-full").text


def getLatestChapterTitle(opLatestCh):
    """Get the title of the latest chapter"""
    return opLatestCh.find(class_="text-gray-500").text


def getLatestChapterNumber(opLatestCh):
    """Get the latest chapter number"""
    return opLatestCh.find(class_="text-lg font-bold").text


def getLatestChapterLink(opLatestCh):
    """Get the endpoint URL of the latest chapter"""
    return baseUrl + opLatestCh['href']


def postOPInfo(opStatus, opLatestNumber, opLatestTitle, opLatestChLink):
    """Getting the data collected to parse to JSON, which is sent to MongoDB"""
    webData = {
        "_id": collectionID,
        "chapter-num": opLatestNumber,
        "title": opLatestTitle,
        "status": opStatus,
        "link": opLatestChLink
    }

    return webData


def getOPInfo():
    """Return the current data stored for the One Piece chapter"""
    getInfo = collection.find_one({"_id": collectionID})
    return getInfo


def updateOPInfo_translating(opStatus):
    """Update the One Piece info to now say the a chapter is being translated"""
    statusUpdate = {"$set": {"status": opStatus}}
    collection.update_one({"_id": collectionID}, statusUpdate)


def updateOPInfo_released(opLatestNumber, opLatestTitle, opStatus, opLatestChLink):
    """Update the chapter number, title, and link to match just release chapter"""
    replaceInfo = {
        "chapter-num": opLatestNumber,
        "title": opLatestTitle,
        "status": opStatus,
        "link": opLatestChLink
    }

    collection.replace_one({"_id": collectionID}, replaceInfo)


def sendTwilioMessage(messageBody):
    twilioClient.messages.create(
        body=messageBody,
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER,
        messaging_service_sid=MESSAGING_SERVICE_SID
    )


# get status specific information
getStatusUrl = baseUrl + "/projects"
statusRequest = requests.get(getStatusUrl)
htmlStatusDoc = BeautifulSoup(statusRequest.text, "html.parser")
web_opStatusCard = htmlStatusDoc.find_all(text="One Piece")[0].parent.parent

# get chapter specific information
getChapterUrl = baseUrl + "/mangas/5/one-piece"
chapterRequest = requests.get(getChapterUrl)
htmlChapterDoc = BeautifulSoup(chapterRequest.text, "html.parser")
web_opLatestCh = htmlChapterDoc.find(class_="col-span-2").find("a")

# quit program if website is not reached
if statusRequest.status_code != 200 or chapterRequest.status_code != 200:
    quit()

# organize web scraped chapter specific info to variables
web_opStatus = getChapterStatus(web_opStatusCard)
web_opLatestNumber = getLatestChapterNumber(web_opLatestCh)
web_opLatestTitle = getLatestChapterTitle(web_opLatestCh)
web_opLatestChLink = getLatestChapterLink(web_opLatestCh)

# organize database scraped chapter specific info to variables
db_latestOpInfo = getOPInfo()
db_opStatus = db_latestOpInfo["status"]
db_opLatestNumber = db_latestOpInfo["chapter-num"]
db_opLatestTitle = db_latestOpInfo["title"]
db_opLatestChLink = db_latestOpInfo["link"]

# there has been a status update
if web_opStatus != db_opStatus:
    # if there are been no update to chapter number, it is translating, else the chapter has been released
    if web_opLatestNumber == db_opLatestNumber:
        updateOPInfo_translating(web_opStatus)
        sendTwilioMessage("The next chapter is now being translated!")
    else:
        sendTwilioMessage("NEW ONE PIECE CHAPTER!!")
        updateOPInfo_released(
            web_opLatestNumber, web_opLatestTitle, web_opStatus, web_opLatestChLink)
else:
    sendTwilioMessage("NoBreakThisWeek: No new chapter yet... but soon")
    quit()
