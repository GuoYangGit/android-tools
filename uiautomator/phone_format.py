import re
from time import sleep

# Readme文档 https://github.com/openatx/uiautomator2/blob/master/README.md
# cmd输入weditor开启预览模式、用于获取界面UI信息
# python -m uiautomator2 init
import uiauto


# 区号选择测试
def phone_code_test(device, text):
    device(resourceId="com.relationship.rings:id/tvPhoneCode").click()
    edit = device(resourceId="com.relationship.rings:id/searchTxtId")
    edit.click()
    edit.send_keys(text)
    device.press("down")
    sleep(1)
    device(resourceId="com.relationship.rings:id/countryCodeTV", text=f"+{text}").click()


# 校验手机格式
def phone_format(device, text):
    is_us = device(resourceId="com.relationship.rings:id/tvPhoneCode").get_text() == "+1"
    et_phone = device(resourceId="com.relationship.rings:id/etMobilePhone")
    et_phone.send_keys(text)
    text = et_phone.get_text()
    if text is None:
        return
    if is_us:
        match = re.match(r'^\d*', et_phone.get_text())
    else:
        match = re.match(r'^\d[0-9| ]*', et_phone.get_text())
    if match is None:
        device.screenshot('格式化错误.png')


# 开始检验手机号
def start_phone():
    d = uiauto.start_app()
    phone = d(resourceId="com.relationship.rings:id/tvMobilePhone")
    phone.click()
    phone_format(d, "ds12~")
    phone_code_test(d, 1)
    phone_format(d, "17696051726")
    d(resourceId="com.relationship.rings:id/ivClean").click()
    sleep(0.5)
    phone_code_test(d, 86)
    phone_format(d, "17696051726")
    d(resourceId="com.relationship.rings:id/nextBtn").click()
    d(resourceId="com.relationship.rings:id/verifyCode").click()


if __name__ == '__main__':
    start_phone()
