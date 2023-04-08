# pip install multiprocess
# pip install selenium
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# A Service class that is responsible
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
# An Expectation for checking an element is visible
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


def click_ads_button(driver):
    try:
        ads_button = driver.find_element(
            By.CSS_SELECTOR,
            ads_button_selector,
        )
        ads_button.click()
    except Exception as e:
        print("Addd button not found")
    return


def click_mute_button(driver):
    driver.find_element(
        by=By.CLASS_NAME,
        value="ytp-mute-button",
    ).click()


def replay_video(driver):
    while True:
        try:
            driver.find_element(
                by=By.XPATH,
                value=replay_xpath,
            ).click()
        except NoSuchElementException as e:
            continue
        else:
            print("Replay")
            click_ads_button(driver)
            driver.execute_script(
                """document.querySelector('video').playbackRate = 16;"""
            )


def run_video(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    driver.get_window_size()
    time.sleep(30)
    try:
        consent = driver.find_element(By.XPATH, consent_button_xpath)
        consent.click()
        time.sleep(10)
        click_ads_button(driver)
        time.sleep(10)
        click_mute_button(driver)
        driver.execute_script("""document.querySelector('video').playbackRate = 16;""")
        replay_video(driver)
    except NoSuchElementException as e:
        print("kkkk ", e)
        driver.close()
        driver.quit()


def get_links():
    homepage = input("Please provide homepage: ")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(homepage)
    consent = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, consent_button_xpath_homepage))
    )
    consent.click()
    links = driver.find_elements(by=By.CLASS_NAME, value=video_links_class_name)
    links = [link.get_attribute("href") for link in links if link.get_attribute("href")]
    driver.close()
    driver.quit()
    return links


if __name__ == "__main__":

    links = get_links()
    print(links)
    processes = []
    for link in links[:5]:
        p = multiprocessing.Process(target=run_video, args=(link,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
