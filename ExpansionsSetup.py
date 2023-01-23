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
def MTG_scraping_cardmarket(completeLinks=False):
    soup = request_block("https://www.cardmarket.com/en/Magic/Products/Singles")
    # print(soup)
    found = str(soup.find_all("select")[1])
    all_ext = re.findall(r'<option(.*?)/option>', found)
    all_ext.pop(0)
    all_id_list = []
    for exp in all_ext:
        value = re.findall(r'value=\"(.*?)\"', exp)[0]
        name = re.findall(r'\">(.*?)<', exp)[0]
        # name = re.sub('[^a-zA-Z0-9]+', '', name)
        all_id_list.append([name, value])
    the_list = []
    # all_id_list now contanins all possible expansions value
    for expansion in all_id_list:
        # time.sleep(5) # lil sleeping
        # go to the expansion
        url = "https://www.cardmarket.com/en/Magic/Products/Singles?idCategory=1&idExpansion=" + expansion[
            1] + "&idRarity=0&perSite=20"
        soup = request_block(url)
        if completeLinks:
            meta = soup.find('link', rel="canonical")
            href = re.findall(r'href=\"(.*?)\" ', str(meta))[0]
            print(href)
        else:
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


def YGO_scraping_cardmarket(completeLinks=False):
    soup = request_block("https://www.cardmarket.com/en/YuGiOh/Products/Singles")
    # print(soup)
    found = str(soup.find_all("select")[1])
    all_ext = re.findall(r'<option(.*?)/option>', found)
    all_ext.pop(0)
    all_id_list = []
    for exp in all_ext:
        value = re.findall(r'value=\"(.*?)\"', exp)[0]
        name = re.findall(r'\">(.*?)<', exp)[0]
        # name = re.sub('[^a-zA-Z0-9]+', '', name)
        all_id_list.append([name, value])
    the_list = []
    # all_id_list now contanins all possible expansions value
    for expansion in all_id_list:
        time.sleep(10) # lil sleeping
        # go to the expansion
        url = "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=1&idExpansion=" + expansion[
            1] + "&idRarity=0&perSite=20"
        soup = request_block(url)
        expansion_title_soup = str(soup.find('title'))
        link_title = soup.find_all("link", rel="canonical")[0]
        # print(link_title)
        base_link_url = re.findall(r'href=\"(.*?)\"', str(link_title))
        try:
            expansion_title = re.findall(r'<title>(.*?) - ', expansion_title_soup)[0]
            # scrape the first card, doesn't matter the card
            found = str(soup.find_all("div", class_="table-body")[0])
            sets = re.findall(r'<span>(.*?)</span>', found)
            if len(sets) > 0:
                print(sets[0]+", "+expansion[1]+", "+base_link_url[0]+", "+expansion[0])
            else:
                print("Expansion : {} did not contain any link".format(expansion_title))
        except Exception as exp:
            print("there was a problem with {}, {}".format(expansion, exp))


def Pokemon_scraping_cardmarket(completeLinks=False):
    soup = request_block("https://www.cardmarket.com/fr/Pokemon/Products/Singles")
    # print(soup)
    found = str(soup.find_all("select")[1])
    all_ext = re.findall(r'<option(.*?)/option>', found)
    all_ext.pop(0)
    all_id_list = []
    for exp in all_ext:
        value = re.findall(r'value=\"(.*?)\"', exp)[0]
        name = re.findall(r'\">(.*?)<', exp)[0]
        # name = re.sub('[^a-zA-Z0-9]+', '', name)
        all_id_list.append([name, value])
    the_list = []
    # all_id_list now contanins all possible expansions value
    all_id_list = all_id_list[200:]
    for expansion in all_id_list:
        # time.sleep(5) # lil sleeping
        # go to the expansion
        url = "https://www.cardmarket.com/en/YuGiOh/Products/Singles?idCategory=1&idExpansion=" + expansion[
            1] + "&idRarity=0&perSite=20"
        soup = request_block(url)
        link_title = soup.find_all("link", rel="canonical")[0]
        # print(link_title)
        base_link_url = re.findall(r'href=\"(.*?)\"', str(link_title))
        if completeLinks:
            meta = soup.find('link', rel="canonical")
            href = re.findall(r'href=\"(.*?)\" ', str(meta))[0]
            print(href)
        else:
            # scrape the first card, doesn't matter the card
            found = str(soup.find_all("div", class_="table-body")[0])
            urls = re.findall(r'<a href="(.*?)"', found)
            if len(urls) > 0:
                card_url = "https://www.cardmarket.com" + urls[0]
                card_soup = request_block(card_url)
                expansion_title_soup = card_soup.find_all("img", src="/img/transparent.gif")
                # print("--", expansion_title_soup)
                try:
                    expansion_title = \
                    re.findall(r'static\.cardmarket\.com\/img\/[0-9a-z]*\/items/[0-9A-Za-z]*\/(.*?)\/',
                               str(expansion_title_soup))[0]
                    # print("Expansion title : {}".format(expansion_title))
                    print("{}, {}, {}".format(expansion_title, expansion[1], base_link_url[0]))
                except Exception as exp:
                    print("Exception with {} : {}".format(expansion, exp))
            else:
                print("Expansion : {} did not contain any link".format(expansion_title))
YGO_scraping_cardmarket()
# Pokemon_scraping_cardmarket()
# with open(".pokemon", "r") as w11:
#     with open("only_name_pkmn.txt", "r") as w22:
#         lines1 = w11.read().splitlines()
#         lines2 = w22.read().splitlines()
#         print(len(lines1))
#         print(len(lines2))
#         for i, elem in enumerate(lines1):
#             print("{}, {}".format(elem, lines2[i]))
