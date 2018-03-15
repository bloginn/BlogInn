# encoding: utf-8

from cook.common.Curl import Curl
from bs4 import BeautifulSoup
import re
import json
import os
import time
import shutil

rootPath = 'D:\\ted'


def log(str):
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = dt + ' ' + str
    saveContent(os.path.join(rootPath, 'ted.log'), log + '\r\n', True)
    print(log)
    return


def requestList(page):
    linkList = []

    url = 'https://www.ted.com/talks?page=' + str(page)
    res = Curl().get(url)
    if res['status'] == 200:
        body = res['body']

        soup = BeautifulSoup(body, "html5lib")  # pip install html5lib
        links = soup.find_all("a", {'data-ga-context': 'talks'})

        for link in links:
            href = link.get('href')
            if href not in linkList:
                linkList.append(href)

    return linkList


def requestOne(uri):
    result = {"mp3Url": "", "mp4Url": "", "mp4q": "", "id": 0, "uploadDate": "", "duration": "", "name": "",
              "description": ""}
    url = 'https://www.ted.com' + uri
    try:
        res = Curl().get(url)
        if res['status'] == 200:
            body = res['body']
            mp3Search = re.search('https([^\"]+)mp3', body)
            if mp3Search:
                mp3Url = mp3Search.group(1)
                result['mp3Url'] = 'https' + mp3Url + 'mp3'

            for q in ['950k', '1080p', '720p', '1500k', '600k', '480p', '450k', '320k', '180k', '']:
                mp4Search = re.search('https([^\"]+)' + q + '.mp4', body)
                if mp4Search:
                    result['mp4Url'] = 'https' + mp4Search.group(1) + q + '.mp4'
                    result['mp4q'] = q
                    break

            talkId = re.search('talk_id\":(\d+)\}', body).group(1)
            if talkId:
                result['id'] = talkId

            soup = BeautifulSoup(body, "html5lib")
            name = soup.find(attrs={"itemprop": "name"})['content']
            if name:
                result['name'] = name

            description = soup.find(attrs={"itemprop": "description"})['content']
            if description:
                result['description'] = description

            uploadDate = soup.find(attrs={"itemprop": "uploadDate"})['content']
            if uploadDate:
                result['uploadDate'] = uploadDate

            duration = soup.find(attrs={"itemprop": "duration"})['content']
            if duration:
                result['duration'] = duration

    except AttributeError:
        print("错误URL:" + url)
    return result


def requestText(id, lan='en'):
    text = ''
    url = 'https://www.ted.com/talks/' + str(id) + '/transcript.json?language=' + lan
    res = Curl().get(url)
    if res['status'] == 200:
        response = json.loads(res['body'])
        try:
            paragraphs = response['paragraphs']
            for one in paragraphs:
                for cue in one['cues']:
                    text += cue['text'].replace('\n', ' ') + ' '
                text += '\n'
        except KeyError:
            text = ''

    return text


def saveContent(filename, content, append=False):
    if append:
        mode = 'a+'
    else:
        mode = 'w+'
    f = open(filename, mode)
    f.write(str(content))
    f.close()


def downloadOne(uri, rootPath='./'):
    res = requestOne(uri)
    if (res['id']) and (res['uploadDate'] != ""):
        id = res['id']
        ts = time.strptime(res['uploadDate'][:19], "%Y-%m-%dT%H:%M:%S")
        prefix = str(time.strftime("%Y%m%d", ts)) + str(res['duration'])
        res['datetime'] = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        path = os.path.join(os.path.abspath(rootPath), str(prefix))
        jsonPath = os.path.join(path, str(id) + ".json")

        log("开始下载ID" + str(id) + "内容,目录:" + prefix)
        if os.path.exists(path):
            if not os.path.isfile(jsonPath):
                shutil.rmtree(path)
                log("json文件不存在,删除文件夹成功")

        if not os.path.exists(path):
            os.mkdir(path)
            log('创建文件夹成功:' + path)

        if res['mp3Url']:
            mp3Path = os.path.join(path, str(id) + ".mp3")
            if not os.path.isfile(mp3Path):
                log("mp3开始下载:" + str(res['mp3Url'].encode('utf-8')))
                Curl().download(res['mp3Url'], mp3Path)
                log('mp3下载完成')

        if res['mp4Url']:
            if res['mp4q']:
                res['mp4q'] = '-' + res['mp4q']
            mp4Path = os.path.join(path, str(id) + res['mp4q'] + ".mp4")
            if False and not os.path.isfile(mp4Path):
                log('mp4开始下载:' + str(res['mp4Url'].encode('utf-8')))
                Curl().download(res['mp4Url'], mp4Path)
                log('mp4下载完成')

        enPath = os.path.join(path, str(id) + ".en")
        if not os.path.isfile(enPath):
            enText = requestText(id, 'en')
            if enText != "":
                saveContent(enPath, enText.encode('utf-8'))
                log('英文字幕保存成功')

        cnPath = os.path.join(path, str(id) + ".cn")
        if not os.path.isfile(cnPath):
            cnText = requestText(id, 'zh-cn')
            if cnText != "":
                saveContent(cnPath, cnText.encode('utf-8'))
                log('中文字幕保存成功')

        saveContent(jsonPath, str(res))
        log('json信息保存成功')
        log('ID' + str(id) + "下载完成")


# downloadOne('/talks/petter_johansson_do_you_really_know_why_you_do_what_you_do',"C:/Users/zongbinghuang.ESG/Downloads/ted")

page = 2
log("开始处理page" + str(page))
for one in requestList(page):
    downloadOne(one, rootPath)
    time.sleep(60)
