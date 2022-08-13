import requests

from ..models.Extractor import Extractor
from urllib.parse import quote
from ..models.Game import Game
from ..util.keys import Keys
from ..models.Link import Link

# https://github.com/d21spike/plugin.video.sling/blob/master/resources/lib/sling.py
ANDROID_USER_AGENT = 'SlingTV/6.17.9 (Linux;Android 10) ExoPlayerLib/2.7.1'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/69.0.3497.100 Safari/537.36'
HEADERS = {'Accept': '*/*',
    'Origin': 'https://www.sling.com',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.sling.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'}
VERIFY = True

class Sling(Extractor):
    def __init__(self) -> None:
        self.domains = [".+movetv.com"]
        self.domains_regex = True
        self.name = "Sling"
        self.short_name = "SLING"

    def get_playlist(self, playlist_url):
        response = requests.get(playlist_url, headers=HEADERS, verify=VERIFY)
        if response is not None and response.status_code == 200:
            video = response.json()

            if video is None or 'message' in video: return
            if 'playback_info' not in video: return
            mpd_url = video["playback_info"]["dash_manifest_url"]
            for clip in video['playback_info']['clips']:
                if clip['location'] != '':
                    qmx_url = clip['location']
                    break
            if "UNKNOWN" not in mpd_url:
                response = requests.get(qmx_url, headers=HEADERS, verify=VERIFY)
                if response is not None and response.status_code == 200:
                    qmx = response.json()
                    if 'message' in qmx: return
                    lic_url = ''
                    if 'encryption' in qmx:
                        lic_url = qmx['encryption']['providers']['widevine']['proxy_url']

                    if 'playback_info' in playlist_url:
                        channel_id = playlist_url.split('/')[-4]
                    else:
                        channel_id = playlist_url.split('/')[-2]
                        if 'channel=' in playlist_url:
                            channel_id = playlist_url.split('?')[-1].split('=')[-1]                        

                    if lic_url != '':
                        key = Keys.get_key(Keys.sling)
                        payload = '{"channel_id": "%s", "env": "production", "message": [D{SSM}], "user_id": "%s"}' % (key["channel_id"], key["user_id"])
                        license_key = '%s|Content-Type=text/plain&User-Agent=%s|%s|' % ("https://p-drmwv.movetv.com/widevine/proxy", USER_AGENT, quote(payload))
        asset_id = ''
        if 'entitlement' in video and 'asset_id' in video['entitlement']:
            asset_id = video['entitlement']['asset_id']
        elif 'playback_info' in video and 'asset' in video['playback_info'] and 'guid' in video['playback_info']['asset']:
            asset_id = video['playback_info']['asset']['guid']
        start_time = video["playback_info"]["linear_info"]["anchor_time"]

        return mpd_url.replace("http://", "https://"), license_key, asset_id, start_time

    def get_channel_info(self, channel_id):
        r = requests.get("https://vip.sports24.club/bm/channels.json?1611060042", headers={"User-Agent": USER_AGENT}).json()
        for channel in r:
            if channel["guid"] == channel_id:
                return channel

    def get_games(self):
        games = []
        r = requests.get("https://cbd46b77.cdn.cms.movetv.com/cms/publish3/domain/summary/ums/1.json", headers={"User-Agent": USER_AGENT}).json()
        for channel in r["channels"]:
            if not channel["visibility"]["visible"]: continue
            # if channel["title"] not in include: continue
            games.append(Game(title=channel["metadata"]["channel_name"], league=channel["title"], icon=channel["metadata"]["thumbnail_cropped"]["url"] if "thumbnail_cropped" in channel["metadata"] else "", links=[Link(channel["qvt_url"])]))
        games = list(sorted(games, key=lambda x: x.title))
        return games

    def get_link(self, url):
        mpd_url, license_url, _, start_time = self.get_playlist(url)
        return Link(address=mpd_url, is_widevine=True, license_url=license_url)