import time, urllib

from selenium import webdriver
from bs4 import BeautifulSoup
from . import helper_funcs
from .constants import *


def fetch():
    base = "https://www.codechef.com"
    URL = "https://www.codechef.com/contests"

    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(5)

    html = driver.page_source
    with open("../out.txt", "w") as f:
        f.write(html)

    driver.close()

    soup = BeautifulSoup(html, "html.parser")
    upcoming_contests = soup.find_all("div", class_="_table__container_1c9os_331 _dark_1c9os_272")[1]
    next_contest = upcoming_contests.find("tbody").find("tr")
    td_tags = next_contest.find_all("td")
    contest_name = td_tags[1].find_all("div")[1].string
    contest_link = td_tags[1].find("a")["href"]
    temp_soup = td_tags[2].find_all("div")[1].find_all("p")
    datetime_obj = datetime.datetime.strptime(
        temp_soup[0].string + " " + temp_soup[1].string, "%d %b %Y %a %H:%M"
    ).replace(tzinfo=istTZObject)

    return helper_funcs.contest_to_json(
        contest_name, datetime_obj, "codechef", urllib.parse.urljoin(base, contest_link)
    )
