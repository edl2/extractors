from typing import List
from .Game import Game
from .Link import Link

class Extractor:
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    domains: List[str] = []
    domains_regex: bool = False
    name: str = None
    short_name: str = None
    shortener: bool = False
    subclasses = []
    disabled = False

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def get_games(self) -> List[Game]:
        return []
    
    def get_link(self, url: str) -> Link:
        if ".m3u8" in url or url.startswith("direct://"):
            return url
        return None
    
    def get_links(self, url: str) -> List[Link]:
        return []