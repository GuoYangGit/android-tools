import re
from time import sleep

# 检验弹窗是否存在
import uiauto


# 校验邮箱格式
def email_format(device, gone):
    device(resourceId="com.relationship.rings:id/closeIv").click()
    view_gone = device(resourceId="com.relationship.rings:id/closeIv").wait_gone(timeout=1)
    if view_gone is not gone:
        device.screenshot('邮箱格式错误.png')


# 开始检测邮箱
def start_email():
    d = uiauto.start_app()
    mine_tab = d(resourceId="com.relationship.rings:id/btnTabMine")
    mine_tab.click()
    d(resourceId="com.relationship.rings:id/avatarIv").click()
    d.swipe_ext("up", 0.6)
    d(resourceId="com.relationship.rings:id/emailLayout").click()
    email_text = d(resourceId="com.relationship.rings:id/inputEt")
    sleep(0.5)
    email_text.clear_text()
    email_text.send_keys("sssdfsfsds")
    email_format(d, False)
    email_text.clear_text()
    email_text.send_keys("guoyanggit@gmail.com")
    email_format(d, True)


if __name__ == '__main__':
    start_email()
