"""
Author: Hamid Vakilzadeh, PhD
October 2022
Florida Atlantic University Workshop

This is an application that collects the earnings call transcripts from The Motley fool
URL: https://www.fool.com/earnings-call-transcripts/
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
from pathlib import Path


# create output folder
output = 'outputs'
Path(output).mkdir(exist_ok=True)


# open web browser (Google Chrome)
def open_new_browser() -> webdriver.Chrome:
    service = Service(executable_path=ChromeDriverManager().install())
    browser_options = webdriver.ChromeOptions()
    # browser_options.add_argument('--headless')
    browser = webdriver.Chrome(service=service)
    return browser


# create a list of transcript urls from the Earnings Call Transcript Page.
def get_transcript_urls(driver: webdriver.Chrome,
                        web_page_address: Optional[str] =
                        'https://www.fool.com/earnings-call-transcripts') -> list[str]:
    """
    create a list of transcript URL addresses.

    :param driver: webdriver to be used (e.g., Chrome).
    :param web_page_address: the address to the motley fool transcripts page
    (e.g., https://www.fool.com/earnings-call-transcripts/?=page=1).
    :return: a list of url addresses
    """
    driver.get(web_page_address)
    try:
        cookies_button = driver.find_element(by=By.ID, value='onetrust-accept-btn-handler')
        if cookies_button:
            cookies_button.click()
    except NoSuchElementException:
        pass

    articles_panel = driver.find_element(by=By.ID, value='aggregator-article-container')
    article_rows = articles_panel.find_elements(by=By.CLASS_NAME, value="py-12px")

    # get href attribute for each article and add it to the url_list
    url_list: list = []
    for article_row in article_rows:
        url_to_transcript_text: str = article_row.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        url_list.append(url_to_transcript_text)

    return url_list


# TODO: create an index file and update the index file to avoid duplicate downloads
def update_url_index():
    pass


def get_transcript_html(transcript_url_address: str, driver: webdriver.Chrome) -> BeautifulSoup:
    """
    get the transcript of earnings announcement and remove in-text advertisements.

    :param driver: webdriver to be used (e.g., Chrome)
    :param transcript_url_address: the url address to any transcript on https://www.fool.com/
    :return: transcript text with html markup.
    """

    # open page and extract the transcript part
    driver.get(transcript_url_address)
    # ea_title = driver.find_element(by=By.CLASS_NAME, value="text-h3").text
    ea_html = driver.find_element(by=By.CLASS_NAME, value="tailwind-article-body").get_attribute('innerHTML')

    # remove ads and pitches (company advertisements)
    soup = BeautifulSoup(ea_html, 'html.parser')
    ads = soup.find_all(attrs={'id': 'pitch'})
    ads += soup.find_all(attrs={'class': 'interad'})
    for item in ads:
        item.decompose()

    return soup


if __name__ == '__main__':

    # open a new browser page
    my_browser = open_new_browser()

    # navigate to fool.com earnings pages
    transcript_urls = get_transcript_urls(web_page_address='https://www.fool.com/earnings-call-transcripts',
                                          driver=my_browser)

    # open each transcript page and save it in a file.
    for url in transcript_urls:
        file_name = url.split("/")[-2]
        url_html_text = get_transcript_html(url, driver=my_browser)

        # save the transcript in a file
        with open(os.path.join(output, f'{file_name}.txt'), mode='w') as file:
            file.write(str(url_html_text))

    # close the browser window
    my_browser.close()