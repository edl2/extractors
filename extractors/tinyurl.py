
import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util import hunter
from urllib.parse import unquote


class Tinyurl(Extractor):
    def __init__(self) -> None:
        self.domains = ["tinyurl.is"]
        self.shortener = True

    # def get_link(self, url):
    #     r = requests.get(url).text
    #     re_hunter = re.compile(r'decodeURIComponent\(escape\(r\)\)}\("(.+?)",(.+?),"(.+?)",(.+?),(.+?),(.+?)\)').findall(r)[0]
    #     deobfus = hunter.hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
    #     link = re.findall(r'\.attr\(\"href\",\"(.+?)\"', deobfus)[1]
    #     return Link(link)
    
    # def get_link(self, url):
    #     r = requests.get(url).text
    #     link = re.findall(r'\.attr\(\"href\",\"(.+?)\"', r)[1]
    #     return Link(link)

    def __dF(self, s):
        s1 = unquote(s[0:len(s) - 1])
        t = ""
        for i in range(len(s1)):
            t += chr(ord(s1[i]) - int(s[-1]))
        return unquote(t)

    def get_link(self, url):
        r = requests.get(url).text
        re_df = re.findall(r"dF\('(.+?)'\)", r)[0]
        df = self.__dF(re_df)
        link = re.findall(r'\.attr\(\"href\",\"(.+?)\"', df)[1]
        return Link(link)