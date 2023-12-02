import requests, datetime, urllib

from bs4 import BeautifulSoup
from . import helper_funcs
from .constants import *


def fetch():
    base = "https://codeforces.com"
    URL = "https://codeforces.com/contests"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    tables = soup.find_all("table")
    upcoming_contests = tables[0]
    table_rows = upcoming_contests.find_all("tr")
    next_contest = table_rows[1]
    fields = next_contest.find_all("td")
    contest_name = fields[0].string.strip()
    contest_start = next_contest.find(class_="format-time").string.strip()
    datetime_obj = datetime.datetime.strptime(contest_start, "%b/%d/%Y %H:%M").replace(
        tzinfo=cfTZObject
    )

    return helper_funcs.contest_to_json(
        contest_name, datetime_obj, "codeforces", urllib.parse.urljoin(base, URL)
    )
