"""
Allows the user to download a song via the song name and artist

Errors:
    InfoNeeded --> caused when not enough information is given
    SongNotFound --> caused when a given song cannot be SongNotFound


Process:
    1. Input song name (and artist if needed), optional pre-selection of song, and download location
    2. Display results and request selection / use pre-selection
    3. Download song, change metadata given user input for 'Song Name' and 'Artist'


@author spagbag03
"""
from __future__ import unicode_literals
from selenium import webdriver
from bs4 import BeautifulSoup
import youtube_dl
import re
import os


def download_song(link):
    """
    Download song from youtube
    :link: youtube link
    """
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    # change directory
    os.chdir('./songs')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def get_yt_url(*args):
    """
    Returns YouTube video link
    """
    # driver setup
    driver_path = '/Applications/chromedriver'
    binary_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.binary_location = binary_path
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # getting the url
    yt_url = 'https://www.youtube.com/results?search_query=description%3A'
    for arg in args:
        new_arg = '+' + re.sub('\W','+',arg)
        yt_url += new_arg
    driver.get(yt_url)
    html = driver.page_source
    soup = BeautifulSoup(html, features='html.parser')
    driver.close()
    for a in soup.find_all('a', href=True):
        if 'watch' in a['href']:
            v_url = 'https://www.youtube.com'+a['href']
            break
    return v_url

def remote_input(query):
    v_url = get_yt_url(query)
    download_song(v_url)

def main():
    while True:
        query = input('search: ')
        if query == '': break
        v_url = get_yt_url(query)
        download_song(v_url)


if __name__ == "__main__":
    main()
