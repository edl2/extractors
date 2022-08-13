from ..models.Extractor import Extractor
from ..models.Link import Link

class NineC9Media(Extractor):
    def __init__(self) -> None:
        self.domains = [".+9c9media.com", ".+9c9media.akamaized.net"]
        self.domains_regex = True
    
    def get_link(self, url):
        return Link(address=url, is_widevine=True, license_url="https://mvplicense.9c9media.ca/widevine||R{SSM}|")