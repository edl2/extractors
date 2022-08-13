import re, requests, base64

from ..models.Link import Link
from ..util import jsunpack
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"

def scan(html):
    res = None
    r = re.findall(r"source src=\"(.+?\.m3u8)\"", html)
    r_var = re.findall(r"var source.?=.?(?:\"|')(.+?)(?:\"|')", html)
    r2 = re.findall(r"source\s*:\s+?(?:\"|')(.+?)(?:\"|')", html)
    r3 = re.findall(r"(?:\"|')(http.*?\.m3u8.*?)(?:\"|')", html)
    r_b64 = re.findall(r"atob\((?:\"|')(aHR.+?)(?:\"|')", html)
    re_packed = re.findall(r"(eval\(function\(p,a,c,k,e,d\).+?{}\)\))", html)
    if len(r) > 0: res = r[0]
    elif len(r_var) > 0:
        for match in r_var:
            if ".m3u8" in match: 
                res = match
                break
    elif len(r2) > 0:
        for match in r2:
            if ".m3u8" in match: 
                res = match
                break
    elif len(r3) > 0:
        for match in r3:
            if ".m3u8" in match:
                res = match
                break
    elif len(r_b64) > 0:
        for match in r_b64:
            b64 = base64.b64decode(match).decode("ascii")
            if ".m3u8" in b64: res = b64
    elif len(re_packed) > 0:
        packed = jsunpack.unpack(re_packed[0])
        res = scan(packed)
    return res

def scan_page(url, html=None, headers={}) -> Link:
    if headers == {}: headers["User-Agent"] = user_agent
    if html == None: html = requests.get(url, headers=headers).text
    url = url.replace("&", "_")
    res = scan(html)
    
    if type(res) == str:
        if res.startswith("//"): res = ("https:" if url.startswith("https") else "http:") + res
    
    link = Link(address=res, headers={"Referer": url, "User-Agent": user_agent} if "aces2" not in url else {}) if res is not None else None
    if link != None:
        if "Referer" in link.headers and "xestreams.com" in link.headers["Referer"]:
            link.headers["Referer"] = "http://xestreams.com/"
            link.headers["Origin"] = "http://xestreams.com"
        
    return link