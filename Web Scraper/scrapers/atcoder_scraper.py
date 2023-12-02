import requests, urllib

from . import helper_funcs
from bs4 import BeautifulSoup
from .constants import *


def fetch():
    base = "https://atcoder.jp"
    URL = "https://atcoder.jp/contests/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    upcoming_contests = soup.find(id="contest-table-upcoming").find("tbody")
    table_rows = upcoming_contests.find_all("tr")
    next_contest = table_rows[0]
    a_tags = next_contest.find_all("a")
    contest_name = a_tags[1].string
    datetime_obj = datetime.datetime.strptime(a_tags[0].string, "%Y-%m-%d %H:%M:%S%z")

    return helper_funcs.contest_to_json(
        contest_name,
        datetime_obj,
        "atcoder",
        urllib.parse.urljoin(base, a_tags[1]["href"]),
    )
