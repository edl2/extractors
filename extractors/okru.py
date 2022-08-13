import requests, re, json, html

from ..models.Extractor import Extractor
from ..models.Link import Link

class OkRu(Extractor):
    def __init__(self) -> None:
        self.domains = ["ok.ru"]

    def get_link(self, url):
        r_embed = requests.get(url, headers={"User-Agent": self.user_agent}).text
        embed_json = json.loads(html.unescape(re.compile(r'data-options="(.+?)"').findall(r_embed)[0]))
        metadata_json = json.loads(embed_json["flashvars"]["metadata"])
        return Link(address=metadata_json["hlsManifestUrl"] if "hlsManifestUrl" in metadata_json else metadata_json["hlsMasterPlaylistUrl"], headers={"User-Agent": self.user_agent})