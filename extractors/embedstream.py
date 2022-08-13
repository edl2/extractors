import requests, re

from ..models.Extractor import Extractor
from .plytv import PlyTv

class Embedstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["embedstream.me"]
        self.name = "Embedstream"

    def embedstream(self, id):
        r_embedstream = requests.get("https://embedstream.me/" + id).text
        re_zmid = re.compile(r'zmid = "(.+?)"').findall(r_embedstream)
        if len(re_zmid) == 0:
            v_vpp = re.compile(r'v_vpp="(.+?)"').findall(r_embedstream)[0]
            v_vid = re.compile(r'v_vid="(.+?)"').findall(r_embedstream)[0]
            v_vpv = re.compile(r'v_vpv="(.+?)"').findall(r_embedstream)[0]
            return PlyTv().plytv_sdembed(f"https://www.plylive.me/hdembed?p={v_vpp}&id={v_vid}&v={v_vpv}", "https://embedstream.me/")
        else:
            return PlyTv().plytv_sdembed(re_zmid[0], "https://embedstream.me/")

    def get_link(self, url):
        return self.embedstream(url.replace("https://embedstream.me/", ""))