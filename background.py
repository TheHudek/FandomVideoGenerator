from random import randrange
from pathlib import Path
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
from dotenv import load_dotenv
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def get_start_and_end_times(video_lenght, lenght_of_clip):
    random_time = randrange(0, int(lenght_of_clip) - int(video_lenght))
    return random_time, random_time + video_lenght


def download_background():
    load_dotenv()
    if not os.path.exists("background.txt"):
        f = open("background.txt", "x")
        f.close()
    if not os.path.exists("audio.txt"):
        f = open("audio.txt", "x")
        f.close()
    with open("background.txt", "r+") as f:
        if not os.getenv("BACKGROUND_LINK") in f.read() or not Path("background.mp4").is_file():
            YouTube(os.getenv("BACKGROUND_LINK")).streams.filter(
                res="720p").first().download(filename="background.mp4")
            f.seek(0)
            f.truncate()
            f.write(os.getenv("BACKGROUND_LINK"))
            f.close()
    with open("audio.txt", "r+") as f:
        if not os.getenv("AUDIO_LINK") in f.read() or not Path("audio.mp3").is_file():
            YouTube(os.getenv("AUDIO_LINK")).streams.filter(
                only_audio=True).first().download(filename="audio.mp3")
            f.seek(0)
            f.truncate()
            f.write(os.getenv("AUDIO_LINK"))
            f.close()


def chop_background_video(video_lenght):
    background = VideoFileClip("background.mp4")
    start_time, end_time = get_start_and_end_times(
        video_lenght, background.duration)
    ffmpeg_extract_subclip("background.mp4", start_time, end_time, "clip.mp4")
    background.close()
