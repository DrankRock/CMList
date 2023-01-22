import requests, re, time, os
from bs4 import BeautifulSoup


def request_block(link):
    try:
        page = requests.get(link)
        while (page.status_code != 200):
            if (page.status_code == 429):
                print("\r[{}/{}] - IP blocked by CM. Around 1min pause.".format(iteration + 1,
                                                                                len(possibleExpansionsListLinks)),
                      end='')
                time.sleep(5)
                page = requests.get(link)
            else:  # if page 404 or else
                return -1
    except Exception as e:
        print("Unexpected Error :\n{}".format(e))
    soup = BeautifulSoup(page.content, "lxml")
    return soup


def divToInfos(div, game):
    div = str(div)
    '''
    <div class="row no-gutters" id="productRow268932"><div class="d-none col">18</div><div class="col-icon"><span class="fonticon-camera" data-html="true" data-placement="bottom" 
    data-toggle="tooltip" title='&lt;img src="//static.cardmarket.com/img/fc9dcfa18684f693732be140b591f309/items/5/MP14/268932.jpg" 
    alt="Number 101: Silent Honor ARK" width="251" height="367"&gt;'></span></div><div class="col-icon small"><a class="expansion-symbol is-yugioh is-text yugiohExpansionIcon"
     data-html="true" data-placement="bottom" data-toggle="tooltip" href="/en/YuGiOh/Expansions/2014-MegaTins-MegaPack" 
     title="2014 Mega-Tins Mega-Pack"><span>MP14</span></a></div><div class="col"><div class="row no-gutters">
     <div class="col-10 col-md-8 px-2 flex-column align-items-start justify-content-center
     "><a href="/en/YuGiOh/Products/Singles/2014-MegaTins-MegaPack/Number-101-Silent-Honor-ARK">Number 101: Silent Honor ARK</a></div>
     <div class="col-md-2 d-none d-lg-flex has-content-centered">219</div><div class="col-sm-2 d-none d-sm-flex has-content-centered"><span class="d-none d-md-flex">
     <span class="icon" data-html="true" data-original-title="Ultra Rare" data-placement="bottom" data-toggle="tooltip" onmouseout="hideMsgBox()" 
     onmouseover="showMsgBox(this,`Ultra Rare`)" style="display: inline-block; width: 16px; height: 16px; background-image: 
     url('//static.cardmarket.com/img/2ebd68b4c57fac1ddc5d2b4a3fc530f4/spriteSheets/ssRarity/ssRarity3.png'); background-position: -208px -0px;" 
     title="Ultra Rare"></span></span></div></div></div><div class="col-availability px-2"><span class="d-none d-md-inline">188</span></div><div class="col-price pr-sm-2">0,50 €</div></div>
    '''# Keeping this for debug purpose
    # print("-------")

    url_and_name_dirty = re.findall(r'"><a href="(.*?)</a>', div)[0]
    url_and_name_splitted = url_and_name_dirty.split('">')
    url = url_and_name_splitted[0]
    url = "https://www.cardmarket.com" + url
    name = url_and_name_splitted[1]
    if game != "YuGiOh":
        expansions = 0
    else:
        expansions = re.findall(r'<span>(.*?)</span>', div)[0]

    num = re.findall(r'has-content-centered">(.*?)</div><div', div)[0]

    rarity = re.findall(r'data-original-title="(.*?)" data-placement', div)[0]
    return [expansions, num, name, rarity, 0, 0, 0, 0,  url]
    # print(expansions, url, name, num, rarity)


def urlScrape(url, signals):
    result = []
    soup = request_block(url)
    all_divs_of_cards = []
    pages = soup.find_all("span", class_="mx-1")
    game = "YuGiOh"
    if "/Pokemon/" in url :
        game = "Pokemon"
    elif "/YuGiOh/" in url:
        game = "YuGiOh"
    elif "/Magic/" in url :
        game = "Magic"

    last_argument = url.split('/')[-1]
    separator = '?'
    if '?' in last_argument:
        separator = '&'

    # base_url = re.sub('(\?site=[0-9]*)', r'?', url)
    # base_url = re.sub('(&site=[0-9]*)', r'', base_url)
    # print("url : ", url, "\nbase url : ", base_url)
    str_page = str(pages[0].encode_contents())
    num_page = int(str_page.split(' ')[-1][:-1])
    if num_page == 15:
        print("[Info] - Max number of pages (15), filler_list might be incomplete.")
    signals.progress.emit(0)
    for i in range(1, num_page + 1):
        # current_url = url + separator + "site=" + str(i)
        if "site=" in url :
            current_url = re.sub("site=[0-9]*","site={}".format(i),url)
        else :
            current_url = url+separator+"site="+str(i)

        current_soup = request_block(current_url)
        links = current_soup.find_all('div', class_='row no-gutters')
        print("-----------")
        print(current_url)
        for elem in links:
            if 'class="col-icon small"' in str(elem):
                result.append(divToInfos(elem, game))
                all_divs_of_cards.append(elem)
        progress_value = int(float(i)/float(num_page) * 100)
        signals.progress.emit(progress_value)
    # for e in all_divs_of_cards:
    #     print(e)
    signals.end.emit(True)
    return sorted(result, key=lambda x: x[1])
