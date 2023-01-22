from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions import pointer_actions
import time


username = input('Enter username: ') 
password = input('Enter password: ')

browser = webdriver.Firefox()
site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
browser.get(site)

time.sleep(3)

user_field = browser.find_element(By.NAME, 'username')
pass_field = browser.find_element(By.NAME, 'password')

user_field.send_keys(username)
pass_field.send_keys(password)
browser.find_element(By.CLASS_NAME, 'combined-sign-in--button').click()

# time.sleep(5)

# GOTO user CP
browser.get('https://forum.bodybuilding.com/usercp.php')

print('CLICK OFF POPUP')
# time.sleep(8)

# Click off "want 15% off?" popup
# browser.find_element(By.CLASS_NAME, "modal__cross").click()

browser.find_element(By.CLASS_NAME, 'smallfont').click() # first thread in control panel
# time.sleep(3)
browser.find_element(By.CLASS_NAME, 'username').click() # open username menu
# time.sleep(1)
browser.find_element(By.CLASS_NAME, 'right').click() # opens post history link
# time.sleep(3)

thread_list = browser.find_elements(By.CLASS_NAME, 'posttitle a')
thread_names = browser.find_elements(By.CLASS_NAME, 'username_container h2 a')

browser.find_element(By.CLASS_NAME, 'posttitle a').click() # enter thread
# time.sleep(3)
browser.find_element(By.CLASS_NAME, 'editpost').click()  # edits post for del
# time.sleep(1)
browser.find_element(By.ID, 'vB_Editor_QE_1_delete').click() # deletes post
