# -*- coding:utf-8 -*-
"""
@version: 3.7
@time: 2023/3/24 8:40
@filename: connectCode.py
@auther: SiriBen
@Descript: 获取连接码
"""

import requests
from fake_useragent import UserAgent
import os
import hashlib

def getExtermalCode():
    # location = os.getcwd() + '\\fake_useragent.json'
    location = os.sep.join([os.getcwd(), r'fake_useragent.json'])
    print(location)
    # ua = UserAgent(cache_path='fake_useragent.json')
    # url = r'https://meta-3.cn/Software.txt'
    url = r'http://222.186.141.155:8866/Software.txt'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }


    print(headers)
    response = requests.get(url=url, headers=headers)
    resStr = response.text
    #print(resStr)

    return resStr

def fileExists(filePath):
    flag = False

    if os.path.exists(filePath):
        #print('文件存在')
        flag = True

    return flag

def getFileValue(filePath):
    BUF_SIZE = 65536
    with open(filePath, 'r') as f:
        tempStr = f.read(BUF_SIZE)
        #print(tempStr)
        return tempStr

def getSha256(tempStr):
    sha256 = hashlib.sha256()
    sha256.update(tempStr.encode('utf-8'))
    res = sha256.hexdigest()
    #print(res)
    return res


if __name__ == '__main__':
    resStr = getExtermalCode()

    pathStr = os.path.dirname(os.path.dirname(__file__))
    filePath = 'CONNECT-KEY.txt'
    filePath = pathStr + '\\' + filePath
    # filePath = os.sep.join([pathStr, filePath])
    print(filePath)
    flag = fileExists(filePath)

    if flag:
        strLocal = getFileValue(filePath)
    else:
        print('文件不存在')


    strSha256 = getSha256(resStr)

    flag2 = False
    if strLocal == strSha256:
        print('通过')
        flag2 = True
    else:
        print('未通过')
