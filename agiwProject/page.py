import requests
import lxml.html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

GECKO_PATH = "./geckodriver"
ADBLOCK_PATH = "./adblock_plus-3.10-an fx.xpi"


class Page:
    def __init__(self, url):
        self.url = url
        self.leaves = None

    def extract(self):
        html = requests.get(self.url)
        doc = lxml.html.fromstring(html.content)
        all_leaves = doc.xpath(
            "//body//*[text()[not(normalize-space()='')]][not(self::script or self::style or self::meta or "
            "self::noscript)]/text()")
        return all_leaves

    def extract2(self):
        html = requests.get(self.url)
        doc = lxml.html.fromstring(html.content)
        all_leaves = doc.xpath("//*[not(child::*)]/text()")
        return all_leaves

    # rotoworld extract
    def extract3(self, firefox):
        firefox.get(self.url)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        leaves = WebDriverWait(firefox, 20, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[not(child::*)]")))
        allLeaves = []
        for leaf in leaves:
            try:
                if str(leaf.text) != "":
                    allLeaves.append(leaf.text)

            except StaleElementReferenceException:
                print("ECCEZIONE")

        return allLeaves
