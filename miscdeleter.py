import requests
from bs4 import BeautifulSoup

# Get user ID
# misc_id = input('Enter user ID#: ')
# # Req user ID concat
# r = requests.get('https://forum.bodybuilding.com/search.php?searchid=' + misc_id)
r = requests.get('https://forum.bodybuilding.com/search.php?searchid=2857114053&pp=&page=4')
# Parse HTML from GET req object
page = BeautifulSoup(r.content, 'html.parser')
# Find all thread titles
thread_titles = page.find_all(class_='above_body')
# Print titles
print(thread_titles)
