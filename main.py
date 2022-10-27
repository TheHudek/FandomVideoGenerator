# FandomVideoGenerator created by TheHudek

from dotenv import load_dotenv

from voices import text_to_mp3
from background import chop_background_video, download_background
from finalvideo import final_video

load_dotenv()
n, length, number_of_comments, final_images = text_to_mp3()
download_background()
chop_background_video(length)
final_video = final_video(number_of_comments, final_images)
