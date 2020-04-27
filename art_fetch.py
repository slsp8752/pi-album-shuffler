#!/usr/bin/env python3

from mutagen import File
from mutagen.id3 import ID3
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import time
import ST7789
import os

base_path = "/home/pi/radio_star/"

def get_art(song):
    images = []
    dir = os.path.dirname(song)
    filelist = os.listdir(dir)
    for file in filelist:
        lowercase = file.lower()
        if(lowercase.endswith(".png") or lowercase.endswith(".jpg") or lowercase.endswith(".jpeg")):
            print(dir + "/" + file)
            images.append(dir + "/" + file)
    image = Image.open(images[0])
    scaled = image.resize((240,240))
    mode = scaled.convert('RGBA')
    return mode


def get_song():
    with open('/home/pi/radio_star/np_path.txt') as song:
        mp3_path = song.readline()
    return mp3_path

def diff_check(song_string, path, art):
    new_song = get_song()
    if(new_song == path):
        print("SAME")
        return song_string, path, art 

    ID = ID3(new_song)
    new_song_string = "  " + ID["TIT2"].text[0] + ' - ' + ID["TPE1"].text[0] + "  "
    new_path = new_song

    new_dir = os.path.dirname(new_song)
    old_dir = os.path.dirname(path)
    if(new_dir != old_dir):
        new_art = get_art(new_song)
        print("NEW ALBUM, NEW SONG")
        return new_song_string, new_path, new_art

    else:
        print("SAME ALBUM, NEW SONG")
        return new_song_string, new_path, art
    

FILE = get_song()
ART = get_art(FILE)
ID = ID3(FILE)
MESSAGE = "  " + ID["TIT2"].text[0] + ' - ' + ID["TPE1"].text[0] + "  "

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=1,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=13,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 30)
draw = ImageDraw.Draw(ART)
size_x, size_y = draw.textsize(MESSAGE, fnt)
text_x = disp.width
text_y = (40 - size_y) // 2
t_start = time.time()

prev_icon = Image.open(base_path + "images/prev/2x/prev2x.png")
next_icon = Image.open(base_path + "images/next/2x/next2x.png")
shuffle_icon = Image.open(base_path + "images/shuffle/2x/shuffle2x.png")
album_icon = Image.open(base_path + "images/album/2x/album2x.png")

while True:
    MESSAGE, FILE, ART = diff_check(MESSAGE, FILE, ART)
    print("Message: " + MESSAGE)
    print("File: " + FILE)
    txt = Image.new('RGBA', (240,240), (255,255,255,0))
    x = (time.time() - t_start) * 100
    x %= (size_x + disp.width)
    draw = ImageDraw.Draw(txt)
    # title box
    draw.rectangle((0,0,240,40),(0,0,0,180))
    # prev button
    draw.rectangle((0,45,40,85),(0,0,0,180))
    # next button
    draw.rectangle((200,45,240,85),(0,0,0,180))
    # shuffle button
    draw.rectangle((0,162,40,202),(0,0,0,180))
    # album button
    draw.rectangle((200,162,240,202),(0,0,0,180))
    draw.text((0, text_y), MESSAGE, font=fnt, fill=(255, 255, 255))
    out = Image.alpha_composite(ART, txt)
    out.paste(prev_icon, (0,48), prev_icon) 
    out.paste(next_icon, (204,48), next_icon) 
    out.paste(shuffle_icon, (0,165), shuffle_icon) 
    out.paste(album_icon, (204,165), album_icon) 
    disp.display(out)
    MESSAGE = MESSAGE[1:] + MESSAGE[0]
