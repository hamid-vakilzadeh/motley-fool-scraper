"""
Author: Hamid Vakilzadeh, PhD
October 2022
Florida Atlantic University Workshop

This is an application that collects the earnings call transcripts from The Motley fool
URL: https://www.fool.com/earnings-call-transcripts/

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# open web browser (Google Chrome)
def open_new_browser():
    service = Service(executable_path=ChromeDriverManager().install())
    browser_options = webdriver.ChromeOptions()
    # browser_options.add_argument('--headless')
    browser = webdriver.Chrome(service=service)
    return browser


# create a list of transcript urls from the Earnings Call Transcript Page.
def get_article_urls(web_page_address: str, driver: webdriver.Chrome) -> list[str]:
    """
    create a list of transcript URL addresses.
    :param driver: webdriver to be used (e.g., Chrome)
    :param web_page_address: the address to the motley fool transcripts page
    (e.g., https://www.fool.com/earnings-call-transcripts/?=page=1).
    :return: a list of url addresses
    """
    driver.get(web_page_address)
    articles_panel = driver.find_element(by=By.ID, value='aggregator-article-container')
    article_rows = articles_panel.find_elements(by=By.CLASS_NAME, value="py-12px")

    # get href attribute for each article and add it to the url_list
    url_list: list = []
    for article_row in article_rows:
        url_to_transcript_text: str = article_row.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        url_list.append(url_to_transcript_text)

    return url_list


def get_transcript_html(transcript_url_address: str, driver: webdriver.Chrome) -> str:
    """
    get the transcript of earnings announcement and remove in-text advertisements.

    :param driver: webdriver to be used (e.g., Chrome)
    :param transcript_url_address: the url address to any transcript on https://www.fool.com/
    :return: transcript text with html markup.
    """
    my_browser.get(transcript_urls[0])
    ea_title = my_browser.find_element(by=By.CLASS_NAME, value="text-h3").text
    ea_html = my_browser.find_element(by=By.CLASS_NAME, value="tailwind-article-body").get_attribute('innerHTML')
    soup = BeautifulSoup(ea_html, 'html.parser')
    soup.find(name='div', attrs={'id': 'pitch'}).decompose()
    for item in soup.find_all(attrs={'class': 'interad'}):
        print(item)
        item.decompose()


if __name__ == '__main__':
    my_browser = open_new_browser()
    # navigate to fool.com earnings pages
    my_browser.get("https://www.fool.com/earnings-call-transcripts")
    transcript_urls = get_article_urls(web_page_address='https://www.fool.com/earnings-call-transcripts',
                                       driver=my_browser)


    # save the transcript in a file
    with open('ea_html_for_IDT.txt', mode='w') as file:
        file.write(ea_html)
