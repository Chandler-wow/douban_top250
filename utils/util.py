import os
import requests
import threading
from datetime import datetime

REQUEST_URL = "https://movie.douban.com/top250?start={start}&filter="
REQUEST_HEADERES = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

PATH_ASSETS = "./assets"
PATH_IMG = PATH_ASSETS + "/img"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "bdwJf0124"
MYSQL_DATABASE = "test"

SQL_DROP_TABLE = """
DROP TABLE IF EXISTS douban_250;
"""

SQL_CREATE_TABLE = """
CREATE TABLE douban_250(
    date VARCHAR(10) NOT NULL COMMENT '日期',
    rk INT NOT NULL COMMENT '排名',
    name VARCHAR(1024) COMMENT '名称',
    link VARCHAR(1024) COMMENT '豆瓣链接',
    img VARCHAR(1024) COMMENT '图片',
    is_playable INT COMMENT '可播放',
    director VARCHAR(1024) COMMENT '导演',
    actors VARCHAR(1024) COMMENT '主演',
    release_date VARCHAR(10) COMMENT '上映日期',
    release_countries VARCHAR(1024) COMMENT '上映国家',
    type VARCHAR(1024) COMMENT '影片类型',
    star INT COMMENT '星级',
    score FLOAT COMMENT '评分',
    comments INT COMMENT '评价数量',
    quote TEXT COMMENT '名句',
    PRIMARY KEY (date,rk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

SQL_INSERT = """
INSERT INTO douban_250 VALUES 
(\'{date}\',{rk},\'{name}\',\'{link}\',\'{img}\',{is_playable},\'{director}\',\'{actors}\',\'{release_date}\',\'{release_countries}\',\'{type}\',{star},{score},{comments},\'{quote}\')
"""


def download_img(seq, url):

    thread = threading.Thread(
        target=download,
        args=(
            seq,
            url,
        ),
    )
    thread.start()
    return thread


def download(seq, url):
    if not os.path.exists(PATH_IMG):
        os.mkdir(PATH_IMG)
    with open(f"{PATH_IMG}/movie_{'%03d'%seq}_img.jpg", "wb") as img:
        img.write(requests.get(url).content)


def insert_sql(cursor, map):
    date = datetime.now().strftime("%Y")
    sql = SQL_INSERT.format(
        date=date,
        rk=map["rk"],
        name=map["name"],
        link=map["link"],
        img=map["img"],
        is_playable=map["is_playable"],
        director=map["director"],
        actors=map["actors"],
        release_date=map["release_date"],
        release_countries=map["release_countries"],
        type=map["type"],
        star=map["star"],
        score=map["score"],
        comments=map["comments"],
        quote=map["quote"].replace("'", "\\'").replace('"', '\\"'),
    )
    cursor.execute(sql)


def store_line(method, s, line):
    if method == "file":
        # python3.6后，dict的values顺序是插入顺序
        s.write(",".join(map(lambda v: str(v), line.values())) + "\n")
    elif method == "mysql":
        insert_sql(s, line)
