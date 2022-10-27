from pathlib import Path
from fanobject import get_fanobject, get_pictures
import requests
from mutagen.mp3 import MP3
import os
from dotenv import load_dotenv


def text_to_mp3():
    print("Welcome to TheHudek's FandomVideoGenerator")
    length = 0

    load_dotenv()

    if not os.path.exists("png"):
        os.makedirs("png")
    if not os.path.exists("mp3"):
        os.makedirs("mp3")

    n, final_images = get_pictures()
    fanobject_object = get_fanobject()
    for i in range(len(fanobject_object['body'])):
        if n-1 < i+1 or length > int(os.getenv("LENGHT")):
            break
        else:
            print(
                f"Printing {i}/{range(len(fanobject_object['body']))}, which is {fanobject_object['body'][i]}")
            Path("mp3").mkdir(parents=True, exist_ok=True)
            url = 'https://streamlabs.com/polly/speak'
            body = {'voice': 'Matthew', 'text': fanobject_object["body"][i]}
            response = requests.post(url, data=body)
            voice_data = requests.get(response.json()['speak_url'])
            f = open("mp3/{}.mp3".format(i), "wb")
            f.write(voice_data.content)
            if length <= int(os.getenv("LENGHT")):
                length += MP3("mp3/{}.mp3".format(i)).info.length
            f.close()
    length = length + i*0.5

    n -= 1

    print("Pictures: ", n, ", Length: ", length, ", Prompts: ", i)

    return n, length, i, final_images
