# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/11/1-14:40
@Desc: fir.im相关操作
@Link:
"""

import requests
import urllib3
import apk_utils
import constant
from urllib3.exceptions import InsecureRequestWarning

# TODO 这里需要根据自己项目进行改写
fir_bundle_id = constant.fir_bundle_id
# fir上面自己的token
fir_api_token = constant.fir_api_token


# fir获取Token https://www.betaqr.com/docs/publish
def fir_token():
    req_data = {
        'type': 'android',
        'bundle_id': fir_bundle_id,
        'api_token': fir_api_token,
    }
    req = requests.post(url='http://api.bq04.com/apps', data=req_data)
    return req


# fir获取apk信息 https://www.betaqr.com/docs/version_detection
def fir_apk_url():
    req = requests.get(url=f'http://api.bq04.com/apps/latest/{fir_bundle_id}?api_token={fir_api_token}&type=android')
    return req


# fir上传apk https://www.betaqr.com/docs/publish
def update_apk(req_apk_path, req_data):
    print(f'开始上传Apk,上传信息为:{req_data}')
    file = {'file': open(req_apk_path, 'rb')}
    param = {
        'key': req_data['key'],
        'token': req_data['token'],
        'x:name': req_data['apk_name'],
        'x:version': req_data['version_code'],
        'x:build': req_data['version_name'],
        'x:changelog': req_data['changelog'],
    }
    urllib3.disable_warnings(InsecureRequestWarning)
    req = requests.post(url=req_data['upload_url'], files=file, data=param, verify=False)
    return req


# 真正执行方法
def init():
    # 获取apk路径
    apk_path = apk_utils.get_apk_file()
    # 获取apk详情信息
    data = apk_utils.get_apk_info(apk_path)
    # 获取fir的token
    response = fir_token().json()['cert']['binary']
    data['key'] = response['key']
    data['token'] = response['token']
    data['upload_url'] = response['upload_url']
    data['changelog'] = apk_utils.git_change()
    # 开始上传apk
    result = update_apk(apk_path, data)
    print('上传成功')


if __name__ == '__main__':
    init()
