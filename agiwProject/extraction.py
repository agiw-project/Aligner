import json
import page
from selenium import webdriver


def extract(fileName):
    urls = []
    # leggo dal file di urls
    f = open(fileName, "r")
    for line in f:
        urls.append(line)
    f.close()

    pages = []
    ffprofile = webdriver.FirefoxProfile()
    ffprofile.add_extension(page.ADBLOCK_PATH)
    ffprofile.set_preference("extensions.adblockplus.currentVersion", "3.10")
    firefox = webdriver.Firefox(firefox_profile=ffprofile, executable_path=page.GECKO_PATH)
    for url in urls:
        p = page.Page(url)
        p.leaves = p.extract3(firefox)
        pages.append(p)

    newFileName = fileName.replace('.txt', '').replace('Url/', '')

    json_string = json.dumps([p.__dict__ for p in pages])
    with open("Json/pages_new_" + newFileName + ".json", "a") as file:
        file.write(json_string)
        file.close()
