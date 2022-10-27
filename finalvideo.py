from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeVideoClip,
    CompositeAudioClip,
    AudioClip
)
from moviepy.audio.fx.volumex import volumex
import io
from PIL import Image, ImageDraw, ImageFont
import requests
import os
from dotenv import load_dotenv
import math
from background import get_start_and_end_times

W, H = 1080, 1920


def final_video(number_of_clips, final_images):
    load_dotenv()
    length: int = 0
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)
    background_clip = (VideoFileClip("clip.mp4").without_audio().resize(
        height=H).crop(x1=1166.6, y1=0, x2=2246.6, y2=1920))
    audio_clips = []
    silence = AudioClip(make_frame=lambda t: 0, duration=0.5, fps=30)
    for i in range(0, number_of_clips):
        audio_clips.append(AudioFileClip(f"mp3/{i}.mp3"))
        length = length + AudioFileClip(f"mp3/{i}.mp3").duration
        audio_clips.append(silence)
        length = length + silence.duration
    audio_concat = concatenate_audioclips(audio_clips)
    audio = AudioFileClip("audio.mp3")
    start_time, end_time = get_start_and_end_times(
        length, audio.duration)
    audio = audio.subclip(start_time, end_time)
    audio = volumex(audio, 0.2)
    audio = CompositeAudioClip([audio, audio_concat])
    audio.write_audiofile("clip_audio.mp3", 44100, )
    audio.close

    image_clips = []
    print(f"Appending title.png")

    firstimg = Image.open(f"png/{final_images[0]}.jpg")
    nsize: list = list(firstimg.size)
    nsize[1] = int(nsize[1]*1.2)
    width, height = tuple(nsize)
    nsize = math.prod((width, height))
    img = Image.new("RGBA", (width, height), color="white")
    font_url = "https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true"
    with requests.get(font_url, allow_redirects=True) as r:
        subtitle_font = ImageFont.truetype(
            io.BytesIO(r.content), size=int(width/len((os.getenv("PROMPT")).replace("_", " "))))
    img.putalpha(0)
    img.paste(firstimg, (0, int(height-height/1.2)))
    draw = ImageDraw.Draw(img)
    title = (os.getenv("PROMPT")).replace("_", " ")
    _, _, w, h = draw.textbbox((0, 0), title, font=subtitle_font)
    draw.text(((width-w)/2, ((height/2)-((height/2)/1.2))), title, font=subtitle_font,
              stroke_width=2, fill="white", stroke_fill="black")
    img.save("png/title.png")
    img.close()
    firstimg.close()
    image_clips.append(
        ImageClip(f"png/title.png")
        .set_duration(audio_clips[0].duration+0.5)
        .set_position("center")
        .resize(width=W - 75)
    )
    del final_images[0]
    print(final_images)
    k: int = 2
    for i in range(0, number_of_clips-1):
        if os.path.exists(f"png/{final_images[i]}.jpg") and not os.path.exists(f"png/{final_images[i]}.png"):
            im = Image.open(f"png/{final_images[i]}.jpg")
            im.save(f"png/{final_images[i]}.png")
            image_clips.append(
                ImageClip(f"png/{final_images[i]}.png")
                .set_duration(audio_clips[k].duration+audio_clips[k+1].duration)
                .set_position("center")
                .resize(width=W - 75)
            )
            im.close()
        print(
            f"Appending Image {final_images[i]} with lenght {audio_clips[k].duration} and {audio_clips[k+1].duration}")
        k += 2
    image_concat = concatenate_videoclips(
        image_clips, method="compose").set_position(("center", "center"))
    image_concat.audio = AudioFileClip("clip_audio.mp3")
    final = CompositeVideoClip(
        [background_clip, image_concat])
    final.write_videofile("final.mp4", fps=30, ffmpeg_params=[
                          "-vcodec", "h264_nvenc"], audio_codec="aac", audio_bitrate="192k")
    final.close()
