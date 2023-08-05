import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import txt2proj
from template_generator import binary as genertor_binary
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

rootDir = ""
curGroupId = 0
allCount = 0
successCount = 0

def clearDir():
    s = os.path.join(rootDir, ".download")
    if os.path.exists(s):
        shutil.rmtree(s)
    s1 = os.path.join(rootDir, ".out")
    if os.path.exists(s1):
        shutil.rmtree(s1)

def curDownloadDir():
    s = os.path.join(rootDir, ".download", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s

def curOutputDir():
    s = os.path.join(rootDir, ".out", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s
    
def notifyMessage(ossurl, count):
    try:
        param = {
            "id": curGroupId,
            "video_path": ossurl,
            "video_num": count
        }
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.post(f"https://beta.2tianxin.com/common/admin/tta/get_set_task_complete", json.dumps(param), verify=False)
        if res.status_code == 200:
            logging.info(f"notifyMessage success")
        else:
            resContext = res.content.decode(encoding="utf8", errors="ignore")
            logging.info(f"notifyMessage fail! code={res.status_code}, context={resContext}")
            print("report error!")
        s.close()
    except Exception as e:
        logging.info(f"notifyMessage exception :{e}")

def processAllVideo(crawler_template_name, addRandomText):
    src = curDownloadDir()
    dst = curOutputDir()
    dataFile = os.path.join(src, "params.config")
    data = []
    templateDir = os.path.join(genertor_binary.randomEffectPath(""), crawler_template_name)
    for root,dirs,files in os.walk(curDownloadDir()):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".mp4" or ext == ".mov":
                w,h,bitrate,fps = utils.videoInfo(os.path.join(src, file))
                if w <= 0 or bitrate <= 0:
                    continue
                realTemplateDir = templateDir
                if addRandomText:
                    tempDir = txt2proj.newTemplateWithText(templateDir, w, h)
                    if len(realTemplateDir) > 0:
                        realTemplateDir = tempDir
                data.append({
                    "input":[os.path.join(src, file)],
                    "template": realTemplateDir,
                    "params":{},
                    "output": os.path.join(dst, file)})
        if root != files:
            break
    with open(dataFile, 'w') as f:
        json.dump(data, f)
    try:
        print(f"template --input {dataFile} --adaptiveSize")
        result = subprocess.run(f"template --input {dataFile} --adaptiveSize", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            print("=== process success")
            for it in data:
                if it["template"] != templateDir:
                    shutil.rmtree(it["template"])
        else:
            print("====================== script error ======================")
            print(result.stderr.decode(encoding="utf8", errors="ignore"))
            print("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    
def download(name, media_type, post_text, media_resource_url, audio_resource_url):
    ext = ".mp4"
    if media_type == "image":
        ext = ".jpg"
    elif media_type == "audio":
        ext = ".mp3"
    savePath = os.path.join(curDownloadDir(), f"{name}{ext}")
    if os.path.exists(savePath):
        os.remove(savePath)
    #download
    logging.info(f"download: {media_resource_url}, {audio_resource_url}")
    s = requests.session()
    s.headers.update({'Connection':'close'})
    ua = UserAgent()
    download_start_pts = calendar.timegm(time.gmtime())
    file = s.get(media_resource_url, verify=False, headers={'User-Agent': ua.random})
    with open(savePath, "wb") as c:
        c.write(file.content)
    download_end_pts = calendar.timegm(time.gmtime())
    logging.info(f"download duration={(download_end_pts - download_start_pts)}")
    #merge audio & video
    if len(audio_resource_url) > 0:
        audioPath = os.path.join(curDownloadDir(), f"{name}.mp3")
        file1 = s.get(audio_resource_url)
        with open(audioPath, "wb") as c:
            c.write(file1.content)
        tmpPath = os.path.join(curDownloadDir(), f"{name}.mp4.mp4")
        utils.ffmpegProcess(f"-i {savePath} -i {audioPath} -vcodec copy -acodec copy -y {tmpPath}")
        if os.path.exists(tmpPath):
            os.remove(savePath)
            os.rename(tmpPath, savePath)
            os.remove(audioPath)
        logging.info(f"merge => {file}, {file1}")
    s.close()
    
def processPosts(uuid, data):
    global allCount

    post_text = data["text"]
    medias = data["medias"]
    idx = 0
    for it in medias:
        media_type = it["media_type"]
        media_resource_url = it["resource_url"]
        audio_resource_url = ""
        if "formats" in it:
            formats = it["formats"]
            quelity = 0
            for format in formats:
                if format["quality"] > quelity and format["quality"] <= 1080:
                    quelity = format["quality"]
                    media_resource_url = format["video_url"]
                    audio_resource_url = format["audio_url"]
        try:
            allCount += 1
            download(f"{uuid}_{idx}", media_type, post_text, media_resource_url, audio_resource_url)
            time.sleep(1)
        except Exception as e:
            print("====================== download+process+upload error! ======================")
            print(e)
            print("======================                                ======================")
            time.sleep(10) #maybe Max retries
        idx += 1

def aaaapp(multiMedia, url,  cursor, page):
    if len(url) <= 0:
        return
    
    param = {
        "userId": "D042DA67F104FCB9D61B23DD14B27410",
        "secretKey": "b6c8524557c67f47b5982304d4e0bb85",
        "url": url,
        "cursor": cursor,
    }
    requestUrl = "https://h.aaaapp.cn/posts"
    if multiMedia == False:
        requestUrl = "https://h.aaaapp.cn/single_post"
    logging.info(f"=== request: {requestUrl} cursor={cursor}")
    s = requests.session()
    s.headers.update({'Connection':'close'})
    res = s.post(requestUrl, params=param, verify=False)
    with open(os.path.join(curDownloadDir(), "config.txt"), mode='a') as configFile:
        configFile.write(f'\n {res.content} \n')
    if len(res.content) > 0:
        data = json.loads(res.content)
        if data["code"] == 200:
            idx = 0
            if multiMedia == False:
                processPosts(f"{curGroupId}_{page}_{idx}", data["data"])
                if allCount > 1000:
                    print("stop mission with out of cnt=1000")
                    return
            else:
                posts = data["data"]["posts"]
                for it in posts:
                    processPosts(f"{curGroupId}_{page}_{idx}", it)
                    if allCount > 1000:
                        print("stop mission with out of cnt=1000")
                        return
                    idx+=1
            if "has_more" in data["data"] and data["data"]["has_more"] == True:
                next_cursor = ""
                if "next_cursor" in data["data"] and len(str(data["data"]["next_cursor"])) > 0:
                    if "no" not in str(data["data"]["next_cursor"]):
                        next_cursor = str(data["data"]["next_cursor"])
                if len(next_cursor) > 0:
                    aaaapp(multiMedia, url, next_cursor, page+1)
        else:
            print(f"=== error aaaapp, context = {res.content}")
            logging.info(f"=== error aaaapp, context = {res.content}")
            if data["code"] == 300:
                print("=== no money, exit now!")
                logging.info("=== no money, exit now!")
                exit(-1)
    else:
        print("=== error aaaapp, context = {res.content}, eixt now!")
        logging.info("=== error aaaapp, context = {res.content}, eixt now!")
        exit(-1)
    s.close()

def cacheDir():
    src = curDownloadDir()
    dist = os.path.join(os.path.dirname(src), f"{curGroupId}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(src):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, src)
            zip.write(filepath, writepath)
    zip.close()
    shutil.copyfile(dist, f"d://{curGroupId}.zip")
    os.remove(dist)

    dst = curOutputDir()
    dist1 = os.path.join(os.path.dirname(dst), f"{curGroupId}_out.zip")
    zip1 = zipfile.ZipFile(dist1, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(dst):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, dst)
            zip1.write(filepath, writepath)
    zip1.close()
    shutil.copyfile(dist1, f"d://{curGroupId}_out.zip")
    os.remove(dist1)

def process(url, crawler_template_name, addRandomText):
    global successCount
    ### downlaod
    print(f"=== downloading ")
    aaaapp(True, url, "", 0)
    ## process
    print(f"=== processing ")
    processAllVideo(crawler_template_name, addRandomText)
    cacheDir() #cache file to d://
    ### upload
    print(f"=== uploading ")
    dist = os.path.join(os.path.dirname(curOutputDir()), f"{curGroupId}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(curOutputDir()):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            writepath = os.path.relpath(filepath, curOutputDir())
            zip.write(filepath, writepath)
            successCount+=1
    zip.close()
    ossurl = utils.ftpUpload(dist)[0]
    ### notify
    print(f"=== notifying ")
    notifyMessage(ossurl, successCount)

def lastTaskFile():
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisFileDir, "last_task.txt")

def removeLastTask():
    file = lastTaskFile()
    if os.path.exists(file):
        os.remove(file)

def getLocalTask():
    file = lastTaskFile()
    data = {}
    if os.path.exists(file):
        with open(file, 'r', encoding='UTF-8') as f:
            data = json.load(f)
    return data

def saveLastTask(data):
    file = lastTaskFile()
    with open(file, 'w') as f:
        json.dump(data, f)

def getTask():
    data = getLocalTask()
    if len(data) == 0:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.get(f"https://beta.2tianxin.com/common/admin/tta/get_task?t={random.randint(100,99999999)}", verify=False)
        s.close()
        if len(res.content) > 0:
            data = json.loads(res.content)
            saveLastTask(data)
    return data

def autoCrawler():
    global rootDir
    global curGroupId
    global allCount
    global successCount
    
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    rootDir = thisFileDir
    while(os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        try:
            data = getTask()
            if len(data) > 0:
                curGroupId = data["id"]
                allCount = 0
                successCount = 0
                start_pts = calendar.timegm(time.gmtime())
                logging.info(f"================ begin {curGroupId} ===================")
                logging.info(f"========== GetTask: {data}")
                print(f"=== begin {curGroupId}")
                url = data["url"].replace("\n", "").replace(";", "").replace(",", "").strip()
                crawler_template_name = data["crawler_template_name"].replace("\n", "").replace(";", "").replace(",", "").strip()
                if len(crawler_template_name) <= 0:
                    crawler_template_name = "template2"
                addText = False
                if "addText=true" in url:
                    addText = True
                    url = url.replace("addText=true","")

                clearDir()
                process(url, crawler_template_name, addText)
                removeLastTask()

                current_pts = calendar.timegm(time.gmtime())
                print(f"complate => {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}")
                logging.info(f"================ end {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}===================")
                exit(-1)
        except Exception as e:
            notifyMessage(False, str(e))
            logging.error("====================== uncatch Exception ======================")
            logging.error(e)
            logging.error("======================      end      ======================")
        time.sleep(2)
    os.remove(os.path.join(thisFileDir, "stop.now"))
    print(f"stoped !")

# urllib3.disable_warnings()
# d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# thisFileDir = os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename=f"{thisFileDir}/ttauto_crawler_{d}.log", 
#                     format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     encoding="utf-8",
#                     level=logging.DEBUG)
# rootDir = thisFileDir

# data = {
#     "663": "https://www.douyin.com/user/MS4wLjABAAAApGFo2iYnfSnQzJZ0WxesCM4RJrRuw6wOxgPEJIID5Ms?is_search=0&list_name=follow&nt=0addText=true",
# }

# for k in data:
#     curGroupId = int(k)
#     allCount = 0
#     successCount = 0
#     start_pts = calendar.timegm(time.gmtime())
#     logging.info(f"================ begin {curGroupId} ===================")
#     print(f"=== begin {curGroupId}")
#     url = data[k]
#     crawler_template_name = "template8"
#     process(url, crawler_template_name, True)
#     current_pts = calendar.timegm(time.gmtime())
#     print(f"complate => {curGroupId} rst={successCount}/{allCount} duration={(current_pts - start_pts)}")
#     logging.info(f"================ end {curGroupId} ===================")

