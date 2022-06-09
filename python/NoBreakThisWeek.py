from multiprocessing import connection
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
import requests

load_dotenv(find_dotenv())

opTitle = "One Piece"
baseUrl = "https://onepiecechapters.com"

MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
CLUSTER_NAME = os.environ.get('CLUSTER_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
connection_string = f"mongodb+srv://nobreakthisweek:{MONGODB_PASSWORD}@nobreakthisweek.dapsuc9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client[CLUSTER_NAME]
collection = db[COLLECTION_NAME]


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


def dataToJSON(opStatus, opLatestNumber, opLatestTitle, opLatestChLink):
    """Getting the data collected to parse to JSON, which is sent to MongoDB"""
    webData = {
        "_id" : 0,
        "chapter-num" : opLatestNumber,
        "title" : opLatestTitle,
        "status" : opStatus,
        "link" : opLatestChLink
    }

    return webData


# get status specific information
getStatusUrl = baseUrl + "/projects"
statusRequest = requests.get(getStatusUrl)
htmlStatusDoc = BeautifulSoup(statusRequest.text, "html.parser")
opStatusCard = htmlStatusDoc.find_all(text="One Piece")[0].parent.parent

# get chapter specific information
getChapterUrl = baseUrl + "/mangas/5/one-piece"
chapterRequest = requests.get(getChapterUrl)
htmlChapterDoc = BeautifulSoup(chapterRequest.text, "html.parser")
opLatestCh = htmlChapterDoc.find(class_="col-span-2").find("a")

# quit program if website is not reached
if statusRequest.status_code != 200 or chapterRequest.status_code != 200:
    quit()

# organize chapter specific info to variables
opStatus = getChapterStatus(opStatusCard)
opLatestNumber = getLatestChapterNumber(opLatestCh)
opLatestTitle = getLatestChapterTitle(opLatestCh)
opLatestChLink = getLatestChapterLink(opLatestCh)

# insert to database
onePieceData = dataToJSON(opStatus, opLatestNumber, opLatestTitle, opLatestChLink)
collection.insert_one(onePieceData)
