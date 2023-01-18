'''
    an image downloader for some site
'''
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from pathlib import Path
import os
import time
#################
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
#################


def getUserInput(): return input('Enter URL: ')

def downloadImage(): pass

# Request URL, return request object
def requestURL(url): 
    time.sleep(1.5)
    # return requests.get(url, timeout=5.000)
    #################################################
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session.get(url, timeout=3)
    #################################################
    
# Parses HTML doc
def beautilfulSoupHTML(url):
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup

# Change directory
def chDir(): os.chdir('C:/Users/boonn/Downloads/New folder (3)')
    
def getImagesHTML(soup): return soup.find_all('img')

def createImageURL(image, count):
    x = image[count]['src']
    return 'https://' + x.strip('//')

def xxx(image_list):
    for count, x in enumerate(image_list, start=0):             # Loop image list
        img_url = createImageURL(image_list, count)             # create each img URL
        if img_url.endswith('.jpg'):                            # if image is JPEG
            img_byte = requestURL(img_url)                      # get req image URL
            with Image.open(BytesIO(img_byte.content)) as img:  # open img byte data
                img.save(f'image{count}.jpeg', "JPEG")          # save image as jpeg
                print(f'downloaded {img_url}...')               

# START
def starter():    
    chDir()                         # Change DIR
    x = getUserInput()              # Get URL
    url = requestURL(x)             # Req URL
    html = beautilfulSoupHTML(url)  # Beautiful HTML
    image_list = getImagesHTML(html)
    xxx(image_list)
    
starter()