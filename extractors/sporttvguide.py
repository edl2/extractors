from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game
import requests, datetime, re, xbmc, base64
from bs4 import BeautifulSoup
from ..external.airtable.airtable import Airtable

class SportTVGuide(Extractor):
    def __init__(self) -> None:
        self.name = "SportTVGuide"
        self.username = base64.b64decode("ampqZXQ3MUB5YWhvby5jb20=").decode("utf-8")
        self.password = base64.b64decode("amV0c3BvcnR0dg==").decode("utf-8")
        self.days = 2
    
    def get_games(self):
        games = []

        # Get channels from Airtable
        channels_table = Airtable("appE6mAL3izoxgdp7", "SPORT_CHANNELS", api_key="keyvWT1TdSyCaibez")
        m3u8_table = Airtable("appE6mAL3izoxgdp7", "IPTVmine1", api_key="keyvWT1TdSyCaibez")

        channels_records = channels_table.get_all()
        m3u8_records = m3u8_table.get_all()

        m3u8s = {}
        for m3u8_record in m3u8_records:
            record_id = m3u8_record["id"]
            fields = m3u8_record["fields"]
            urls = []
            if "SERVER2" in fields and "://" in fields["SERVER2"]: urls.append(Link(fields["SERVER2"].strip()))
            if "SERVER" in fields and "://" in fields["SERVER"]: urls.append(Link(fields["SERVER"], jetproxy=True))
            if "IPTVCAT" in fields and "://" in fields["IPTVCAT"]: urls.append(Link(fields["IPTVCAT"]))
            # for i in range(1, 5):
            #     if "link" + str(i) in fields:
            #         url = fields["link" + str(i)]
            #         if "://" in url: urls.append(unidecode(url))
            m3u8s[record_id] = urls

        channels = {}
        for record in channels_records:
            fields = record["fields"]
            if "label2" in fields:
                label = fields["label2"]
                urls = []
                if "url" in fields and fields["url"] != "-": urls.append(Link(fields["url"].strip()))
                if "url2" in fields and fields["url2"] != "-": urls.append(Link(fields["url2"].strip()))
                if "url3" in fields and fields["url3"] != "-": urls.append(Link(fields["url3"].strip()))
                if "link1" in fields and fields["link1"] != "-": urls.append(Link(fields["link1"].strip()))
                if "IPTVmine1" in fields and fields["IPTVmine1"] != "-":
                    for record_id in fields["IPTVmine1"]: urls.extend(m3u8s[record_id])
                # if "IPTVCAT" in fields and fields["IPTVCAT"] != "-":
                # for record_id in fields["IPTVCAT"]: urls.extend(m3u8s[record_id])
                channels[label] = urls

        # Get session cookies
        s = requests.Session()
        s.get("https://sport-tv-guide.live")
        s.post("https://sport-tv-guide.live/user/login/", data=f"email={self.username}&password={self.password}", headers={"content-type": "application/x-www-form-urlencoded"})
        s.get("https://sport-tv-guide.live/live/allsports")

        missing_channels = []

        # Get games
        for day in range(self.days):
            s.post("https://sport-tv-guide.live/ajaxdata/selectdate", data="d=" + (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d"), headers={"content-type": "application/x-www-form-urlencoded"})
            i = 0
            page = 0
            r = {"last": False}
            
            while not r["last"]:
                r = s.post("https://sport-tv-guide.live/ajaxdata/nextlistpage", data=f"l=0&p={page}&c=-1&t=99&d=&x=0", headers={"content-type": "application/x-www-form-urlencoded", "x-requested-with": "XMLHttpRequest"})
                r = r.json()
                page = r["page"]
                soup = BeautifulSoup(r["data"], "html.parser")
                for game in soup.select("div.row"):
                    game_title = game.select_one("div.col-inline").text.strip()
                    if "\n" in game_title:
                        game_title_split = game_title.split("\n")
                        game_title = f"{game_title_split[0]} ({game_title_split[1]})"
                    game_type = game.select_one("div.typeName").text
                    game_time = game.select_one("div.time").contents[3].text.split(":")
                    game_utc = (datetime.datetime.now() + datetime.timedelta(days=day)).replace(hour=int(game_time[0]), minute=int(game_time[1][:2]), second=0, microsecond=0) - datetime.timedelta(hours=int(dict(s.cookies)["user_time_zone_id"]))
                    game_icon = game.select_one("img#img-inline")

                    exists = False
                    for g in games:
                        if g.title == game_title and g.starttime == game_utc:
                            exists = True
                            break
                    if exists: continue

                    links = []
                    tv_coverage = [channel.get("title") for channel in game.select("img.floatRight")]
                    for channel in tv_coverage:
                        channel = channel.replace(" []", "")
                        try: links += channels[channel]
                        except: 
                            if channel not in missing_channels:
                                missing_channels.append(channel)
                            continue
                    if links == []: continue

                    games.append(Game(title=game_title, links=links, starttime=game_utc, league=game_type, icon=game_icon.get("data-src") if game_icon != None else ""))
                i += 1
                # if i == 10: break
        if len(missing_channels) > 0:
            xbmc.log("[jetextractors.sporttvguide] missing channels: " + ", ".join(missing_channels), xbmc.LOGINFO)
        return games