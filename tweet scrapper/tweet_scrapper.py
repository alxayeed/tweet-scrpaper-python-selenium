from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Access to twitter
url = 'https://twitter.com'
driver = webdriver.Chrome()
driver.get(url)

try:
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Log in"))
    )

finally:
    print(login_btn)
    login_btn.click()


# login_btn = driver.find_element_by_xpath("//div[@class='css-1dbjc4n']")
