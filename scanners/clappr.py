import re, requests, base64

def scan_page(url, html=None):
    if html == None: html = requests.get(url).text
    r = re.findall(r"Clappr[\s\S]+source:.+?(?:\"|')(.+?)(?:\"|'),", html)
    r_b64 = re.findall(r"Clappr.+?(?:\n?).+?e:(?:.+?)atob\((?:\"|')(.+?)(?:\"|')\)", html)
    if len(r) > 0: return r[0] + "|Referer=" + url
    elif len(r_b64) > 0: return base64.b64decode(r_b64[0]).decode("ascii") + "|Referer=" + url