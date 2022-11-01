# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/11/1-15:47
@Desc: 飞书通知脚本
"""
import json

import requests
import fir
import constant

# TODO 这里需要根据自己项目进行改写
# 机器人应用id
app_id = constant.app_id
# 机器人应用secret
app_secret = constant.app_secret
# 机器人webhook
web_hook = constant.web_hook
# @人的id，可以在网页版飞书进行查看
at_guo_yang = constant.at_guo_yang


# 获取飞书token
def get_token():
    req_data = {
        'app_id': app_id,
        'app_secret': app_secret,
    }
    req = requests.post(url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=req_data)
    return req.json()['tenant_access_token']


# 发送飞书消息 https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN?lang=zh-CN#f62e72d5
def send_message(apk_data):
    headers = {"Content-Type": "application/json"}
    req_data = {
        'msg_type': 'post',
        'content': {
            'post': {
                'zh_cn': {
                    'title': f'{apk_data["name"]}-Android打包完成',
                    'content': [
                        [{
                            'tag': 'text',
                            'text': f'版本号:{apk_data["build"]}({apk_data["version"]})\n',
                        }, {
                            'tag': 'text',
                            'text': f'更新日志:\n{apk_data["changelog"]}',
                        }, {
                            'tag': 'a',
                            'text': '下载链接\n',
                            'href': apk_data["install_url"]
                        },
                            {
                                'tag': 'at',
                                'user_id': at_guo_yang
                            }
                        ]
                    ]
                }
            }
        }
    }
    req = requests.post(url=web_hook, data=json.dumps(req_data), headers=headers)
    return req


# 真正执行方法
def init():
    # 通过fir获取apk相关信息
    data = fir.fir_apk_url().json()
    print(data)
    token = send_message(data)
    print(token)


if __name__ == '__main__':
    init()
