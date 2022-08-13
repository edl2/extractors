import requests, time, re, json, html
from datetime import datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class FullMatchTV(Extractor):
    def __init__(self) -> None:
        super().__init__()
        self.domains = ["fullmatchtv.com"]
        self.name = "Full Match TV"
        self.short_name = "FMTV"
        self.leagues = {
            "NBA": 3,
            "MLB": 6,
            "NFL": 4,
            "NHL": 5,
            "Motorsports": 973,
            "AFL": 1279,
            "Rugby": 928,
            "WWE & MMA": 989
        }

    def get_games(self):
        games = []
        r = requests.get(
            f"https://{self.domains[0]}/motorsports/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": f"https://{self.domains[0]}/",
                "Origin": f"https://{self.domains[0]}",
                "User-Agent": self.user_agent
            }
        ).text
        magic_token = re.findall(r"var tdBlockNonce=\"(.+?)\";", r)[0]
        for league, code in self.leagues.items():
            td_atts = "%7B%22custom_title%22%3A%22Latest+Rugby+games%22%2C%22category_id%22%3A%22928%22%2C%22limit%22%3A%2218%22%2C%22td_ajax_filter_type%22%3A%22td_category_ids_filter%22%2C%22ajax_pagination%22%3A%22load_more%22%2C%22block_type%22%3A%22td_block_16%22%2C%22separator%22%3A%22%22%2C%22custom_url%22%3A%22%22%2C%22block_template_id%22%3A%22%22%2C%22mx7_tl%22%3A%22%22%2C%22mx7_el%22%3A%22%22%2C%22m6_tl%22%3A%22%22%2C%22post_ids%22%3A%22%22%2C%22category_ids%22%3A%22%22%2C%22tag_slug%22%3A%22%22%2C%22autors_id%22%3A%22%22%2C%22installed_post_types%22%3A%22%22%2C%22sort%22%3A%22%22%2C%22offset%22%3A%22%22%2C%22show_modified_date%22%3A%22%22%2C%22el_class%22%3A%22%22%2C%22td_ajax_filter_ids%22%3A%22%22%2C%22td_filter_default_txt%22%3A%22All%22%2C%22td_ajax_preloading%22%3A%22%22%2C%22f_header_font_header%22%3A%22%22%2C%22f_header_font_title%22%3A%22Block+header%22%2C%22f_header_font_settings%22%3A%22%22%2C%22f_header_font_family%22%3A%22%22%2C%22f_header_font_size%22%3A%22%22%2C%22f_header_font_line_height%22%3A%22%22%2C%22f_header_font_style%22%3A%22%22%2C%22f_header_font_weight%22%3A%22%22%2C%22f_header_font_transform%22%3A%22%22%2C%22f_header_font_spacing%22%3A%22%22%2C%22f_header_%22%3A%22%22%2C%22f_ajax_font_title%22%3A%22Ajax+categories%22%2C%22f_ajax_font_settings%22%3A%22%22%2C%22f_ajax_font_family%22%3A%22%22%2C%22f_ajax_font_size%22%3A%22%22%2C%22f_ajax_font_line_height%22%3A%22%22%2C%22f_ajax_font_style%22%3A%22%22%2C%22f_ajax_font_weight%22%3A%22%22%2C%22f_ajax_font_transform%22%3A%22%22%2C%22f_ajax_font_spacing%22%3A%22%22%2C%22f_ajax_%22%3A%22%22%2C%22f_more_font_title%22%3A%22Load+more+button%22%2C%22f_more_font_settings%22%3A%22%22%2C%22f_more_font_family%22%3A%22%22%2C%22f_more_font_size%22%3A%22%22%2C%22f_more_font_line_height%22%3A%22%22%2C%22f_more_font_style%22%3A%22%22%2C%22f_more_font_weight%22%3A%22%22%2C%22f_more_font_transform%22%3A%22%22%2C%22f_more_font_spacing%22%3A%22%22%2C%22f_more_%22%3A%22%22%2C%22mx7f_title_font_header%22%3A%22%22%2C%22mx7f_title_font_title%22%3A%22Article+title%22%2C%22mx7f_title_font_settings%22%3A%22%22%2C%22mx7f_title_font_family%22%3A%22%22%2C%22mx7f_title_font_size%22%3A%22%22%2C%22mx7f_title_font_line_height%22%3A%22%22%2C%22mx7f_title_font_style%22%3A%22%22%2C%22mx7f_title_font_weight%22%3A%22%22%2C%22mx7f_title_font_transform%22%3A%22%22%2C%22mx7f_title_font_spacing%22%3A%22%22%2C%22mx7f_title_%22%3A%22%22%2C%22mx7f_cat_font_title%22%3A%22Article+category+tag%22%2C%22mx7f_cat_font_settings%22%3A%22%22%2C%22mx7f_cat_font_family%22%3A%22%22%2C%22mx7f_cat_font_size%22%3A%22%22%2C%22mx7f_cat_font_line_height%22%3A%22%22%2C%22mx7f_cat_font_style%22%3A%22%22%2C%22mx7f_cat_font_weight%22%3A%22%22%2C%22mx7f_cat_font_transform%22%3A%22%22%2C%22mx7f_cat_font_spacing%22%3A%22%22%2C%22mx7f_cat_%22%3A%22%22%2C%22mx7f_meta_font_title%22%3A%22Article+meta+info%22%2C%22mx7f_meta_font_settings%22%3A%22%22%2C%22mx7f_meta_font_family%22%3A%22%22%2C%22mx7f_meta_font_size%22%3A%22%22%2C%22mx7f_meta_font_line_height%22%3A%22%22%2C%22mx7f_meta_font_style%22%3A%22%22%2C%22mx7f_meta_font_weight%22%3A%22%22%2C%22mx7f_meta_font_transform%22%3A%22%22%2C%22mx7f_meta_font_spacing%22%3A%22%22%2C%22mx7f_meta_%22%3A%22%22%2C%22mx7f_ex_font_title%22%3A%22Article+excerpt%22%2C%22mx7f_ex_font_settings%22%3A%22%22%2C%22mx7f_ex_font_family%22%3A%22%22%2C%22mx7f_ex_font_size%22%3A%22%22%2C%22mx7f_ex_font_line_height%22%3A%22%22%2C%22mx7f_ex_font_style%22%3A%22%22%2C%22mx7f_ex_font_weight%22%3A%22%22%2C%22mx7f_ex_font_transform%22%3A%22%22%2C%22mx7f_ex_font_spacing%22%3A%22%22%2C%22mx7f_ex_%22%3A%22%22%2C%22m6f_title_font_header%22%3A%22%22%2C%22m6f_title_font_title%22%3A%22Article+title%22%2C%22m6f_title_font_settings%22%3A%22%22%2C%22m6f_title_font_family%22%3A%22%22%2C%22m6f_title_font_size%22%3A%22%22%2C%22m6f_title_font_line_height%22%3A%22%22%2C%22m6f_title_font_style%22%3A%22%22%2C%22m6f_title_font_weight%22%3A%22%22%2C%22m6f_title_font_transform%22%3A%22%22%2C%22m6f_title_font_spacing%22%3A%22%22%2C%22m6f_title_%22%3A%22%22%2C%22m6f_cat_font_title%22%3A%22Article+category+tag%22%2C%22m6f_cat_font_settings%22%3A%22%22%2C%22m6f_cat_font_family%22%3A%22%22%2C%22m6f_cat_font_size%22%3A%22%22%2C%22m6f_cat_font_line_height%22%3A%22%22%2C%22m6f_cat_font_style%22%3A%22%22%2C%22m6f_cat_font_weight%22%3A%22%22%2C%22m6f_cat_font_transform%22%3A%22%22%2C%22m6f_cat_font_spacing%22%3A%22%22%2C%22m6f_cat_%22%3A%22%22%2C%22m6f_meta_font_title%22%3A%22Article+meta+info%22%2C%22m6f_meta_font_settings%22%3A%22%22%2C%22m6f_meta_font_family%22%3A%22%22%2C%22m6f_meta_font_size%22%3A%22%22%2C%22m6f_meta_font_line_height%22%3A%22%22%2C%22m6f_meta_font_style%22%3A%22%22%2C%22m6f_meta_font_weight%22%3A%22%22%2C%22m6f_meta_font_transform%22%3A%22%22%2C%22m6f_meta_font_spacing%22%3A%22%22%2C%22m6f_meta_%22%3A%22%22%2C%22ajax_pagination_infinite_stop%22%3A%22%22%2C%22css%22%3A%22%22%2C%22tdc_css%22%3A%22%22%2C%22td_column_number%22%3A2%2C%22header_color%22%3A%22%22%2C%22color_preset%22%3A%22%22%2C%22border_top%22%3A%22%22%2C%22class%22%3A%22tdi_19_860%22%2C%22tdc_css_class%22%3A%22tdi_19_860%22%2C%22tdc_css_class_style%22%3A%22tdi_19_860_rand_style%22%7D"
            response = requests.post( 
                f"https://{self.domains[0]}/wp-admin/admin-ajax.php",
                data=f"td_block_id=tdi_19_6e5&td_filter_value={code}&td_column_number=2&td_current_page=1&block_type=td_block_16&td_magic_token={magic_token}&action=td_ajax_block&td_atts={td_atts}",
                headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": f"https://{self.domains[0]}/motorsports/",
                "Origin": f"https://{self.domains[0]}",
                "User-Agent": self.user_agent
            },
                params={
                    "td_theme_name": "Newspaper", 
                    "v": "10.3.7"
                }
            ).json()
            soup = BeautifulSoup(response["td_data"], "html.parser")
            for game in soup.select("div.td-block-span4"):
                img = game.select_one("img").get("src")
                title = game.select_one("h3").text
                href = game.select_one("a").get("href")
                game_time = datetime(*(time.strptime(game.select_one("time").get("datetime"), "%Y-%m-%dT%H:%M:%S+00:00")[:6]))
                games.append(Game(title=title, links=[Link(address=href)], icon=img, league=league, starttime=game_time))
        return games

    def get_link(self, url):
        r_game = requests.get(url, headers={"Referer": self.domains[0], "User-Agent": self.user_agent}).text
        # if "https://streamtape.com/e" in r_game:
        #     embed_url = re.compile(r'src="(https://streamtape.com/e/.+?/)"').findall(r_game)[0]
        #     r = requests.get(embed_url, headers={"User-Agent": user_agent}).text
        #     soup = BeautifulSoup(r, "html.parser")
        #     mp4 = ""
        #     scripts = soup.find_all("script")
        #     for script in scripts:
        #         script_str = str(script)
        #         if "document.getElementById('" in script_str:
        #             mp4 = "https:" + eval(script_str[script_str.index("= ") + 2:].replace(";</script>", ""))
        #             break
        #     return mp4 + "&stream=1|User-Agent=%s&Referer=%s" % (user_agent, url) if mp4 != "" else url
        if "//ok.ru/videoembed" in r_game:
            embed_url = "https:" + re.compile(r'src="(//ok.ru/videoembed/.+?)"').findall(r_game)[0]
            r_embed = requests.get(embed_url, headers={"User-Agent": self.user_agent}).text
            embed_json = json.loads(html.unescape(re.compile(r'data-options="(.+?)"').findall(r_embed)[0]))
            metadata_json = json.loads(embed_json["flashvars"]["metadata"])
            return Link(address=metadata_json["hlsManifestUrl"], headers={"User-Agent": self.user_agent})
        return Link(address=url)
