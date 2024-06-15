import requests
import re
import threading
import time
from utils import util
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_one_page(start, f):
    resp = requests.get(
        f"https://movie.douban.com/top250?start={start}&filter=",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    # 获取当前页的电影
    items = soup.find_all("div", attrs={"class": "item"})
    print(f"开始爬取{start}-{start+25}: ", end=" ")
    for item in tqdm(items):
        line = []
        # l1
        pic = item.find(attrs={"class": "pic"})
        info = item.find(attrs={"class": "info"})
        # l1[pic]
        line.append(pic.em.string)  # 1-排名
        line.append(pic.a["href"])  # 2-链接
        img_src = pic.a.img["src"]
        line.append(img_src)  # 3-图片
        download = threading.Thread(
            target=util.download_img,
            args=(
                pic.em.string,
                img_src,
            ),
        )
        download.start()
        download.join()
        # util.download_img(pic.em.string, img_src)
        # l1[info]
        hd = info.find(attrs={"class": "hd"})
        bd = info.find(attrs={"class": "bd"})
        # l1[info] - l2[hd]
        line.append(hd.a.find("span").text.replace("/", "").strip())  # 4-标题
        line.append(
            (
                "可播放"
                if hd.find(attrs={"class": "playable"}) is not None
                else "不可播放"
            )
        )  # 5-可播放
        # l1[info] - l2[bd]
        splits = re.sub(" +", " ", bd.p.text.strip()).split("\n")
        first_line = splits[0].split(":")
        line.append(first_line[1].strip().split(" ")[0].strip())  # 6-导演
        line.append(
            (
                first_line[2].strip().split(" ")[0].strip()
                if len(first_line) >= 3
                else ""
            )
        )  # 7-主演
        second_line = splits[1].split("/")
        line.append(second_line[0].strip())  # 8-上映日期
        line.append(second_line[1].strip())  # 9-上映国家
        line.append(second_line[2].strip())  # 10-影片类型
        star_spans = bd.find(attrs={"class": "star"}).find_all("span")
        line.append(star_spans[0]["class"][0])  # 11-星级
        line.append(star_spans[1].text.strip())  # 12-评分
        line.append(star_spans[-1].text.strip()[:-3])  # 13-评价人数
        quote = bd.find(attrs={"class": "quote"})
        line.append((quote.text.strip() if quote is not None else ""))  # 14-名句
        f.write(",".join(line) + "\n")
        time.sleep(2)
