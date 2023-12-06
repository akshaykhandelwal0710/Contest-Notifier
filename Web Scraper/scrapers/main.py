from . import codeforces_scraper, atcoder_scraper, codechef_scraper


def get_contests():
    result = "["

    result += codeforces_scraper.fetch()
    result += ", "
    result += atcoder_scraper.fetch()
    result += ", "
    result += codechef_scraper.fetch()

    result += "]"

    return result
