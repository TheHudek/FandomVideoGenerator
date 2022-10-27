from cmd import PROMPT
import fandom
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import webbrowser


def get_fanobject():
    load_dotenv()
    content = {}
    fandom.set_wiki(os.getenv("WIKI"))
    fanobject_chosen = fandom.page(title=os.getenv("PROMPT"))
    fanobject_body = fanobject_chosen.plain_text
    fanobject_body_split = fanobject_body.split("\n")
    del fanobject_body_split[0]
    if len(fanobject_body_split) < 40:
        j = fanobject_body_split
    else:
        j = fanobject_body_split[:40]
    for i in range(len(j)):
        print(f"{i}: {fanobject_body_split[i]}")
    unnecesary = input(
        "Please provide the number of the unnecesary lines in the beginning: ")
    if not unnecesary == "":
        unnecesary = unnecesary.split(",")
        unnecesary = [int(x) for x in unnecesary]
        for i in range(len(unnecesary)):
            del j[int(unnecesary[i])]
            unnecesary = [x-1 for x in unnecesary]
    j = " ".join(j)
    j = j.split('. ')
    del j[len(j)-1]

    if not os.getenv("INTRO") == "":
        j.insert(0, os.getenv("INTRO"))
    for i in range(len(j)):
        print(f"{i}: {j[i]}")

    try:

        content["body"] = j
        content["elements"] = len(j)

    except AttributeError as e:

        pass

    return content


def get_pictures():
    load_dotenv()
    fandom.set_wiki(os.getenv("WIKI"))
    fanobject_chosen = fandom.page(title=os.getenv("PROMPT"))

    html_page = fanobject_chosen.html
    images = []
    soup = BeautifulSoup(html_page, 'html.parser')
    warning = soup.find("div", class_="mw-parser-output")
    if len(warning.findAll("img")) < 40:
        j = warning.findAll("img")
    else:
        j = warning.findAll("img")[:40]
    for links in j:
        link = links.get("src")
        if type(link) is str and not link.startswith("data"):
            v: int = link.find("revision")
            link = link[0:v]
            try:
                images.index(link)
                continue
            except ValueError:
                images.append(link)
                print(link)
    for links in j:
        link = links.get("data-src")
        if type(link) is str and not link.startswith("data"):
            v: int = link.find("revision")
            link = link[0:v]
            try:
                images.index(link)
                continue
            except ValueError:
                images.append(link)
                print(link)
    dir = "png/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    n = 0
    for imgs in range(len(images)):
        if images[imgs]:
            response = requests.get(images[imgs])
            if response.status_code:
                fp = open(f"png/{n}.jpg", "wb")
                fp.write(response.content)
                fp.close()
                n += 1

    path = "png"
    path = os.path.realpath(path)
    webbrowser.open(path)
    chosen_pictures = input(
        f"From the newly opened window, please choose the pictures you would like to use in the video and write them here in order, comma separated (e.g.: 0,3,4,6): ")
    chosen_pictures = chosen_pictures.split(",")
    final_images = []
    for i in range(len(chosen_pictures)):
        final_images.append(images[int(chosen_pictures[i])])
    n = len(chosen_pictures)
    return n, chosen_pictures
