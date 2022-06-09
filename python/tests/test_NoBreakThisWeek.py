from unittest import mock
from bs4 import BeautifulSoup
import unittest
import sys
sys.path.append('../')

from NoBreakThisWeek import getChapterStatus, getLatestChapterTitle, getLatestChapterNumber, getLatestChapterLink

class TestNoBreakThisWeek(unittest.TestCase):
    """Unit testing for NoBreakThisWeek.py"""

    def test_getChapterStatus(self):
        """Asserts equal if the status of the HTML div is \"Waiting For Next Chapter\""""
        with open("./utils/mock_opStatusCard.html", "r") as f:
            mockStatusCard = BeautifulSoup(f, "html.parser")
        self.assertEqual(getChapterStatus(mockStatusCard).strip(" \t\n"), "Waiting For Next Chapter")

        
    def test_getLatestChapterTitle(self):
        """Asserts equal if the title of the chapter is \"The Shogun of Wano - Kozuki Momonosuke\""""
        with open("./utils/mock_opLatestCh.html", "r") as f:
            mockLatestCh = BeautifulSoup(f, "html.parser")
        self.assertEqual(getLatestChapterTitle(mockLatestCh.find("a")).strip(" \t\n"), "The Shogun of Wano - Kozuki Momonosuke")


    def test_getLatestChapterNumber(self):
        """Asserts equal if the chapter number is \"One Piece Chapter 1051\""""
        with open("./utils/mock_opLatestCh.html", "r") as f:
            mockLatestCh = BeautifulSoup(f, "html.parser")
        self.assertEqual(getLatestChapterNumber(mockLatestCh.find("a")).strip(" \t\n"), "One Piece Chapter 1051")


    def test_getLatestChapterLink(self):
        """Asserts equal if the link for the chapter is \"/chapters/2301/one-piece-chapter-1051\""""
        with open("./utils/mock_opLatestCh.html", "r") as f:
            mockLatestCh = BeautifulSoup(f, "html.parser")
        self.assertEqual(getLatestChapterLink(mockLatestCh.find("a")), "https://onepiecechapters.com/chapters/2301/one-piece-chapter-1051/chapters/2301/one-piece-chapter-1051")

if __name__ == '__main__':
    unittest.main()