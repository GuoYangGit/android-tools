import uiauto


def start_logout():
    d = uiauto.start_app()
    d(resourceId="com.relationship.rings:id/btnTabMine").click()
    d(resourceId="com.relationship.rings:id/settingLayout").click()
    d(resourceId="com.relationship.rings:id/signOutTv").click()
    d(resourceId="com.relationship.rings:id/confirmTv").click()


if __name__ == '__main__':
    start_logout()
