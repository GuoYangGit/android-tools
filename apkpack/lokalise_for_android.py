# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/6/16-3:17 PM
@Desc: 拉取多语言脚本(lokalise)
"""

import xml.etree.ElementTree as ET
import os
import shutil
import re
import logging

# 本地资源地址
localStrPath = "/Users/yz/DHNProjects/LamourApp/app/src/main/res/"

# 本地存储目录
lokalisePath = "/Users/yz/IntelliJIDEAProjects/script/lokalise"

# lokalise token
token = "83bb3cc3d8c32aa14b254421f21ead2f51b31f4d"

# lokalise projectId
projectId = "4205512460e6db01add0a6.69814144"

# 文件名映射  远端名称:本地名称
fileDirMapping = {
    'values': 'values-zh-rCN',
    'values-en': 'values',
    'values-ar': 'values-ar',
    'values-de': 'values-de',
    'values-es': 'values-es',
    'values-fr': 'values-fr',
    'values-hi': 'values-hi-rIN',
    'values-id': 'values-in',
    'values-it': 'values-it',
    'values-ms': 'values-ms-rMY',
    'values-pt-rBR': 'values-pt',
    'values-ru': 'values-ru',
    'values-th': 'values-th-rTH',
    'values-tr': 'values-tr-rTR',
    'values-vi': 'values-vi-rVN',
    'values-zh-rHK': 'values-zh-rHK',
    'values-zh-rTW': 'values-zh-rTW'
}

# lokalise 执行命令拼接
lokalise2Cmd = f'lokalise2 \
    --token {token} \
    --project-id  {projectId} \
    file download \
    --format xml \
    --all-platforms android \
    --export-sort first_added \
    --unzip-to {lokalisePath}'


# 循环遍历String.xml
def xmlTreeToDict(xmlTree):
    xmlMap = {}
    for item4 in xmlTree.findall('string'):
        xmlMap[item4.get('name')] = item4.text

    return xmlMap


# 从lokalise拉取多语言文件
def lokalise():
    print("lokalise网络文件拉取中....")
    # 执行lokalise命令
    cmdResult = os.popen(lokalise2Cmd).read()
    # 输出lokalise命令返回
    print(cmdResult)
    if "Unzipping to" in cmdResult.split('\n')[-2]:
        print("拉取成功!!!")
    else:
        print("拉取失败!!!")
        exit()


# 计算lokalise拉取与本地的差异
def diffMapping():
    localRes = os.listdir(localStrPath)
    for fileName in fileDirMapping:
        # 遍历映射字典
        localFileName = fileDirMapping[fileName]
        if localFileName in localRes:

            localFilePath = os.path.join(localStrPath, localFileName, "strings.xml")
            localDict = xmlTreeToDict(ET.parse(localFilePath).getroot())

            lokaliseFilePath = os.path.join(lokalisePath, fileName, "strings.xml")
            lokaliseDict = xmlTreeToDict(ET.parse(lokaliseFilePath).getroot())

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

            print(f'文件名：{localFileName} "新增多语言数量：{str(len(insertDeffer))} '
                  f'修改多语言数量：{str(len(updateDefferDict))} '
                  f'删除多语言数量：{str(len(delDeffer))}')

            insertNoneKeys = []
            updateNoneKeys = []
            # 验证新增
            for insert in insertDeffer:
                if lokaliseDict[insert] is None:
                    insertNoneKeys.append(insert)
            if len(insertNoneKeys) != 0:
                logging.warning(localFileName + "新增多语言中包含空值 keys=" + str(insertNoneKeys))
            # 验证修改
            for update in updateDefferDict:
                if lokaliseDict[update] is None:
                    updateNoneKeys.append(update)
            if len(updateNoneKeys) != 0:
                logging.warning(localFileName + "修改多语言中包含空值 keys=" + str(updateNoneKeys))


# 执行copy
def copyFileToLocal():
    for fileName, localName in fileDirMapping.items():
        localFile = os.path.join(localStrPath, localName, "strings.xml")
        if not os.path.exists(os.path.join(localStrPath, localName)):
            os.mkdir(os.path.join(localStrPath, localName))
        lokaliseFile = os.path.join(lokalisePath, fileName, "strings.xml")
        shutil.copyfile(lokaliseFile, localFile)


# 如果百分号前是数字,则忽略
def isNum(s):
    arrays = s.split("%")
    for arr in arrays:
        beforeStr = arr[len(arr) - 2:len(arr) - 1]
        if beforeStr.isnumeric():
            return True
    return False


# 获取xml中的placeHolder  key:[placeHolders]
def matchStr(s):
    count = s.count("%")
    matchCount = 0
    if count > 0:
        for _ in re.findall(r'%\d[$][sd]', s):
            matchCount = matchCount + 1
    if count != matchCount and not isNum(s):
        logging.warning(s.strip())
        return False
    return True


# 用来匹配 特殊字符
def matchAsc(content):
    if re.match(r'[&#]', content) is not None:
        logging.warning("matchAsc:", content.strip())
        return False
    return True


def findStringFromFile(strFile):
    with open(strFile, encoding="utf8", errors="ignore") as content:
        lines = content.readlines()
        errCount = 0
        for line in lines:
            if not matchStr(line):
                errCount += 1
            if not matchAsc(line):
                print(strFile)


# 获取所有strings
def fileListFunc(filePathList):
    fileList = []
    for top, dirs, files in os.walk(filePathList):
        for fileStr in files:
            if str(fileStr).endswith('strings.xml') > 0:
                fileList.append(os.path.join(top, fileStr))

    return fileList


# 写入文件前进行过滤
def filterWriteFile(strFile):
    tree = ET.parse(strFile)
    root = tree.getroot()
    for document in root.findall('string'):
        name = document.get('name')
        if len(name) == 0:
            logging.warning(f'key name为空: {document.text}')
            root.remove(document)
            continue
        if re.search(r'\W|^_', name) is not None:
            logging.warning(f'有问题的key为: {name}')
            root.remove(document)
            continue
        for match in re.findall(r'%\d[$][@]', str(document.text)):
            logging.warning(f'占位符有问题的key: {name},value: {document.text}')
            document.text = document.text.replace(str(match), match[0:3] + 's')

    tree.write(strFile, encoding="UTF-8", xml_declaration=True)


# 多个百分号的问题
def diffLocal():
    print("横向对比计算占位符差异")
    currentPlaceHolder = {}
    for _, fileValue in fileDirMapping.items():
        placeHolder = {}
        localFilePath = os.path.join(localStrPath, fileValue, "strings.xml")
        localStrDict = xmlTreeToDict(ET.parse(localFilePath).getroot())
        for key, value in localStrDict.items():
            if value is None:
                continue
            valuePlaceHolder = []
            results = re.findall(r'%\d[$][sd@]', value)
            for result in results:
                valuePlaceHolder.append(result)
                placeHolder[key] = str(valuePlaceHolder)
                currentPlaceHolder[fileValue] = placeHolder

    # 差异
    lastHolder = {}
    lastKey = None
    for key, value in currentPlaceHolder.items():
        if len(lastHolder) == 0:
            lastKey = key
            lastHolder = value
        else:
            differDict = dict(lastHolder.items() ^ value.items())
            thisDifferList = []
            for differKey in differDict:
                if differKey in value:
                    thisDifferList.append(f'key = {differKey} -- 占位符 = {value.get(differKey)}')
                else:
                    thisDifferList.append(f'key = {differKey} -- 无占位符')
                if differKey in lastHolder:
                    thisDifferList.append(f'对比文件: {lastKey} -- 占位符 = {lastHolder[differKey]}\n')
                else:
                    thisDifferList.append(f'对比文件: {lastKey} -- 无占位符\n')
            logging.warning(f'\n校验文件:{key} 占位符异常数量:{str(len(differDict))}')
            for item in thisDifferList:
                logging.warning(item)
    print("横向对比计算占位符差异结束")


if __name__ == '__main__':
    # 从lokalise拉取多语言
    lokalise()
    # 计算差异
    diffMapping()
    # 从lokalise复制到项目
    copyFileToLocal()
    # 横向对比计算占位符差异
    diffLocal()
    print("开始检查项目中的String文件格式并替换")
    for currentKey, currentValue in fileDirMapping.items():
        localStrFile = os.path.join(localStrPath, currentValue, "strings.xml")
        filterWriteFile(localStrFile)
    print("多语言校验脚本运行")
    stringFiles = fileListFunc(localStrPath)
    for file in stringFiles:
        findStringFromFile(file)
