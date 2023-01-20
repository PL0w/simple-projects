'''
=================================================

motto: what do
Author: naaboo
About: a command line interface version of the MISC section of BB.com
=================================================
FEATURES: (active)
1) Beautiful logo
2) View entire misc homepage
3) View entire first page of a thread
=================================================
FEATURES: (pending)
1) Browse all pages of a thread seamlessly
2) View all of your threads + posts
3)
=================================================

'''

import requests
from bs4 import BeautifulSoup
import re

version = '0.0.1'

def display_logo():
    print(f'''
    
 $$$$$$\  $$\       $$$$$$\       $$\      $$\ $$$$$$\  $$$$$$\   $$$$$$\  
$$  __$$\ $$ |      \_$$  _|      $$$\    $$$ |\_$$  _|$$  __$$\ $$  __$$\ 
$$ /  \__|$$ |        $$ |        $$$$\  $$$$ |  $$ |  $$ /  \__|$$ /  \__|
$$ |      $$ |        $$ |        $$\$$\$$ $$ |  $$ |  \$$$$$$\  $$ |      
$$ |      $$ |        $$ |        $$ \$$$  $$ |  $$ |   \____$$\ $$ |      
$$ |  $$\ $$ |        $$ |        $$ |\$  /$$ |  $$ |  $$\   $$ |$$ |  $$\ 
\$$$$$$  |$$$$$$$$\ $$$$$$\       $$ | \_/ $$ |$$$$$$\ \$$$$$$  |\$$$$$$  | {version}
 \______/ \________|\______|      \__|     \__|\______| \______/  \______/ 
                                                                           
                                                                           
                                                                           

    ''')



def homepage():
    r = requests.get('https://forum.bodybuilding.com/forumdisplay.php?f=19&page=1&order=desc')
    soup = BeautifulSoup(r.content, 'html.parser')
    query = 31
    raw_title = soup.select('.title', limit=query)
    links = []
    [links.append('https://forum.bodybuilding.com/' + link['href']) for link in raw_title]    
    author = soup.find_all(class_='username understate', limit=query)
    for count, titles in enumerate(raw_title, start= 1):
        users = author[count-1].text
        if count < 10: 
            count = str(count)
            count = str(count.zfill(2))
        if len(users) > 9:
            print(f'> {count}: {users}\t - {titles.text.strip()}')
        else:print(f'> {count}: {users}\t\t - {titles.text.strip()}')
    return links


def checkPrevNext(html, soup):
    if soup.find(class_="prev_next"):
        return True
    else: return False


def displayThreadContents(url, soup):
    soup = BeautifulSoup (url.content, 'html.parser')
    user = soup.find_all(class_='popupmenu memberaction', limit=31)
    thread_title = soup.select('title', limit=1)
    comment = soup.find_all(class_='postcontent restore', limit =31)
    return user, thread_title, comment

def displayNextPage(html, soup):
    next_page_text = soup.find(class_='prev_next')
    next_page_URL = 'https://forum.bodybuilding.com/' + next_page_text.next['href']
    url = getURL(next_page_URL)
    author, thread_title, comment = displayThreadContents(url, soup)

    print('\n~~~~~~CLI MISC~~~~~~\n')
    print(f"\n[TITLE] {thread_title[0].string.strip()}\n[PAGE {next_page_text.name}]")
    for count, x in enumerate(author, start=1):
        name = x.text.split()
        print(f"\n> {name[0]}: {comment[count-1].text.strip()}\n")
        # print(comment.string)
    print('\n[Z]next-page] [X]prev-page] [C]back]\n')
    while True:
        match input('\n'):
            case 'z':
                if checkPrevNext(html ,soup):
                    displayNextPage(url, soup)

            case 'x':
                pass
            case 'c':
                break



def displayPrevPage(html, soup):
    pass

def getURL(url): return requests.get(url)
def thread(url, urlpos):
    r = requests.get(url[int(urlpos)-1])
    soup = BeautifulSoup(r.content, 'html.parser')
    query = 31
    author = soup.find_all(class_='popupmenu memberaction', limit=query)
    thread_title = soup.select('title', limit=1)
    comment = soup.find_all("blockquote", class_='postcontent restore',limit=query)
    display_logo()
    print(f"\n[TITLE] {thread_title[0].string.strip()}\n[PAGE 01]")
    for count, x in enumerate(author, start=1):
        name = x.text.split()
        print(f"\n> {name[0]}: {comment[count-1].text.strip()}\n")
    print('\n[Z]next-page] [X]prev-page] [C]back]\n')
    
    # Thread loop controls
    while True:
        match input('\n'):
            case 'z':
                 if checkPrevNext(r ,soup):
                    displayNextPage(r, soup)

            case 'x':
                pass
            case 'c':
                break

def misc():
    while True:  
        # print('\n~~~~~~CLI MISC~~~~~~\n')
        display_logo()
        links = homepage()

        # Main loop controls
        print('\n[Z]next-page] [X]prev-page] [C]login] [V]call-fbi]\n')
        match input('Enter thread # to view\n'):
            case 'z':
                pass
            case 'x':
                pass
            case 'c':
                break
            case int:
                thread(links, int)
misc()  