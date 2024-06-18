import time
import random
import os
import pymysql
import sys
from utils import util, scrape
from tqdm import tqdm

# TODO: 添加日期分区，并写入数据库
if __name__ == "__main__":

    args = sys.argv
    store_method = args[1] if len(args) >= 2 else "file"
    download = bool(args[2]) if len(args) >= 3 else False
    print(
        """
爬取设置：
    1. 存储设置：{store_method}
    2. 图片下载：{download}
5秒后开始爬取 ===>""".format(
            store_method=store_method, download=download
        )
    )
    time.sleep(5)

    f = None
    if store_method == "file":
        if not os.path.exists(util.PATH_ASSETS):
            os.mkdir(util.PATH_ASSETS)
        f = open(util.PATH_ASSETS + "/movies.csv", "w")
        columns = "排名,链接,图片,标题,可播放,导演,主演,上映日期,上映国家,影片类型,星级,评分,评价人数,名句\n"
        f.write(columns)

    db = None
    cursor = None
    if store_method == "mysql":
        db = pymysql.connect(
            host=util.MYSQL_HOST,
            user=util.MYSQL_USER,
            password=util.MYSQL_PASSWORD,
            database=util.MYSQL_DATABASE,
        )
        cursor = db.cursor()
        cursor.execute(util.SQL_DROP_TABLE)
        cursor.execute(util.SQL_CREATE_TABLE)

    for start in tqdm(range(0, 250, 25)):
        scrape.get_one_page(
            start, store_method, f if store_method == "file" else cursor, download
        )
        if store_method == "mysql":
            db.commit()
        time.sleep(random.randint(5, 10))

    if store_method == "file":
        f.close()
    elif store_method == "mysql":
        db.close()
