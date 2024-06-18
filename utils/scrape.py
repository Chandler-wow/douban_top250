import requests
import re
from utils import util
from bs4 import BeautifulSoup


def get_one_page(start, store_method, s, download):
    resp = requests.get(
        util.REQUEST_URL.format(start=start), headers=util.REQUEST_HEADERES
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    thread = None
    # 获取当前页的电影
    items = soup.find_all("div", attrs={"class": "item"})
    for item in items:
        line = {}
        # l1
        pic = item.find(attrs={"class": "pic"})
        info = item.find(attrs={"class": "info"})
        # l1[pic]
        line["rk"] = int(pic.em.string)  # 1-排名
        line["link"] = pic.a["href"]  # 2-链接
        line["img"] = pic.a.img["src"]  # 3-图片
        if download:
            thread = util.download_img(line["rk"], line["img"])
        # l1[info]
        hd = info.find(attrs={"class": "hd"})
        bd = info.find(attrs={"class": "bd"})
        # l1[info] - l2[hd]
        line["name"] = hd.a.find("span").text.replace("/", "").strip()  # 4-标题
        line["is_playable"] = (
            1 if hd.find(attrs={"class": "playable"}) is not None else 0
        )  # 5-可播放
        # l1[info] - l2[bd]
        splits = re.sub(" +", " ", bd.p.text.strip()).split("\n")
        first_line = splits[0].split(":")
        line["director"] = first_line[1].strip().split(" ")[0].strip()  # 6-导演
        line["actors"] = (
            first_line[2].strip().split(" ")[0].strip() if len(first_line) >= 3 else ""
        )  # 7-主演
        second_line = splits[1].split("/")
        line["release_date"] = second_line[0].strip()[:4]  # 8-上映日期
        line["release_countries"] = second_line[-2].strip()  # 9-上映国家
        line["type"] = second_line[-1].strip()  # 10-影片类型
        star_spans = bd.find(attrs={"class": "star"}).find_all("span")
        star = star_spans[0]["class"][0]
        line["star"] = float(
            (star[:7] + "." + star[7:])[6:9].replace("-", "")
        )  # 11-星级
        line["score"] = star_spans[1].text.strip()  # 12-评分
        line["comments"] = star_spans[-1].text.strip()[:-3]  # 13-评价人数
        quote = bd.find(attrs={"class": "quote"})
        line["quote"] = quote.text.strip() if quote is not None else ""  # 14-名句
        util.store_line(store_method, s, line)
        if download:
            thread.join()
