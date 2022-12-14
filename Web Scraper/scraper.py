import requests, datetime, urllib.parse, time
from bs4 import BeautifulSoup
from selenium import webdriver

priority_hours = 24

utcTimeDelta = datetime.timedelta(hours = 0)
utcTZObject = datetime.timezone(utcTimeDelta, name = "UTC")

cfTimeDelta = datetime.timedelta(hours = 3)
cfTZObject = datetime.timezone(cfTimeDelta, name = "CF")

istTimeDelta = datetime.timedelta(hours = 5, minutes = 30)
istTZObject = datetime.timezone(istTimeDelta, name = "IST")

def contest_to_json(contest_name, datetime_obj, platform, contest_link):
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
  res += ", \"link\": "
  res += "\"" + contest_link + "\""
  res += "}"
  return res

def get_contests():
  result = "["

  # Codeforces
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
  contest_start = next_contest.find(class_ = "format-time").string.strip()
  datetime_obj = datetime.datetime.strptime(contest_start, "%b/%d/%Y %H:%M").replace(tzinfo = cfTZObject)
  result += contest_to_json(contest_name, datetime_obj, "codeforces", urllib.parse.urljoin(base, URL))

  #Atcoder
  base = "https://atcoder.jp"
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
  result += contest_to_json(contest_name, datetime_obj, "atcoder", urllib.parse.urljoin(base, a_tags[1]['href']))

  #Codechef
  base = "https://www.codechef.com"
  URL = "https://www.codechef.com/contests"

  driver = webdriver.Chrome('./chromedriver')
  driver.get(URL)

  time.sleep(5)

  html = driver.page_source

  driver.close()

  soup = BeautifulSoup(html, "html.parser")
  upcoming_contests = soup.find_all("div", class_ = "_table__container_jhph2_249")[1]
  next_contest = upcoming_contests.find("tbody").find("tr")
  td_tags = next_contest.find_all("td")
  contest_name = td_tags[1].find_all("div")[1].string
  contest_link = td_tags[1].find("a")['href']
  temp_soup = td_tags[2].find_all("div")[1].find_all("p")
  datetime_obj = datetime.datetime.strptime(temp_soup[0].string + " " + temp_soup[1].string, "%d %b %Y %a %H:%M").replace(tzinfo = istTZObject)
  result += ", "
  result += contest_to_json(contest_name, datetime_obj, "codechef", urllib.parse.urljoin(base, contest_link))

  result += "]"
  return result