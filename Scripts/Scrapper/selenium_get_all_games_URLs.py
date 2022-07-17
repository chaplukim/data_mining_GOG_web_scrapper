"""
Project: Data-Mining GOG (Good Old Games)
Import URLs FIle
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import os
import config

# Constant
STOP_SELENIUM_AFTER_NO_PAGES = 3


def get_game_urls(gog_url):
    """
    Goes through the website pages and fetch all game urls
    :return: a list of all games urls
    """
    # User default setting for chromium behavior
    my_chrome_options = Options()
    my_chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install()
                              , chrome_options=my_chrome_options)

    # get the first page (ie 1)
    index = config.FIRST_PAGE_INDEX
    game_urls = []
    while index:

        # Ignore: for testing and QA.
        # if index == 3:
        #     break

        # list_length = len(game_urls)

        # opens chrome + GAME ID
        driver.get(gog_url + str(index))
        if index > config.FIRST_PAGE_INDEX and driver.current_url == config.GOG_URL:  # if it returns to the first
            # page finish
            break

        try:
            # collecting the number of elements in the page (each game)
            elms = WebDriverWait(driver, config.TEN_SECONDS).until \
                (EC.presence_of_all_elements_located((By.TAG_NAME, config.MAIN_TAG)))
            # push to variable "game_urls" the full URL of the game
            for elem in elms:
                # The href attribute specifies the URL of the page the link goes to.
                # Gets the given attribute or property of the element.
                # This method will first try to return the value of a property with the given name.
                # If a property with that name doesn’t exist, it returns the value of the attribute with the same name.
                # If there’s no attribute with that name, None is returned.
                href = elem.get_attribute(config.HREF)
                if href is not None and href.startswith(config.GAMES_URL_PATH):
                    game_urls.append(href)
            print(f"Fetched games from page {index}")
            index += 1
        except EC.StaleElementReferenceException:
            time.sleep(1)
            print(f'stale element reference raised for page {index}, skipping page...')
            index += 1

        # no pages threshold for each execution
        if index == STOP_SELENIUM_AFTER_NO_PAGES:
            break

    driver.quit()
    return list(set(game_urls))
