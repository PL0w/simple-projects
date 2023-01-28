from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time 
import os   # to clear screen
import sys  # to exit program 

version = '0.6a'

def displayLogo():
    print(f'''
    
 ██████  ██   ██  ██████  ███████ ████████    ███    ███ ███████    ██████   ██████  ██    ██  ██████  ███████ 
██       ██   ██ ██    ██ ██         ██       ████  ████ ██         ██   ██ ██    ██  ██  ██  ██    ██ ██      
██   ███ ███████ ██    ██ ███████    ██       ██ ████ ██ █████      ██████  ██    ██   ████   ██    ██ ███████ 
██    ██ ██   ██ ██    ██      ██    ██       ██  ██  ██ ██         ██   ██ ██    ██    ██    ██    ██      ██ 
 ██████  ██   ██  ██████  ███████    ██    ██ ██      ██ ███████ ██ ██████   ██████     ██     ██████  ███████ {version}
                                                                                                               
                                                                                                               
''')

def checkVisibility(elem):
    return WebDriverWait(browser, 10).until(EC.visibility_of(elem))
def checkClickability(elem):
    return WebDriverWait(browser, 10).until(EC.element_to_be_clickable(elem))

################# START #################



################# LOGIN #################\

username = password = False
# Enter user/pass
while not (username and password):
    os.system('cls')
    displayLogo()
    username = input('Enter username: ') 
    password = input('Enter password: ')
    print('')

# Create Firefox object
browser = webdriver.Firefox()
site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
browser.get(site)

# Search for username field, input username
try: 
    user_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'username')))
    if user_field:
        user_field.send_keys(username)
except ElementNotVisibleException: print('Username field not found...')

# Search for password field, input password
try:
    pass_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
    if pass_field:
        pass_field.send_keys(password)
except ElementNotVisibleException: print('Password field not found...')


# Click off "want 15% off?" popup
ugh = 'N'
while ugh != 'Y':
    ugh = input('\nDid you remove 15% off popup? (Y/N) ')


# try:
#     fifteenoff = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ab-programmatic-close-button')))
# except: pass
# didclose = input('did id close?')

# Click 'sign-in' button
try:
    login = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'combined-sign-in--button'))).click()
except ElementClickInterceptedException: print('Sign-in not reached...')

# Wait page load
time.sleep(3)

################# USERID #################

# Load BB.com dark theme
dark_mode = 'https://forum.bodybuilding.com/?styleid=63'
browser.get(dark_mode)

# Checks for user id (determines login success)
try:
    id1 = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcomelink [HREF]')))
    print('Login successful...')
except NoSuchElementException: print('Login unsuccessful...')

# Split id from link
id2 = id1.get_attribute('href')
id3 = id2.split('=')
user_id = id3[1]

################# POST HISTORY #################

post_history = f'https://forum.bodybuilding.com/search.php?do=finduser&userid={user_id}&contenttype=vBForum_Post&showposts=1'
browser.get(post_history)

# get temp search id
search_id_a = browser.current_url
search_id_b = search_id_a.split('=')
search_id = search_id_b[1]

# option to not delete recent posts
post_history_page_num = input('\n(Default is 1)\nEnter page # to start deleting from: ')
post_history_page = f'https://forum.bodybuilding.com/search.php?searchid={search_id}&pp=&page={post_history_page_num}'
if int(post_history_page_num) > 1:
    browser.get(post_history_page)

try: # create list of thread links
    thread_links_elem = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]'))) 
except TimeoutException: 
    print('\nPost history not found...')

# stats
posts_deleted = 0

################# PAGES + THREAD #################

while thread_links_elem:

    print(f'\nPAGE: [{post_history_page_num}]')
    
    for count, x in enumerate(thread_links_elem, start=0):       
        
        # For each item in thread_list, GET 'HREF' attr
        thread_link = x.get_attribute('href')
        
        # Split post ID from URL
        x = thread_link.split('post')
        y = x[1]
        
        # concat to edit corresponding post ID
        z = 'vB::QuickEdit::' + y

        browser.execute_script(f'''window.open("{thread_link}", "_blank");''')

        window_name = browser.window_handles[-1] # focus last tab
        browser.switch_to.window(window_name=window_name)
        
        # check if locked thread
        thread_status = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'newcontent_textcontrol')))
        if thread_status.text == 'Closed Thread':
            print('Thread locked.')
            browser.close()
            # focus first tab
            window_name = browser.window_handles[0] 
            browser.switch_to.window(window_name=window_name)
            continue
        
        try: # edits post for del. targ -> "vB::QuickEdit::" + post ID
            edit_post = WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.NAME, z))).click()
        except ElementClickInterceptedException: 
            print('Unable to click edit button...')

        try: # deletes post
            delete_post = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, 'vB_Editor_QE_1_delete'))).click() 
        except ElementClickInterceptedException: 
            print('Unable to click delete button...')

        try: # toggle 'delete message radio button'
            dlt_radio_toggle = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dep_ctrl'))).click() 
        except ElementClickInterceptedException: 
            print('Unable to click toggle delete button...')

        try: # confirm delete
            confirm_delete = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, 'quickedit_dodelete'))).click()
        except ElementClickInterceptedException: 
            print('Unable to click confirm delete button...')
        
        posts_deleted += 1
        print(f'[{posts_deleted}] posts deleted')
        
        # close thread
        browser.close() 
        # focus first tab
        window_name = browser.window_handles[0] 
        browser.switch_to.window(window_name=window_name)
    
    try: # next page   
        next_page_list = WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'prev_next [href]')))
        next_page = next_page_list[1]
        next_page.click()
    except ElementNotVisibleException: 
        print('Next page not found...')
        input('Press enter to close program.\n')
        sys.exit()

    # update page num
    post_history_page_num = str(int(post_history_page_num) + 1)
    
    try: # get title links
        thread_links_elem = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]')))
    except NoSuchElementException: 
        print('\nPost history not found...')
        input('\nPress enter to close program.\n')
        sys.exit()