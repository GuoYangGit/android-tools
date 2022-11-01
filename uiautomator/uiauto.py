# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/6/16-3:17 PM
@Desc: 自动化测试入口类
"""

import re
from time import sleep
import uiautomator2 as u2
import email_format

app_package_name = 'com.relationship.rings'


# 启动App
def start_app():
    device = u2.connect()
    print(device.info)
    device.app_stop(app_package_name)
    device.app_start(app_package_name)
    pid = device.app_wait(app_package_name)  # 等待应用运行, return pid(int)
    if not pid:
        print(f"{app_package_name} is not running")
    else:
        print(f"{app_package_name} pid is {pid}")
        print(device.app_current())
    return device


if __name__ == '__main__':
    email_format.start_email()
