import time
import random
import os
from utils import util, scrape

if __name__ == "__main__":

    if not os.path.exists(util.PATH_ASSETS):
        os.mkdir(util.PATH_ASSETS)
    res_path = util.PATH_ASSETS + "/movies.csv"
    with open(res_path, "w") as f:
        columns = "排名,链接,图片,标题,可播放,导演,主演,上映日期,上映国家,影片类型,星级,评分,评价人数,名句\n"
        f.write(columns)
    with open(res_path, "a") as f:
        for start in range(0, 250, 25):
            scrape.get_one_page(start, f)
            time.sleep(random.randint(5, 10))
