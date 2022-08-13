import requests, base64
from bs4 import BeautifulSoup

from ..models.Link import Link
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344"

def get_streams(match_id, match_sport, origin):
    url = "https://sportscentral.io/streams-table/%s/%s?new-ui=1&origin=%s" % (match_id, match_sport, origin)
    links = get_streams_table(url)
    return links

def get_streams_table(url):
    links = []
    r_streams = requests.get(url, headers={"User-Agent": user_agent, "Referer": "https://nbabite.com"}).text
    soup = BeautifulSoup(r_streams, "html.parser")
    exclude = requests.get(base64.b64decode("aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9NQURfVElUQU5fU1BPUlRTL1NQT1JUUy9TSVRFUy9zaXRlX2V4Y2x1ZGUuanNvbg==").decode("utf-8")).json()
    for stream in soup.select("tbody > tr"):
        href = stream.get("data-stream-link")
        name = stream.select_one("span.first").text.strip()
        if name in exclude:
            continue
        quality = stream.select_one("span.label-purple").text.strip()
        links.append(Link(address=href, name="%s %s" % (name, quality)))
    return links