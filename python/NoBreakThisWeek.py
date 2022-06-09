from bs4 import BeautifulSoup
import requests

opTitle = "One Piece"
baseUrl = "https://onepiecechapters.com/"


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
    return opLatestCh['href']

# get status specific information
getStatusUrl = baseUrl + "projects"
statusRequest = requests.get(getStatusUrl)
htmlStatusDoc = BeautifulSoup(statusRequest.text, "html.parser")
opStatusCard = htmlStatusDoc.find_all(text="One Piece")[0].parent.parent

# get chapter specific information
getChapterUrl = baseUrl + "mangas/5/one-piece"
chapterRequest = requests.get(getChapterUrl)
htmlChapterDoc = BeautifulSoup(chapterRequest.text, "html.parser")
opLatestCh = htmlChapterDoc.find(class_="col-span-2").find("a")


if statusRequest.status_code != 200 or chapterRequest.status_code != 200:
    quit()

opStatus = getChapterStatus(opStatusCard)
opLatestNumber = getLatestChapterNumber(opLatestCh)
opLatestTitle = getLatestChapterTitle(opLatestCh)
opLatestChLink = getLatestChapterLink(opLatestCh)

# notification
print(opLatestNumber + ": " + opLatestTitle + "\n" + opLatestChLink + "\n\n")
print("Next Chapter Progress: " + opStatus + "\n")
