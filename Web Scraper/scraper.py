import requests, datetime
from bs4 import BeautifulSoup

utcTimeDelta = datetime.timedelta(hours = 0)
utcTZObject = datetime.timezone(utcTimeDelta, name = "UTC")

cfTimeDelta = datetime.timedelta(hours = 3)
cfTZObject = datetime.timezone(cfTimeDelta, name = "CF")

istTimeDelta = datetime.timedelta(hours = 5, minutes = 30)
istTZObject = datetime.timezone(istTimeDelta, name = "IST")

def print_contest(contest_name, datetime_obj, platform):
  res = "\n"
  contest_start = datetime_obj.astimezone(istTZObject).strftime("%d %b, %Y %I:%M %p")

  res += "NEXT " + platform.upper() + " CONTEST:\n"
  res += contest_start + '\t' + contest_name + "\n"
  res += "\n"
  return res

def get_contests():
  result = ""

  # Codeforces
  URL = "https://codeforces.com/contests"
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")

  tables = soup.find_all("table")
  upcoming_contests = tables[0]
  table_rows = upcoming_contests.find_all("tr")
  next_contest = table_rows[1]
  fields = next_contest.find_all("td")
  contest_name = fields[0].string.strip()
  contest_start = next_contest.find(class_ = "format-time").string.strip()
  datetime_obj = datetime.datetime.strptime(contest_start, "%b/%d/%Y %H:%M").replace(tzinfo = cfTZObject)
  result += print_contest(contest_name, datetime_obj, "codeforces")

  #Atcoder
  URL = "https://atcoder.jp/contests/"
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")

  upcoming_contests = soup.find(id = "contest-table-upcoming").find("tbody")
  table_rows = upcoming_contests.find_all("tr")
  next_contest = table_rows[0]
  a_tags = next_contest.find_all("a")
  contest_name = a_tags[1].string
  datetime_obj = datetime.datetime.strptime(a_tags[0].string, "%Y-%m-%d %H:%M:%S%z")
  result += print_contest(contest_name, datetime_obj, "atcoder")

  print(result)
  return result