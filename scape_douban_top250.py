import requests
import re
from bs4 import BeautifulSoup

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    resp = requests.get("https://movie.douban.com/top250", headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    # 获取当前页的电影
    items = soup.find_all("div", attrs={"class": "item"})
    with open("./movies.csv", "w") as f:
        columns = "排名,链接,图片,标题,可播放,导演,主演,上映日期,上映国家,影片类型,星级,评分,评价人数,名句\n"
        f.write(columns)
        for item in items:
            line = []
            # l1
            pic = item.find(attrs={"class": "pic"})
            info = item.find(attrs={"class": "info"})
            # l1[pic]
            line.append(pic.em.string)  # 1-排名
            line.append(pic.a["href"])  # 2-链接
            line.append(pic.a.img["src"])  # 3-图片
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
            line.append(bd.find(attrs={"class": "quote"}).text.strip())  # 14-名句
            str_line = ",".join(line)
            f.write(str_line + "\n")
