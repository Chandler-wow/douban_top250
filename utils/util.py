import os
import requests
from datetime import datetime

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
    if not os.path.exists(PATH_IMG):
        os.mkdir(PATH_IMG)
    with open(f"{PATH_IMG}/movie_{seq.rjust(3,'0')}_img.jpg", "wb") as img:
        img.write(requests.get(url).content)


def insert_sql(cursor, map):
    date = datetime.now().strftime("%Y%m%d")
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
