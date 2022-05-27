from re import search as re_search
from urllib.parse import parse_qs, urlparse


def parse_gd_link(link):
    if "folders" in link or "file" in link:
        regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
        res = re_search(regex,link)
        if res is None:
            return None
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)['id'][0]
