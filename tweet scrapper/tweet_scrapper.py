from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Access to twitter
url = 'https://twitter.com'
driver = webdriver.Chrome()
driver.get(url)


def waiting_func(by_variable, attribute):
    try:
        WebDriverWait(driver, 20).until(
            lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


# try:
#     login_btn = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.LINK_TEXT, "Log in"))
#     )
# finally:
#     login_btn.click()

waiting_func('link text', 'Log in')
login_btn = driver.find_element_by_link_text('Log in')
login_btn.click()
