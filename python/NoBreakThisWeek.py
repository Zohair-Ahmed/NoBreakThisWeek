from cgitb import html, text
from turtle import st
from bs4 import BeautifulSoup
import requests

opTitle = "One Piece"
baseUrl = "https://onepiecechapters.com/"

# get status specific information
getStatusUrl = baseUrl + "projects"

statusRequest = requests.get(getStatusUrl)
htmlStatusDoc = BeautifulSoup(statusRequest.text, "html.parser")

if statusRequest.status_code != 200:
    quit()

opStatusCard = htmlStatusDoc.find_all(text="One Piece")[0].parent.parent
opTitle = opStatusCard.find("a").text
opNextChProgress = opStatusCard.find(text="Next Chapter Progress")
opStatus = opStatusCard.find(class_="w-full text-center text-white px-2 rounded-full").text

# get chapter specific information
getChapterUrl = baseUrl + "mangas/5/one-piece"

chapterRequest = requests.get(getChapterUrl)
htmlChapterDoc = BeautifulSoup(chapterRequest.text, "html.parser")

if chapterRequest.status_code != 200:
    quit()

opChapterCard = htmlChapterDoc.find(class_="col-span-2")
opLatestCh = opChapterCard.find("a")
opLatestTitle = opLatestCh.text
opLatestChLink = opLatestCh['href']

# notification
print(opLatestTitle + "\n" + opLatestChLink + "\n\n")
print(opNextChProgress + ": " + opStatus + "\n")