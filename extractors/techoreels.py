import requests, re
from ..models.Extractor import Extractor
from ..models.Link import Link

class Techoreels(Extractor):
    def __init__(self) -> None:
        self.domains = ["techoreels.com"]

    def get_link(self, url):
        r = requests.get(url).text
        servers = re.findall(r'var servs = (\[.+?\]);', r)
        if len(servers) > 0:
            servers = eval(servers[0])
            stream_id = re.findall(r"source: '' \+ serv \+ '(.*?)'", r)[0]
            for server in servers:
                stream = server + stream_id
                r_stream = requests.get(stream)
                if r_stream.status_code == 200:
                    return Link(address=stream)
        else:
            iframe = re.findall(r'iframe src="(.+?)"', r)[0]
            r_iframe = requests.get(iframe).text
            servers = eval(re.findall(r'var servs = (\[.+?\]);', r_iframe)[0])
            stream_id = re.findall(r"source: '' \+ serv \+ '(.*?)'", r_iframe)[0]
            for server in servers:
                stream = server + stream_id
                r_stream = requests.get(stream, headers={"Referer": iframe})
                if r_stream.status_code == 200:
                    return Link(address=stream, headers={"Referer": iframe})