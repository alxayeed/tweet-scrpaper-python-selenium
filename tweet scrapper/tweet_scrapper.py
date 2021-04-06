import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


# Access to twitter
options = Options()
# start the browser window at maximized size
options.add_argument("--start-maximized")

url = 'https://twitter.com'
driver = webdriver.Chrome(options=options)
driver.get(url)


def waiting_func(by_variable, attribute):
    try:
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


waiting_func('link text', 'Log in')
login_btn = driver.find_element_by_link_text('Log in')
time.sleep(3)
login_btn.click()

# get email input field and fill it with username
waiting_func('name', "session[username_or_email]")
email_input = driver.find_element_by_name("session[username_or_email]")
username = os.environ['USER_NAME']
email_input.send_keys(username)

# get password input field and fill it with username
waiting_func('name', "session[password]")
password_input = driver.find_element_by_name("session[password]")
password = os.environ['PASSWORD']
password_input.send_keys(password, Keys.ENTER)
