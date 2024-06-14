import requests
import re
import time
import os
import random
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_one_page(start, headers, f):
    resp = requests.get(
        f"https://movie.douban.com/top250?start={start}&filter=", headers=headers
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
        download_img(pic.em.string, img_src)
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


def download_img(seq, url):
    if not os.path.exists("./assets/img"):
        os.mkdir("./assets/img")
    with open(f"./assets/img/movie_{seq}_img.jpg", "wb") as img:
        img.write(requests.get(url).content)
    time.sleep(random.randint(1, 5))


# TODO: 电影图片下载，多线程的方式使用
# TODO: 分文件构建程序
if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    columns = "排名,链接,图片,标题,可播放,导演,主演,上映日期,上映国家,影片类型,星级,评分,评价人数,名句\n"
    with open("./assets/movies.csv", "w") as f:
        f.write(columns)

    with open("./assets/movies.csv", "a") as f:
        for start in range(0, 25, 25):
            get_one_page(start, headers, f)
            time.sleep(random.randint(1, 5))
