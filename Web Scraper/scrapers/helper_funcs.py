import datetime

from .constants import *


def contest_to_json(contest_name, datetime_obj, platform, contest_link):
    res = "{"
    contest_start = datetime_obj.astimezone(istTZObject).strftime("%d %b, %Y %I:%M %p")

    current_time = datetime.datetime.now()
    current_time = current_time.replace(tzinfo=istTZObject)
    difference = datetime_obj - current_time
    hours = difference.total_seconds() / 3600

    res += '"head": '
    res += '"NEXT ' + platform.upper() + ' CONTEST"'
    res += ', "time": '
    res += '"' + contest_start + '"'
    res += ', "name": '
    res += '"' + contest_name + '"'
    res += ', "high_priority": '
    if hours <= priority_hours:
        res += "true"
    else:
        res += "false"
    res += ', "link": '
    res += '"' + contest_link + '"'
    res += "}"
    return res
