import requests, re
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..scanners.m3u8_src import scan_page

class Crackstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["crackstreams.biz"]
        self.name = "Crackstreams"
        self.short_name = "CS"
    
    # def get_link(self, url):
    #     request = requests.Session()
    #     request.cookies.set("challenge", "BitMitigate.com", domain="crackstreams.net", path="/")
    #     m3u8 = ""
    #     video_html = request.get(url).text
    #     video = BeautifulSoup(video_html, "html.parser")
    #     stream_url = video.find_all("iframe")[0].get("src")
    #     stream_html = requests.get(stream_url, headers={"Referer": url}).text
    #     soup_stream = BeautifulSoup(stream_html, "html.parser")
    #     m3u8 = Link()
    #     if len(soup_stream.find_all("iframe")) > 0:
    #         iframe = soup_stream.find("iframe").get("src")
    #         r_iframe = requests.get(iframe).text
    #         m3u8.address = re.compile(r"source: '(.+?)'").findall(r_iframe)[0]
    #     else:
    #         m3u8 = scan_page(url, video_html)    
    #     if "hdstreamss" in m3u8:
    #         m3u8.headers = {"Referer": "http://hdstreamss.club/"}
    #     return m3u8
    def get_link(self, url):
        m3u8 = ""
        video_html = requests.get(url).text
        video = BeautifulSoup(video_html, "html.parser")
        if len(video.find_all("iframe")) > 0:
            iframe = video.find("iframe").get("src")
            r_iframe = requests.get(iframe).text
            m3u8 = Link(address=re.compile(r"source: '(.+?)'").findall(r_iframe)[0])
        else:
            m3u8 = scan_page(url, video_html)    
        # if "hdstreamss" in m3u8.address:
        #     m3u8.headers = {"Referer": "http://hdstreamss.club/"}
        # else:
        #     m3u8.headers = {"Referer": "http://crackstreams.biz/"}
        return m3u8

    # def get_games(self):
    #     games = []
    #     base_url = "http://crackstreams.biz"
    #     request = requests.Session()
    #     request.cookies.set("challenge", "BitMitigate.com", domain="crackstreams.net", path="/")
    #     r = request.get(base_url).text
    #     soup = BeautifulSoup(r, "html.parser")
    #     categories = soup.select("ul.nav > li > a")
    #     for category in categories:
    #         league = category.text.replace(" streams", "")
    #         league_href = base_url + category.get("href")
    #         r_league = request.get(league_href).text
    #         soup_league = BeautifulSoup(r_league, "html.parser")
    #         for body in soup_league.find_all("a", {"class": "btn-block"}):
    #             href = base_url + body.get("href") if body.get("href").startswith("/") else body.get("href")
    #             icon = "-"
    #             title = body.find("h4").text.strip()
    #             time = body.find("p").text
    #             if "Stream" in time:
    #                 continue
    #             utc_time = None
    #             if time != "":
    #                 try:
    #                     utc_time = parse(time) + timedelta(hours=4)
    #                 except:
    #                     pass
    #             games.append(Game(title=title, links=[Link(address=href)], icon=icon, league=league, starttime=utc_time))
    #     return games
    def get_games(self):
        games = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul#primary-menu > li > a")[1:]
        for category in categories:
            league = category.text.replace(" streams", "")
            league_href = category.get("href")
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for body in soup_league.find_all("a", {"class": "btn-block"}):
                href = body.get("href")
                title = body.find("h4").text.strip()
                time = body.find("p").text
                if "Stream" in time:
                    continue
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=4)
                    except:
                        pass
                games.append(Game(title=title, links=[Link(address=href)], icon="-", league=league, starttime=utc_time))
        return games
