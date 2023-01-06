import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://forum.bodybuilding.com/forumdisplay.php?f=19&page=1&order=desc')
soup = BeautifulSoup(r.content, 'html.parser')

query = 31
raw_title = soup.select('.title', limit=query)
links = []
[links.append('https://forum.bodybuilding.com/' + link['href']) for link in raw_title]    
author = soup.find_all(class_='username understate', limit=query)

print('\n~~~~~~CLI MISC~~~~~~\n')
# [print('Thread:',titles.text.strip()) for titles in raw_title]
# [print(user.text.strip()) for user in author]

for count, titles in enumerate(raw_title, start= 1):
    users = author[count-1].text
    if count < 10: 
        count = str(count)
        count = str(count.zfill(2))
    if len(users) > 9:
        print(f'> {count}: {users}\t - {titles.text.strip()}')
    else:print(f'> {count}: {users}\t\t - {titles.text.strip()}')
        
print('\n[1]next-page] [2]prev-page] [3]login] [4]call-fbi]\n')
# print('\n~~~~~~~~~~~~~~~~~~~')

def misc():
    while True:
        print('Enter thread # to view')
        match input():
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
misc()  