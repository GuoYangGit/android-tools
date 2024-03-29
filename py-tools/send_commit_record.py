# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/6/16-3:17 PM
@Desc: 飞书发送提交记录脚本
"""

import os
import sys
import requests
import json

# 项目地址
gitPath = "/Users/axl/AndroidStudioProjects/Crust-Chatjoy/dhn-android-Crust-Chatjoy/ChatJoy"
# 上次提交记录存储地址
lastIdFilePath = "/Users/axl/AndroidStudioProjects/Crust-Chatjoy/dhn-android-Crust-Chatjoy/lastCommitId"

git_get_count_cmd = "git rev-list HEAD --count"

git_get_last_commit_log = "git log -1 --pretty=oneline"

docTag = "[doc]"


# 从git记录中提取commit ID
def getCommitIdFromLine(line):
    return line.split(" ")[0]


def createLastCommitFile():
    with open(lastIdFilePath, "w") as file:
        file.write("0")
    return "0"


def getLastCommitCount() -> str:
    is_exists = os.path.exists(lastIdFilePath)
    print("getLastCommitIdFromFile,isExists:", is_exists)
    if is_exists:
        file = open(lastIdFilePath, 'r+', encoding="utf-8")
        commit_count = file.read()
        file.close()
        return commit_count
    else:
        count = createLastCommitFile()
        return count


def getMidGitLog(lastCount):
    currentCount = os.popen(f"cd {gitPath} && " + git_get_count_cmd).read()
    midCount = int(currentCount) - int(lastCount)
    logsResult = os.popen(
        f"cd {gitPath} && git log " + "-" + str(midCount) + " --oneline")
    res = logsResult.read()
    logsResult.close()
    return res


def getFormatCommitText(last_count) -> str:
    res = getMidGitLog(last_count)
    commitArr = []
    for line in res.splitlines():
        if line.find(docTag) != -1:
            commitArr.append(line)

    print("需要组织成文字的提交", commitArr)
    if len(commitArr) == 0:
        print("没有需要展示的提交记录")
        sys.exit()

    commitText = ""
    index = 0
    while index < len(commitArr):
        commitText += '%d' % (index + 1) + "."
        commitMessage = commitArr[index]
        commitText += commitMessage[commitMessage.find(docTag) + len(docTag):]
        commitText += "\n"
        index += 1

    return commitText


def sendMsgByRoboto(text, lastCommitId):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/e0e767c9-907a-4e9d-94d8-e8ca19db9519"

    headers = {"Content-Type": "application/json"}

    sendText = "commit_id:" + lastCommitId + "\n" + text

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "更新记录:",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": sendText
                            }
                        ]
                    ]
                }
            }
        }
    }

    # print("sendText", sendText)
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print("发送机器人", r.status_code)
    return r.status_code


# def getLastGitCommitId():
#     logsResult = os.popen(f"cd {gitPath} && git log -1 --oneline")
#     return logsResult.read().split(" ")[0]+"\n"


def saveLastCommitId(lastId):
    os.remove(lastIdFilePath)
    f = open(lastIdFilePath, "w", encoding='utf8')
    f.write(lastId)
    f.close()
    print("saveid:", lastId)


last_count = getLastCommitCount()
if not last_count:
    print("没有拿到上次提交记录id")
    sys.exit()

print("上次打包的count", last_count)
formatCommitText = getFormatCommitText(last_count)
print("即将展示的记录文案", formatCommitText)
lastCommitId = os.popen(
    f"cd {gitPath} && git log -1 --pretty=oneline").read()[:40]
print("lastCommitId:", lastCommitId)
status_code = sendMsgByRoboto(formatCommitText, lastCommitId)

if status_code == 200:
    currentCount = os.popen(f"cd {gitPath} && " + git_get_count_cmd).read()
    saveLastCommitId(str(currentCount))
