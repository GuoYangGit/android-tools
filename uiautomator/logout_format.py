# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/6/16-3:17 PM
@Desc: 自动化测试：登陆验证
"""

import uiauto


def start_logout():
    d = uiauto.start_app()
    d(resourceId="com.relationship.rings:id/btnTabMine").click()
    d(resourceId="com.relationship.rings:id/settingLayout").click()
    d(resourceId="com.relationship.rings:id/signOutTv").click()
    d(resourceId="com.relationship.rings:id/confirmTv").click()


if __name__ == '__main__':
    start_logout()
