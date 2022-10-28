# FandomVideoGenerator created by TheHudek

## About

This tool generates 1080 x 1920 videos based on any fandom page with alternating images and voiceover. Being my first GitHub project, this is a highly alpha version, but feel free to report any bugs that you may have found. Please mention my name under the videos you generate using this tool. Tested in Python 3.10.4.

[![LICENSE](https://img.shields.io/badge/License-Apache_2.0-green)](https://github.com/TheHudek/FandomVideoGenerator/blob/master/LICENSE.md)
[![Language](https://img.shields.io/badge/Language-Python3-blue.svg)](https://www.python.org/)

## Installation

- Have Python 3 installed
- Clone this repository
- Run `pip3 install -r requirements.txt`

## Usage

- Rename `.env.template` to `.env`
- Change the texts in `.env`. `PROMPT`and `WIKI` should be copied from the fandom URL. `LENGTH` is the maximum length of the video in seconds. The actual length of the video depends on the number of images chosen and will likely be much shorter. `BACKGROUND_LINK` and `AUDIO_LINK` are YouTube links used for the ambience of the video. These files will only be downloaded when you change them. `INTRO` is the first sentence that will be read in the beginning of the video. Please don't make this too short as the speech-to-text API might crash. Example settings for https://gameofthrones.fandom.com/wiki/Daenerys_Targaryen:

```.env
PROMPT="Daenerys_Targaryen"
WIKI="gameofthrones"
LENGHT="60"
BACKGROUND_LINK="https://www.youtube.com/watch?v=Jqf9haCd6mM"
AUDIO_LINK="https://www.youtube.com/watch?v=EGcXF0iG-2s"
INTRO="Game Of Thrones Characters Part 1 - Daenerys Targaryen"
```

- Run `python3 main.py`
- After the images are downloaded, you should see a window pop up. Based on the file names, select the images that you would like to use in the video. Separate them with commas.
- A number of sentences will be printed. Mainly from the beginning of the list, please select the sentences that should not be included in the video. These tend to be quotes from the characters or ads.
- Voilà

## Examples

- [Game of Thrones - Daenerys Targaryen](https://vm.tiktok.com/ZMFBv9P87/)
- [Game of Thrones - Jon Snow](https://vm.tiktok.com/ZMFBvqS1o/)
