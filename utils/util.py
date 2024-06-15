import os
import requests

PATH_ASSETS = "./assets"
PATH_IMG = PATH_ASSETS + "/img"


def download_img(seq, url):
    if not os.path.exists(PATH_IMG):
        os.mkdir(PATH_IMG)
    with open(f"{PATH_IMG}/movie_{seq.rjust(3,'0')}_img.jpg", "wb") as img:
        img.write(requests.get(url).content)
