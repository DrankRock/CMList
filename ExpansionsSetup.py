import csv
import sys

import requests, re, time, os
from bs4 import BeautifulSoup
from dataclasses import dataclass

FILE = open(".expansions.txt", "w+")


def request_block(link):
    try:
        page = requests.get(link)
        while page.status_code != 200:
            if page.status_code == 429:
                print("\rIP blocked  Around 1min pause.")
                time.sleep(10)
                page = requests.get(link)
            else:  # if page 404 or else
                return -1
    except Exception as e:
        print("Unexpected Error :\n{}".format(e))
    soup = BeautifulSoup(page.content, "lxml")
    return soup

# I will be sleeping 5 between each scrapes because I'm putting too much on CM
def MTG_scraping_cardmarket():
    soup = request_block("https://www.cardmarket.com/en/Magic/Products/Singles")
    # print(soup)
    found = str(soup.find_all("select")[1])
    all_ext = re.findall(r'<option(.*?)/option>', found)
    all_id_list = []
    for exp in all_ext:
        value = re.findall(r'value=\"(.*?)\"', exp)[0]
        name = re.findall(r'\">(.*?)<', exp)[0]
        # name = re.sub('[^a-zA-Z0-9]+', '', name)
        all_id_list.append([name, value])
    the_list = []
    # all_id_list now contanins all possible expansions value
    for expansion in all_id_list:
        time.sleep(5) # lil sleeping
        # go to the expansion
        url = "https://www.cardmarket.com/en/Magic/Products/Singles?idCategory=1&idExpansion=" + expansion[
            1] + "&idRarity=0&perSite=20"
        print(url)
        soup = request_block(url)
        expansion_title_soup = str(soup.find('title'))
        print(expansion_title_soup)
        try:
            expansion_title = re.findall(r'<title>(.*?) - ', expansion_title_soup)[0]
            # scrape the first card, doesn't matter the card
            found = str(soup.find_all("div", class_="table-body")[0])
            urls = re.findall(r'<a href="(.*?)"', found)
            if len(urls) > 0:
                card_url = "https://www.cardmarket.com" + urls[0]
                card_soup = request_block(card_url)
                title_1 = str(card_soup.find('title'))  # get base
                title_2 = re.findall(r'<title>(.*?) - ', title_1)[0]  # gget only interesting part
                title_3 = re.findall(r'\((.*?)\)', title_2)  # get all thats between parenthesis
                title = title_3[-1]  # only keep the last
                print("\"{}\", \"{}\", {}".format(expansion_title, title, expansion[1]))
                the_list.append([expansion_title, title, expansion[1]])
            else:
                print("Expansion : {} did not contain any link".format(expansion_title))
        except Exception as exp:
            print("there was a problem with {}, {}".format(expansion, exp))


MTG_scraping_cardmarket()