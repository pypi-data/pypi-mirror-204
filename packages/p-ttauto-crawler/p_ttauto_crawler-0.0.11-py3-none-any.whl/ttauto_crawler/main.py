import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import auto_crawler
from ttauto_crawler import txt2proj
import logging
import urllib3
import datetime
import shutil
import subprocess
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
import uuid
import calendar

def img2video():
    if len(sys.argv) <= 2:
        print('please s')
        return
    dir = sys.argv[2]
    cnt = sys.argv[3]
    if cnt.isdigit() == False:
        print('count is not digit')
        return
    if os.path.exists(dir) == False:
        print(f'path: {dir} not found')
        return
    txt2proj.randomImageCntToVideo(dir, int(cnt))
         
def auto():
    auto_crawler.autoCrawler()

module_func = {
    "--img2video": img2video,
    "--auto": auto
}

def main():
    urllib3.disable_warnings()
    d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename=f"{thisFileDir}/ttauto_crawler_{d}.log", 
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        encoding="utf-8",
                        level=logging.DEBUG)
    
    if len(sys.argv) < 2:
        auto()
        return
    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
        
if __name__ == '__main__':
    main()
