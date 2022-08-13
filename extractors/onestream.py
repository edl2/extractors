import requests, re, base64
from ..models.Extractor import Extractor
from ..models.Link import Link
from urllib.parse import urlparse
import random

class Onestream(Extractor):
    def __init__(self) -> None:
        self.domains = ["1stream.top"]

    def get_link(self, url):
        path = urlparse(url).path.split("/")[-1] + str(round(random.random() * 12))
        r = requests.get(f"http://{self.domains[0]}/getspurcename?{path}").json()
        link = base64.b64decode(r["source"]).decode("utf-8")
        return Link(link, headers={"Referer": url})
        # r = requests.get(url, headers={"User-Agent": self.user_agent}).text
        # re_b64 = re.findall(r"window\.atob\('(.+?)'\)", r)[0]
        # re_cdn = re.findall(r'const cdn = \["(.+?)"', r)[0]
        # host = base64.b64decode(re_b64).decode("ascii")
        # host = host.replace(host[host.index("/") + 2:].split(".")[0], re_cdn)
        # return Link(address=host.replace("http", "https"), headers={"Referer": url})