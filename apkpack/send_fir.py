# -*- coding:utf-8 -*-
"""
@author: guoyang
@contact: guoyang_add@163.com
@file: send_fir.py
@time: 2019/1/9 5:52 PM
@desc:
"""
import os
import platform
import re

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

__author__ = 'guoyang'

# 这里输入你的项目名称
apkName = ""
# android的项目地址
projectPath = "/Users/guoyang/FuQinHengYe/FortunesFinance"
# 构建命令
buildTool = "releseApi"
# Android SDK buidtools路径
sdkBuildToolPath = "/Users/guoyang/Library/Android/sdk/build-tools/26.0.2"

# fir的配置
# fir的BundleId
firBundleId = ''
# fir的apiToken
firApiToken = ''


# 判断当前系统
def isWindows():
    sysStem = platform.system()
    if "Windows" in sysStem:
        return 1
    else:
        return 0


# 兼容不同系统的路径分隔符
def getBackslash():
    if isWindows() == 1:
        return "\\"
    else:
        return "/"


# 获取apk
def getApk(path):
    for file in os.listdir(path):
        if ".apk" in file:
            return file


# 从fir获取token
def getToken():
    data = {
        'type': 'android',
        'bundle_id': firBundleId,
        'api_token': firApiToken
    }
    req = requests.post(url='http://api.fir.im/apps', data=data)
    return req


# 将apk上传fir
def updataApk(apkPath, data):
    try:
        print("开始上传apk,上传信息为:")
        print(data)
        file = {'file': open(apkPath, 'rb')}
        param = {
            'key': data['key'],
            'token': data['token'],
            'x:name': apkName,
            'x:version': data['version'],
            'x:build': data['build']
        }
        urllib3.disable_warnings(InsecureRequestWarning)
        req = requests.post(url=data['upload_url'], files=file, data=param, verify=False)
        return req
    except Exception as e:
        print('error' + e)


# 开始构建apk
def buildApk():
    buildApkShell = "./gradlew clean assemble" + buildTool + "Release"
    os.system(buildApkShell)
    print('开始构建Apk:' + buildApkShell)


# 获取apk的信息
def getApkInfo(apkPath):
    apkInfo = os.popen(sdkBuildToolPath + getBackslash() + "aapt d badging " + apkPath).read()
    print('获取apk信息为:' + apkInfo)
    data = {}
    match = re.compile(
        "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(apkInfo)
    data['version'] = match.group(3)
    data['build'] = match.group(2)
    return data


if __name__ == '__main__':
    projectPath = projectPath + getBackslash()
    os.chdir(projectPath)
    # 构建apk
    buildApk()
    print('Apk构建成功')
    # 获取apk所在的路径
    buildPath = ''
    if buildTool != "":
        buildPath = buildTool + getBackslash()
    apkPath = projectPath + "app" + getBackslash() + "build" + getBackslash() + "outputs" + getBackslash() + "apk" + \
              getBackslash() + buildPath + "release" + getBackslash()
    # 获取apk路径
    outputApk = apkPath + getApk(apkPath)
    print('apk的完整路径为:' + outputApk)
    # 获取apk的信息
    data = getApkInfo(outputApk)
    # 获取fir的token
    response = getToken().json()['cert']['binary']
    data['key'] = response['key']
    data['token'] = response['token']
    data['upload_url'] = response['upload_url']
    # 开始上传apk
    result = updataApk(outputApk, data)
    if result.ok:
        print('上传成功')
    else:
        print('上传失败')
