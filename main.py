import time
import random
import os
import pymysql
from utils import util, scrape

# TODO: 添加日期分区，并写入数据库
if __name__ == "__main__":

    if not os.path.exists(util.PATH_ASSETS):
        os.mkdir(util.PATH_ASSETS)

    db = pymysql.connect(
        host=util.MYSQL_HOST,
        user=util.MYSQL_USER,
        password=util.MYSQL_PASSWORD,
        database=util.MYSQL_DATABASE,
    )
    cursor = db.cursor()
    cursor.execute(util.SQL_DROP_TABLE)
    cursor.execute(util.SQL_CREATE_TABLE)
    # res_path = util.PATH_ASSETS + "/movies.csv"
    # with open(res_path, "w") as f:
    #     columns = "排名,链接,图片,标题,可播放,导演,主演,上映日期,上映国家,影片类型,星级,评分,评价人数,名句\n"
    #     f.write(columns)
    # with open(res_path, "a") as f:
    for start in range(0, 250, 25):
        print(f"开始爬取{start}-{start+25}: ")
        scrape.get_one_page_mysql(start, cursor)
        db.commit()
        time.sleep(random.randint(5, 10))
