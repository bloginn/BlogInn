# encoding: utf-8
from cook.common.Curl import Curl
from bs4 import BeautifulSoup

request_res = Curl().get('https://baike.baidu.com/item/%E6%80%BB')
if request_res['status'] == 200:
    body = request_res['body']

    soup = BeautifulSoup(body, "html5lib")  # pip install html5lib
    names = soup.find_all("dt", class_="basicInfo-item name")

    values = soup.find_all("dd", class_="basicInfo-item value")

    value_list = [[]]
    if len(names) == len(values):
        for index, name in enumerate(names):
            value_list[index]['name'] = name.get_text().replace(u'\xa0', '')

    print value_list
