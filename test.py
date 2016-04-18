#! /usr/bin/env python

import re
import sys
import os
import unittest
import time

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

class LaunchBrowser(unittest.TestCase):
    def setUp(self):
        self.device, self.serialno = ViewClient.connectToDeviceOrExit()
    def test_LaunchBrowser(self):
            print("Back to home")
            self.device.press('KEYCODE_BACK')
            self.device.press('KEYCODE_HOME')
            self.device.press('KEYCODE_HOME')
            self.device.press('KEYCODE_BACK')
            VPS = "javascript:alert(document.getElementsByTagName('html')[0].innerHTML);"
            USE_BROWSER = False
            if USE_BROWSER:
                package = 'com.android.browser'
                activity = '.BrowserActivity'
                _id = 'id/no_id/12'
            else:
                package = 'com.android.chrome'
                activity = 'com.google.android.apps.chrome.Main'
                _id = 'id/no_id/28'
            component = package + "/" + activity
            uri = 'http://dtmilano.blogspot.com'


            print("Open Browser")
            self.device.startActivity(component=component, uri=uri)
            print("Waite for 5 sec")
            ViewClient.sleep(5)

            vc = ViewClient(device=self.device, serialno=self.serialno)
            sdkVersion = vc.getSdkVersion()
            print("Get SDK Version:"+str(sdkVersion))

            if sdkVersion > 10:
                print("Show search bar")
                self.device.drag((240, 180), (240, 420), 1, 20)
            else:
                for i in range(10):
                    self.device.press('KEYCODE_DPAD_UP')
                    ViewClient.sleep(1)
            print("Delete search bar")
            self.device.press('KEYCODE_DEL')
            ViewClient.sleep(1)

            print("Input JS and go")
            self.device.type(VPS)
            ViewClient.sleep(1)
            self.device.press('KEYCODE_ENTER')
            ViewClient.sleep(3)
            print("dump ViewClient data")
            vc.dump()
            print vc.findViewByIdOrRaise('com.android.chrome:id/js_modal_dialog_message' if sdkVersion >= 16 else 'id/message').getText().replace('\\n', "\n")
            self.device.press('KEYCODE_BACK' if sdkVersion > 10 else 'KEYCODE_ENTER')
            ViewClient.sleep(1)

class LaucnAPP(unittest.TestCase):
    def setUp(self):
        self.device, self.serialno = ViewClient.connectToDeviceOrExit()

    def test_LaunchDemoAPI(self):
        device, serialno = ViewClient.connectToDeviceOrExit()
        print("Back to home")
        self.device.press('KEYCODE_BACK')
        self.device.press('KEYCODE_HOME')
        self.device.press('KEYCODE_HOME')
        self.device.press('KEYCODE_BACK')

        FLAG_ACTIVITY_NEW_TASK = 0x10000000
        # 09-06 01:01:34.964: I/ActivityManager(873): START {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10200000 cmp=com.example.android.apis/.ApiDemos bnds=[784,346][880,442]} from pid 991
        componentName = 'com.example.android.apis/.ApiDemos'
        print("Open DemoAPI")
        device.startActivity(component=componentName, flags=FLAG_ACTIVITY_NEW_TASK)

        ViewClient.sleep(5)
        vc = ViewClient(device=device, serialno=serialno)
        app = vc.findViewWithText('App')
        if app:
            app.touch()
            ViewClient.sleep(1)
            # windows changed, request a new dump
            print("Find Alert Dialogs")
            vc.dump()
            ad = vc.findViewWithText('Alert Dialogs')
            if ad:
                ad.touch()
                ViewClient.sleep(1)
                # windows changed, request a new dump
                print("find List dialog")
                vc.dump()
                ld = vc.findViewWithText('List dialog')
                if ld:
                    ld.touch()
                    ViewClient.sleep(1)
                    # windows changed, request a new dump
                    print("Find Command three")
                    vc.dump()
                    c3 = vc.findViewWithText('Command three')
                    if c3:
                        c3.touch()
                        ViewClient.sleep(1)
                        device.press('KEYCODE_BACK')
                    else:
                        print >> sys.stderr, "Cannot find 'Command three'"
                else:
                    print >> sys.stderr, "Cannot find 'List dialog'"
            else:
                print >> sys.stderr, "Cannot find 'Alert Dialogs'"
        else:
            print >> sys.stderr, "Cannot find 'App'"

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LaunchBrowser)
    unittest.TextTestRunner(verbosity=2).run(suite)
    time.sleep(5)
    suite = unittest.TestLoader().loadTestsFromTestCase(LaucnAPP)
    unittest.TextTestRunner(verbosity=2).run(suite)