# 获取上次的打包时的commitID

import os
import sys
import requests
import json

# 这里为本人用户名
userName = ""
# TODO 这里为飞书群机器人的url地址
robotUrl = "https://open.feishu.cn/open-apis/bot/v2/hook/9be69e1b-1286-4962-b74d-239581bb39d8"
# TODO 这里为个人项目app模块路径
gitPath = "/Users/yz/IntelliJIDEAProjects/LamourApp/app"
# 记录上次提交记录count的文件
lastIdFilePath = gitPath + "/lastCommitId"
# git获取最新提交记录count指令
git_get_count_cmd = "git rev-list HEAD --count"
# 通过标签来进行提交内容拼接
docTag = "[doc]"


# git_get_last_commit_log = "git log -1 --pretty=oneline"


# 从git记录中提取commit ID
def getCommitIdFromLine(line):
    return line.split(" ")[0]


# 创建上次提交记录文件
def createLastCommitFile():
    file = open(lastIdFilePath, "w")
    file.write("0")
    file.close()
    return "0"


# 获取上次提交记录ID
def getLastCommitCount() -> str:
    is_exists = os.path.exists(lastIdFilePath)
    print("获取上次提交记录ID,文件是否存在:", is_exists)
    if is_exists:
        file = open(lastIdFilePath, 'r+', encoding="utf-8")
        commit_count = file.read()
        file.close()
        return commit_count
    else:
        count = createLastCommitFile()
        return count


# 获取上次提交记录与最新提交记录之间的提交内容
def getMidGitLog(lastCount):
    currentCount = os.popen(f"cd {gitPath} && " + git_get_count_cmd).read()
    midCount = int(currentCount) - int(lastCount)
    logsResult = os.popen(
        f"cd {gitPath} && git log " + "-" + str(midCount) + " --oneline")
    res = logsResult.read()
    logsResult.close()
    return res


# 获取上次提交记录内容
def getFormatCommitText(lastCount) -> str:
    res = getMidGitLog(lastCount)
    commitArr = []
    print("需要组织成文字的提交", res)
    for line in res.splitlines():
        if line.find(docTag) != -1:
            commitArr.append(line)
    if len(commitArr) == 0:
        print("没有需要展示的提交记录")
        sys.exit()

    commitText = ""
    index = 0
    while index < len(commitArr):
        commitText += '%d' % (index + 1) + "."
        commitMessage = commitArr[index].split(" ", 1)[1].replace(" ", "")
        commitText += commitMessage[commitMessage.find("]") + 1:]
        commitText += "\n"
        index += 1

    return commitText


# 发送给飞书机器人
def sendMsgByRoboto(text, lastCommitID):
    headers = {"Content-Type": "application/json"}

    sendText = "commit_id:" + lastCommitID + "\n" + text

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
                                "text": userName + sendText,
                            },
                            {
                                "tag": "a",
                                "text": "下载地址",
                                "href": "https://test.pengpengla.com/android/lamour.html"
                            }
                        ]
                    ]
                }
            }
        }
    }

    r = requests.post(robotUrl, headers=headers, data=json.dumps(data))
    print("发送机器人", r.status_code)
    return r.status_code


# def getLastGitCommitId():
#     logsResult = os.popen(f"cd {gitPath} && git log -1 --oneline")
#     return logsResult.read().split(" ")[0]+"\n"

# 保存最后一次的提交记录
def saveLastCommitId(lastId):
    f = open(lastIdFilePath, "w", encoding='utf8')
    f.write(lastId)
    f.close()
    print("saveid:", lastId)


if __name__ == '__main__':
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
    # saveLastCommitId(str(currentCount))
