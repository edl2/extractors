from datetime import datetime
from typing import List, Optional
from .Link import Link

class Game:
    title: Optional[str]
    links: Optional[List[Link]]
    starttime: Optional[datetime]
    status: Optional[str]
    league: Optional[str]
    icon: Optional[str]
    extractor: Optional[str]

    def __init__(self, title: Optional[str] = None, links: Optional[List[Link]] = [], starttime: Optional[datetime] = None, status: Optional[str] = None, league: Optional[str] = None, icon: Optional[str] = "", extractor: Optional[str] = None) -> None:
        self.title = title
        self.links = links
        self.starttime = starttime
        self.status = status
        self.league = league
        self.icon = icon
        self.extractor = extractor
