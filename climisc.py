import requests
from bs4 import BeautifulSoup
import re


# [print('Thread:',titles.text.strip()) for titles in raw_title]
# [print(user.text.strip()) for user in author]

        
# print('\n~~~~~~~~~~~~~~~~~~~')

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

def thread(url, urlpos):
    r = requests.get(url[int(urlpos)-1])
    soup = BeautifulSoup(r.content, 'html.parser')
    query = 10
    author = soup.find_all(class_='popupmenu memberaction', limit=query)
    thread_title = soup.select('title', limit=1)
    comment = soup.find_all(class_='postcontent restore',limit=query)

    print('\n~~~~~~CLI MISC~~~~~~\n')
    print(f"\n[Title] {thread_title[0].string.strip()}\n[Page 01]")
    for count, x in enumerate(author, start=1):
        name = x.text.split()
        print(f"\n> {name[0]}: {comment[count-1].text.strip()}\n")
    print('\n[Z]next-page] [X]prev-page] [C]back]\n')
    
    # Thread loop controls
    while True:
        match input('\n'):
            case 'z':
                pass
            case 'x':
                pass
            case 'c':
                break

def misc():
    while True:  
        print('\n~~~~~~CLI MISC~~~~~~\n')
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