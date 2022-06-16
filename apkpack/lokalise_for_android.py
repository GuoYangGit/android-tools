#!/usr/bin/python3
# coding:utf-8

import xml.etree.ElementTree as ET
import os
import shutil

# 本地资源地址
lokalStrValues = "/Users/yz/IntelliJIDEAProjects/LamourApp/app/src/main/res/"

# Localise 本地存储目录
lokalisePath = "/Users/yz/IntelliJIDEAProjects/script/lokalise"

# Localise token
token = "83bb3cc3d8c32aa14b254421f21ead2f51b31f4d"

# Localise projectId
projectId = "4205512460e6db01add0a6.69814144"

# 文件名映射  远端名称:本地名称
fileDirMapping = {
    'values': 'values-zh-rCN',
    'values-en': 'values',
    'values-ar': 'values-ar',
    'values-es': 'values-es',
    'values-hi': 'values-hi-rIN',
    'values-id': 'values-in',
    'values-ms': 'values-ms-rMY',
    'values-pt-rBR': 'values-pt',
    'values-ru': 'values-ru',
    'values-th': 'values-th-rTH',
    'values-tr': 'values-tr-rTR',
    'values-vi': 'values-vi-rVN',
    'values-zh-rHK': 'values-zh-rHK',
    'values-zh-rTW': 'values-zh-rTW'
}

# localise 执行命令拼接
lokalise2Cmd = 'lokalise2 \
    --token ' + token + ' \
    --project-id  ' + projectId + ' \
    file download \
    --format xml \
    --all-platforms android \
    --export-sort first_added \
    --unzip-to ' + lokalisePath


def xmlTreeToDict(xmlTree):
    xmlMap = {}
    for item4 in xmlTree:
        xmlMap[item4.attrib['name']] = item4.text

    return xmlMap


# 获取所有strings
def fileListFunc(filePathList):
    fileList = []
    for top, dirs, nondirs in os.walk(filePathList):
        for item in nondirs:
            fileList.append(os.path.join(top, item))

    strs = []
    for i in fileList:
        if i.find("strings") > 0:
            strs.append(i)
    return strs


def findStringFromFile(file):
    f = open(file, encoding="utf8", errors="ignore")
    lines = f.readlines()
    errCount = 0
    for line in lines:
        if not match(line):
            errCount += 1
        if not matchAsc(line):
            print(file)
    # if errCount > 0:
    # print(errCount,file)


# 如果百分号前是数字,则忽略
def isNum(s):
    arr = s.split("%")
    for str in arr:
        beforStr = str[len(str) - 2:len(str) - 1]
        # print("beforStr",beforStr)
        if beforStr.isnumeric():
            return True
    return False


## 获取xml中的placeHolder  key:[placeHolders]
def match(s):
    count = s.count("%")
    matchCount = 0
    if count > 0:
        for matchStr in matchList:
            isMatch = s.count(matchStr)
            if isMatch > 0:
                matchCount = matchCount + isMatch
        if count != matchCount and not isNum(s):
            print(s.strip())
            return False
    return True


# 用来匹配 特殊字符
def matchAsc(s):
    if s.find("&") != -1 and s.find("#") != -1 and s.find("&#") == -1:
        print("matchAsc:", s.strip())
        return False
    return True


if __name__ == '__main__':

    print("lokalise网络文件拉取中....")
    # 执行lokalise命令
    result = os.popen(lokalise2Cmd).read()

    # 输出lokalise命令返回
    print(result)
    if "Unzipping to" in result.split('\n')[-2]:
        print("拉取成功！！！")
    else:
        print("拉取失败!!!")
        exit()

    startColorRed = "\033[31m"
    startColorYellow = "\033[33m"
    endColor = "\033[0m"

    endPrintList = []

    localRes = os.listdir(lokalStrValues)

    for key in fileDirMapping:
        # 遍历映射字典
        localFileName = fileDirMapping[key]
        if localFileName in localRes:
            # 定位文件
            localFilePath = os.path.join(lokalStrValues, localFileName, "strings.xml")
            lokaliseFilePath = os.path.join(lokalisePath, key, "strings.xml")
            # 解析xml
            localTree = ET.parse(localFilePath).getroot()
            lokaliseTree = ET.parse(lokaliseFilePath).getroot()
            # xml转为字典类型 key:value
            localDict = xmlTreeToDict(localTree)
            lokaliseDict = xmlTreeToDict(lokaliseTree)

            # 计算新增
            insertDeffer = set(lokaliseDict.keys()) - set(localDict.keys())

            # 计算删除
            delDeffer = set(localDict.keys()) - set(lokaliseDict.keys())

            # 计算修改
            updateDeffer = lokaliseDict.items() ^ localDict.items()

            # 修改转为字典
            updateDefferDict = dict(updateDeffer)

            # 删除修改字典中包含的新增
            for insertKey in insertDeffer:
                updateDefferDict.pop(insertKey)

            # 删除修改字典中包含的删除
            for delKey in delDeffer:
                updateDefferDict.pop(delKey)

            print(localFileName + "新增多语言数量：" + str(len(insertDeffer)) + "     " + "修改多语言数量：" + str(
                len(updateDefferDict)) + "       删除多语言数量" + str(len(delDeffer)))

            insertNoneKeys = []
            updateNoneKeys = []
            ##验证新增
            for key in insertDeffer:
                if lokaliseDict[key] == None:
                    insertNoneKeys.append(key)
            if len(insertNoneKeys) != 0:
                endPrintList.append(
                    startColorRed + localFileName + "新增多语言中包含空值 keys=" + endColor + startColorYellow + str(
                        insertNoneKeys) + endColor)

            ##验证修改
            for key in updateDefferDict:
                if lokaliseDict[key] == None:
                    updateNoneKeys.append(key)

            if len(updateNoneKeys) != 0:
                endPrintList.append(
                    startColorRed + localFileName + "修改多语言中包含空值 keys=" + endColor + startColorYellow + str(
                        updateNoneKeys) + endColor)

    ##文件copy
    for item in endPrintList:
        print(item)
    localZhTree = ET.parse(localFilePath).getroot()

    # 执行copy
    for key in fileDirMapping:
        localFileName = fileDirMapping[key]
        localFilePath = os.path.join(lokalStrValues, localFileName, "strings.xml")
        if not os.path.exists(os.path.join(lokalStrValues, localFileName)):
            os.mkdir(os.path.join(lokalStrValues, localFileName))
        lokaliseFilePath = os.path.join(lokalisePath, key, "strings.xml")
        shutil.copyfile(lokaliseFilePath, localFilePath)

    ### 本地多语言校验脚本运行
    matchList = ["%1$d", "%1$s", "%2$d", "%2$s", "%3$d", "%3$s", "%4$d", "%4$s", "%5$d", "%5$s"]

    # values-zh-rCN 记录zh中的占位符数量
    # 多个百分号的问题
    print("横向对比计算占位符差异")
    countryPlaceHolder = {}
    for countryKey in fileDirMapping:
        placeHolder = {}
        localZhPath = os.path.join(lokalStrValues, fileDirMapping[countryKey], "strings.xml")
        localZhDict = xmlTreeToDict(ET.parse(localZhPath).getroot())
        for key in localZhDict:
            value = localZhDict[key]
            if value != None and ("%1$d" in value or "%1$s" in value):
                valuePlaceHolder = []
                for match in matchList:
                    if match in value:
                        valuePlaceHolder.append(match)
                placeHolder[key] = str(valuePlaceHolder)
        countryPlaceHolder[countryKey] = placeHolder

    ## 差异
    lastHolder = {}
    lastKey = None
    for key in countryPlaceHolder:
        thisHolder = {}
        if len(lastHolder) == 0:
            lastHolder = countryPlaceHolder[key]
            lastKey = key
        else:
            thisHolder = countryPlaceHolder[key]
            differ = lastHolder.items() ^ thisHolder.items()
            differDict = dict(differ)
            if len(differDict) > 0:
                thisDifferList = []
                for differKey in differDict:
                    if differKey in thisHolder:
                        thisDifferList.append("key = " + differKey + " -- 占位符 = " + thisHolder.get(differKey))
                    else:
                        thisDifferList.append("key = " + differKey + " -- 无占位符")
                    if differKey in lastHolder:
                        thisDifferList.append("对比文件: " + lastKey + " -- 占位符 = " + lastHolder[differKey] + '\n')
                    else:
                        thisDifferList.append("对比文件: " + lastKey + " -- 无占位符\n")
                print("\n" + startColorRed + "校验文件:" + key + "  占位符异常数量" + str(len(differDict)) + endColor)
                for item in thisDifferList:
                    print(startColorRed + item + endColor)

    print("横向对比计算占位符差异结束")

    print("多语言校验脚本运行")
    list = os.listdir(lokalStrValues)

    strings = fileListFunc(lokalStrValues)
    for i in strings:
        findStringFromFile(i)
