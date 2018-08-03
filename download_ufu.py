import os
import time
import sys
import asyncio
from concurrent import futures

from urllib.request import urlopen
import bs4
import aiohttp
import requests

"""
下载universalflowuniversity.com网站上的电子书
"""

BASE_URL = 'http://universalflowuniversity.com/Books/Computer%20Programming/Data%20Mining%20and%20Data%20Science/'
DEST_DIR = '/home/fm22/Downloads/UFU/data_mining_and_data_science/'

MAX_WORKERS = 10    # 最多同时下载 10 个文件


def save_file(file_cache, save_name):
    """保存单个文件"""
    path = os.path.join(DEST_DIR, save_name)
    with open(path, 'wb') as fp:
        fp.write(file_cache)


def show(text):
    """显示下载相关信息文字"""
    print(text)
    sys.stdout.flush()


def get_file_content(filename):
    """获取文件的数据"""
    if BASE_URL.endswith('/'):
        url_path = BASE_URL + filename
    else:
        url_path = BASE_URL + '/' + filename

    resp = requests.get(url_path)
    return resp.content


def get_save_names(filenames):
    """获取保存文件的名字，将 URL 中的 %20（空格) 替换为 _"""
    return [fn.replace('%20', '_') for fn in filenames]


def get_filenames():
    """获取 URL 下链接的文件名称"""
    html = urlopen(BASE_URL)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    name_list = bsobj.find_all('a')

    """
    所下载的 html 中的 text 形如
    =============================
    Name
    Last modified
    Size
    Description
    Parent Directory
    21 Recipes for Minin..>
    2016 Data Science Sa..>
    A Practical Guide to..>
    A Simple Introductio..>
    Adaptive Stream Mini..>
    Advanced Data Analys..>
    Advanced Data Mining..>
    Advanced Object-Orie..>
    Agile Data Science 2..>
    ...
    =============================
    """

    return [name.get('href') for name in name_list if len(name.get_text()) > 20]


def download():
    """单线程下载文件"""
    file_names = get_filenames()
    save_names = get_save_names(file_names)

    for fn, sn in zip(file_names, save_names):
        if os.path.exists(DEST_DIR + sn):
            print("File {} existed.".format(sn))
            continue

        file_cache = get_file_content(fn)
        show(fn)
        save_file(file_cache, sn)
        print("{} is saved.".format(sn))

    return len(file_names)


def download_one(filename, save_file):
    """下载单个文件"""
    file_cache = get_file_content(filename)
    show(filename)
    save_file(file_cache, save_file)


def download_many():
    """下载多个文件"""
    file_names = get_filenames()
    save_files = get_save_names(file_names)

    workers = min(MAX_WORKERS, len(file_names))
    with futures.ThreadPoolExecutor(workers) as executer:
        res = executer.map(download_one, file_names, save_files)

    return len(file_names)


def main():
    t0 = time.time()
    count = download()
    elapsed = time.time() - t0

    msg = '{} files downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
