#coding=utf-8
import requests
from bs4 import BeautifulSoup

def base_get_soup():
    url = "https://www.seaserpentfleet.com/schedule"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    return res, soup


def base_get_detail(href):
    url = "https://www.seaserpentfleet.com" + href
    print(url)
    res = requests.get(url)
    # print(res.text)
    # print(res.status_code)
    soup = BeautifulSoup(res.text, 'lxml')
    return res, soup

# get_route_menu()