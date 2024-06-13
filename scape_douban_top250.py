import requests
import re
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
resp = requests.get("https://movie.douban.com/top250", headers=headers)
soup = BeautifulSoup(resp.text,"html.parser")
items = soup.find_all('div',attrs={"class":"item"})
# print(items[0])
# pic = items[0].find(attrs = {"class":"pic"})
# print(f"排名：{pic.em.string}")
# print(f"链接：{pic.a['href']}")
# print(f"图片：{pic.a.img['src']}")
info = items[0].find(attrs = {"class": "info"})
hd = info.find(attrs = {"class":"hd"})
# for title in hd.a.find_all("span"):
        # print(f"{('标题' if title['class'][0] == 'title' else'其他标题')}：{title.text.replace('/','').strip()}")
# print(f"是否可播放：{('可播放' if hd.find(attrs = {'class':'playable'}) is not None else '不可播放')}")
bd = info.find(attrs = {"class":"bd"})
splits = re.sub(" +"," ",bd.p.text.strip()).split('\n')
# first_line = splits[0].split(':')
# print(f"导演：{first_line[1].strip().split(' ')[0].strip()}")
# print(f"主演：{first_line[2].strip().split(' ')[0].strip()}")
# second_line = splits[1].split('/')
# print(f"上映日期：{second_line[0].strip()}")
# print(f"上映地点：{second_line[1].strip()}")
# print(f"影片类型：{second_line[2].strip()}")
# print(re.split(" +",info.p.text.replace("\xa0","").strip()))
# star = bd.find(attrs = {"class":"star"})
# star_spans = star.find_all('span')
# print(f"星级：{star_spans[0]['class'][0]}")
# print(f"评分：{star_spans[1].text.strip()}")
# print(f"评价人数：{star_spans[-1].text.strip()[:-3]}")
# quote = bd.find(attrs = {"class":"quote"})
# print(f"名言：{quote.text.strip()}")