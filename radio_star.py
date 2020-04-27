#!/usr/bin/env python3

# TODO:
# power off bug

from os import listdir, system, fsync
from os.path import isfile, join, isdir
from random import shuffle
import threading
import subprocess
import re
from pipes import quote

# sort songs in numerical order using Jeff Atwood's "Sorting for Humans" sorter
# https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
def sorted_nicely( l ): 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


pathname = "/media/RADIO_STAR"

artist_paths = []
album_paths = []
song_paths = []
album_index = 0
song_index = 0
timestamp = 0

def updateTimestamp():
    global timestamp
    threading.Timer(10.0, updateTimestamp).start()
    with open("/home/pi/radio_star/now_playing.txt", "w+") as np_file:
        np_file.write(str(album_index)+'\n')
        np_file.write(str(song_index)+'\n')
        np_file.write(str(timestamp)+'\n')
        np_file.flush()
        fsync(np_file.fileno())

    print ("Writing timestamp to nowplaying.txt")
    timestamp += 1


if(isfile("/home/pi/radio_star/albums.txt")):
    # read in the existing album order
    with open("/home/pi/radio_star/albums.txt", "r") as album_file:
        album_paths = [line.rstrip('\n') for line in album_file]

    # if there was already an album playing, get the now playing info
    if(isfile("/home/pi/radio_star/now_playing.txt")):
        print("Already playing an album")
        with open("/home/pi/radio_star/now_playing.txt", "r") as np_file:
            for i, line in enumerate(np_file):
                 if i == 0:
                     album_index = int(line.rstrip('\n'))
                 elif i == 1:
                     song_index = int(line.rstrip('\n'))
                 elif i == 2:
                     timestamp = int(line.rstrip('\n'))

    # read in song list if it exists
    if(isfile("/home/pi/radio_star/songs.txt")):
        with open("/home/pi/radio_star/songs.txt", "r") as song_file:
            song_paths = [line.rstrip('\n') for line in song_file]

    else:
        song_paths = []
        song_index = 0;
        if(album_index < len(album_paths)):
            for song in listdir(album_paths[album_index]):
              if(song.lower().endswith(".mp3")):
                song_paths.append(join(album_paths[album_index], song))

        else:
            print("We're out of albums, reshuffling!")
            system("/home/pi/radio_star/reshuffle.py")


        song_paths = sorted_nicely(song_paths)
        with open("/home/pi/radio_star/songs.txt", "w+") as song_file:
            for song in song_paths:
                song_file.write("%s\n" % song)
            song_file.flush()
            fsync(song_file.fileno())


        #TODO: reconstruct song list, album must have changed
        print ("Album list exists, but song list is missing!")

else:
    # create list of albums, storing the full path to them 
    for artist in listdir(pathname):
        full_artist_path = join(pathname, artist)
        artist_paths.append(full_artist_path)
        for album in listdir(full_artist_path):
            full_album_path = join(full_artist_path, album)
            if(isdir(full_album_path)):
                album_paths.append(full_album_path)
         
    shuffle(album_paths)

    # write album list to a file, so we can resume from the right album later
    with open("/home/pi/radio_star/albums.txt", "w+") as album_file:
        for item in album_paths:
            album_file.write("%s\n" % item)
        album_file.flush()
        fsync(album_file.fileno())


    for song in listdir(album_paths[0]):
        if(song.lower().endswith(".mp3")):
           song_paths.append(join(album_paths[0], song))

    song_paths = sorted_nicely(song_paths)

    with open("/home/pi/radio_star/songs.txt", "w+") as song_file:
        for item in song_paths:
            song_file.write("%s\n" % item)
        song_file.flush()
        fsync(song_file.fileno())

updateTimestamp()

print ("album index: " + str(album_index))
print ("song index: " + str(song_index))
print ("timestamp: " + str(timestamp))
print ("album_paths length = " + str(len(album_paths)))
print ("song_paths length = " + str(len(song_paths)))

while(album_index < len(album_paths)):
    if(song_index < len(song_paths)):
        print (song_paths[song_index])
        with open("/home/pi/radio_star/np_path.txt", "w+") as np_path:
            np_path.write(song_paths[song_index])        
            np_path.flush()
            fsync(np_path.fileno())

        #print("omxplayer -o alsa -l " + str(timestamp) + " " + quote(song_paths[song_index]))
        system("omxplayer -o alsa -l " + str(timestamp) + " " + quote(song_paths[song_index]))
        #print("omxplayer -o alsa -l " + str(timestamp) + " " + song_paths[song_index].replace(' ', '\ '))
        #system("omxplayer -o alsa -l " + str(timestamp) + " " + song_paths[song_index].replace(' ', '\ '))
        print ("////////////////////Next Song/////////////////////")
        song_index = song_index + 1
        timestamp = 0
    else:
        print ("/////////////////Next Album////////////////////")
        album_index = album_index + 1
        print (album_paths[album_index])
        song_paths = []
        song_index = 0;
        for song in listdir(album_paths[album_index]):
            if(song.lower().endswith(".mp3")):
                song_paths.append(join(album_paths[album_index], song))

        song_paths = sorted_nicely(song_paths)
        with open("/home/pi/radio_star/songs.txt", "w+") as song_file:
            for song in song_paths:
                song_file.write("%s\n" % song)
            song_file.flush()
            fsync(song_file.fileno())

