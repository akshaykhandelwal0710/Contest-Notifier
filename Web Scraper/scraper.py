import requests, datetime
from bs4 import BeautifulSoup

priority_hours = 24

utcTimeDelta = datetime.timedelta(hours = 0)
utcTZObject = datetime.timezone(utcTimeDelta, name = "UTC")

cfTimeDelta = datetime.timedelta(hours = 3)
cfTZObject = datetime.timezone(cfTimeDelta, name = "CF")

istTimeDelta = datetime.timedelta(hours = 5, minutes = 30)
istTZObject = datetime.timezone(istTimeDelta, name = "IST")

def contest_to_json(contest_name, datetime_obj, platform):
  res = "{"
  contest_start = datetime_obj.astimezone(istTZObject).strftime("%d %b, %Y %I:%M %p")

  current_time = datetime.datetime.now()
  current_time = current_time.replace(tzinfo = istTZObject)
  difference = datetime_obj - current_time
  hours = difference.total_seconds() / 3600

  res += "\"head\": "
  res += "\"NEXT " + platform.upper() + " CONTEST\""
  res += ", \"time\": "
  res += "\"" + contest_start + "\""
  res += ", \"name\": "
  res += "\"" + contest_name + "\""
  res += ", \"high_priority\": "
  if hours <= priority_hours:
    res += "true"
  else:
    res += "false"
  res += "}"
  return res

def get_contests():
  result = "["

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
  result += contest_to_json(contest_name, datetime_obj, "codeforces")

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
  result += ", "
  result += contest_to_json(contest_name, datetime_obj, "atcoder")

  result += "]"
  print(result)
  return result