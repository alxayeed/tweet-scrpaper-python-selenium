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
        WebDriverWait(driver, 20).until(
            lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


waiting_func('link text', 'Log in')
login_btn = driver.find_element_by_link_text('Log in')
time.sleep(5)
login_btn.click()

# get email input field and fill it with username
waiting_func('name', "session[username_or_email]")
time.sleep(5)
email_input = driver.find_element_by_name("session[username_or_email]")
username = os.environ['USER_NAME']
email_input.send_keys(username)

# get password input field and fill it with username
waiting_func('name', "session[password]")
password_input = driver.find_element_by_name("session[password]")
password = os.environ['PASSWORD']
password_input.send_keys(password, Keys.ENTER)
driver.switch_to.default_content()

# go to account
account_url = f'{url}/{username}'
driver.get(account_url)

# this will contain all the tweet details links
tweets_path = []
while True:
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    tweet_path = driver.find_elements_by_css_selector(
        "[aria-label='View Tweet activity']")

    tweets_path.extend([tweet.get_attribute('href') for tweet in tweet_path])
    driver.execute_script("window.scrollTo(0, {})".format(last_height + 500))
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break


print(tweets_path)
# locate the iframe of tweet dashboard
tweet_details = []
for path in tweets_path:
    driver.get(path)

    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )

    driver.switch_to.frame(iframe)

    detail = driver.find_element_by_tag_name('body')
    title = detail.find_element_by_class_name('QuoteTweet-text').text

    impression = detail.find_element_by_class_name('ep-MetricAnimation')
    # engagements = detail.find_element_by_class_name('ep-EngagementsSection')
    # print(f"title is {title} \nTotal Impression {impression.text}")
    tweet_array = {}
    tweet_array['title'] = title
    tweet_array['impression'] = impression.text

    # engagements
    try:
        WebDriverWait(driver, 3).until(
            lambda x: x.find_element(
                by="class name", value="ep-ViewAllEngagementsButton")
        )

        view_all = driver.find_element_by_class_name(
            'ep-ViewAllEngagementsButton')
        view_all.click()

        engagement_details = driver.find_elements_by_class_name(
            'ep-SubSection')

        for _ in engagement_details:
            print(_.text)

        # total_engagements = driver.find_element_by_class_name(
        #     'ep-MetricTopContainer')
        # title = total_engagements.find_element_by_class_name(
        #     'ep-MetricName').text
        # total = total_engagements.find_element_by_class_name(
        #     'ep-MetricValue').text

        # print(title, total)

        # tweet_array[title] = total

        # sub_section = driver.find_element_by_class_name(
        #     'ep-EngagementsSection')
        # sub_section_top = sub_section.find_element_by_class_name(
        #     'ep-MetricTopContainer')
        # title = sub_section_top.find_element_by_class_name(
        #     'ep-MetricName').text
        # total = sub_section_top.find_element_by_class_name(
        #     'ep-MetricValue').text

        # print(title, total)
        # tweet_array[title] = total

        # links_click_section = driver.find_element_by_class_name(
        #     'ep-SubSection')
        # sub_section_top = links_click_section.find_element_by_class_name(
        #     'ep-MetricTopContainer')
        # title = sub_section_top.find_element_by_class_name(
        #     'ep-MetricName').text
        # total = sub_section_top.find_element_by_class_name(
        #     'ep-MetricValue').text

        # print('printing links click')
        # print(title, total)
        # tweet_array[title] = total

        # tweet_details.append(tweet_array)

    except TimeoutException:
        pass


# print(tweet_details)
