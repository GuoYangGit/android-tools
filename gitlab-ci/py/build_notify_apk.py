# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/11/1-16:34
@Desc: 打包并且上传fir、飞书通知脚本
"""
import apk_utils
import feishu
import fir

if __name__ == '__main__':
    apk_utils.build_apk()
    fir.init()
    feishu.init()
