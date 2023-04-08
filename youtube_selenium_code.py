# pip install multiprocess
# pip install selenium
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# A Service class is responsible
# for the starting and stopping of chromedriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# An explicit wait is a code you define
# to wait for a certain condition to occur
# before proceeding further in the code
from selenium.webdriver.support import expected_conditions as EC

# Selenium Python binding provides some convenience methods
# so you don’t have to code an expected_condition class yourself
# An expectation for checking an element is visible
# and enabled such that you can click it.
from selenium.common.exceptions import NoSuchElementException

# Thrown when element could not be found.
import time


# homepage = "https://www.youtube.com/@AthanasiouApostolos/videos"
consent_button_xpath_homepage = "//button[@aria-label='Accept all']"
video_links_class_name = "yt-simple-endpoint.ytd-thumbnail"
consent_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
ads_button_selector = "button.ytp-ad-skip-button"
mute_button_class = "ytp-mute-button"
replay_xpath = '//*[@title="Replay"]'
# // -> Selects nodes in the document from the current node
# that match the selection no matter where they are
# * -> Matches any element node


def get_channel_links():
    homepage = input("Please provide channel url: ")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(homepage)
    consent_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, consent_button_xpath_homepage))
    )
    consent_button.click()
    link_lst = driver.find_elements(By.CLASS_NAME, video_links_class_name)
    links = [
        link.get_attribute("href") for link in link_lst if link.get_attribute("href")
    ]
    driver.close()
    driver.quit()
    return links


def click_skip_adds(driver):
    try:
        skip_adds_button = driver.find_element(By.CSS_SELECTOR, ads_button_selector)
        skip_adds_button.click()
    except NoSuchElementException as e:
        print("No adds button found")
        pass


def click_mute_button(driver):
    try:
        mute_button = driver.find_element(By.CLASS_NAME, mute_button_class)
        mute_button.click()
    except NoSuchElementException as e:
        print("Mute button not found")
        pass


def replay(driver):
    while True:
        try:
            replay_button = driver.find_element(By.XPATH, replay_xpath)
            replay_button.click()
        except NoSuchElementException as e:
            continue
        else:
            print("Replay")
            driver.execute_script(
                """document.querySelector("video").playbackRate=16;"""
            )


def run_video(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    time.sleep(30)
    try:
        consent = driver.find_element(By.XPATH, consent_button_xpath)
        consent.click()
        time.sleep(15)
        click_skip_adds(driver)
        time.sleep(10)
        click_mute_button(driver)
        time.sleep(7)
        driver.execute_script("""document.querySelector("video").playbackRate=16;""")
        replay(driver)
    except Exception as e:
        print("Exception is ", e)
        driver.close()
        driver.quit()


if __name__ == "__main__":
    links = get_channel_links()
    processes = []
    for link in links[:4]:
        p = multiprocessing.Process(target=run_video, args=(link,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
