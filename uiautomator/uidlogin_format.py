# !/usr/bin/python3
# coding:utf-8

"""
@Name: yang.guo
@Date: 2022/6/16-3:17 PM
@Desc: 自动化测试：账号密码登陆
"""

from time import sleep
import uiauto


def uid_login():
    d = uiauto.start_app()
    d(resourceId="com.relationship.rings:id/logoTitleIV").click()
    d.xpath('//*[@resource-id="com.relationship.rings:id/recyclerView"]/android.widget.LinearLayout[4]').click()
    d(resourceId="com.relationship.rings:id/userIdEd").click()
    d(resourceId="com.relationship.rings:id/userIdEd").set_text("123456")
    d(resourceId="com.relationship.rings:id/passwdEd").set_text("123456")
    d(resourceId="com.relationship.rings:id/clRoot").click()
    d(resourceId="com.relationship.rings:id/loginTv").click()


if __name__ == '__main__':
    uid_login()
