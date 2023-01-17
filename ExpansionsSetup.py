import csv

import requests, re, time, os
from bs4 import BeautifulSoup
from dataclasses import dataclass

FILE = open(".expansions.txt", "w+")

def request_block(link):
    try:
        page = requests.get(link)
        while (page.status_code != 200):
            if (page.status_code == 429):
                print("\rIP blocked  Around 1min pause.")
                time.sleep(5)
                page = requests.get(link)
            else:  # if page 404 or else
                return -1
    except Exception as e:
        print("Unexpected Error :\n{}".format(e))
    soup = BeautifulSoup(page.content, "lxml")
    return soup


def Magic():
    # using mtg Fandom :

    soup = request_block("https://mtg.fandom.com/wiki/Set")
    # print(soup)
    array = str(soup.find_all("table", class_="wikitable sortable mw-collapsible")[0])
    lines = array.split('\n')
    i = 0
    output = []
    output_iterator = 0
    try :
        for line in lines:
            # print(i, line)
            if i == 2:
                i -= 1
            elif i == 1:
                if "<td>" in line and "</td>" in line :
                    i -= 1
                    value = re.findall(r'<td>(.*?)</td>', line)[0]
                    # print(value)
                    output[output_iterator].append(value)
                    # print(" -- ", output[output_iterator])
                    output_iterator += 1
            elif "<i>" in line and "title=" in line:
                name = re.findall(r'\" title=\"(.*?)\">', line)[0]
                # print(name)
                output.append([name])
                i = 2
    except Exception as exc :
        print(exc)
    fields = ["Name", "SET"]
    write = csv.writer(FILE)
    write.writerow(fields)
    write.writerows(output)
    # print(output)
    # print(array)

def MTG():
    url = "https://scryfall.com/sets"
    str_soup = str(request_block(url))
    all_lines = str_soup.split('\n')
    output = []
    for line in all_lines :
        if "<small>" in line :
            name = line.split("<small>")[0].strip()
            abrv = line.split("<small>")[1].replace("</small>", "")
            output.append([name, abrv])
    output = sorted(output)
    for elem in output:
        print(elem)
    return output
    # all_names = re.findall(r'   (.*?)</small>')
    # print(str(soup))

def Cardmarket_MTG():
    soup = request_block("https://www.cardmarket.com/en/Magic/Products/Singles")
    # print(soup)
    found = str(soup.find_all("select")[1])
    all_ext = re.findall(r'<option(.*?)/option>', found)
    output=[]
    for elem in all_ext:
        value=re.findall(r'value=\"(.*?)\"', elem)[0]
        name=re.findall(r'\">(.*?)<', elem)[0]
        output.append([name, value])
        # print([value, name])
    output = sorted(output)
    print(len(output))
    # print(found)
    # list_found = found.split('\n')
    for line in output :
        print(line)
    return output




print(Cardmarket_MTG())
print(MTG())
