import os

import requests

url = "http://saic.che.link:4881/source/6dec452b0d40295cb57277866882cd2a9267c0b9b43a95d761c29f1113d57419/update.zip"

def download(url):
    r = requests.get(url, stream=True)
    print("code:", r.status_code)
    if r.status_code == 404:
        print("下载失败，可能地址异常")
        return r.status_code
    print("下载完成")
    return r.status_code
download(url)
