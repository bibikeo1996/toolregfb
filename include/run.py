import sys
import os
import subprocess
import cv2
import numpy as np
import time
import random
import string
import requests
import adb_shell
import json


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'defined'))
from dotenv import load_dotenv
from key import KeyCode, Action
from PIL import Image
from io import BytesIO


## import function
from include.function import Tap, SwipeMonth, SwipeDay, SwipeYear, GoText, TimAnhSauKhiChupVaSoSanh, KetNoiPortThietBiTheoPort, OpenApp, UnInstallAppFile, KiemTraDangKyThanhCong
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, TrangThaiInstance
from include.setUpDevices import ThietLapThongSoThietbi
from include.getCookieToken import getAdbData

saveText = {}
def RunLD(index, apk_path, package_name):
    emailText = 'npx58646@msssg.com'
    passText = '9dVhsUax@'
    fieldFirstName = 'Tim'
    fieldLastName = 'Xiao'

    # isSetup = ThietLapThongSoThietbi(index)
    # if(isSetup == True):
    #     TrangThaiInstance(index, f"Instance {index} đã setup xong", saveText)
    #     pass
    # time.sleep(1)


    # isStarted = KhoiDongLDPlayer(index)
    # if(isStarted == True):
    #     TrangThaiInstance(index, f"Instance {index} đã khởi động xong", saveText)
    #     pass

    # isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path)
    # if(isInstalled == True):
    #     TrangThaiInstance(index, f"Instance {index} đã cài xong app", saveText)
    #     pass

    # OpenApp(index) 

    # time.sleep(1.5)

    buttons = [
        # (Action.createbutton_Btn, "Tap", None),
        # (Action.getstarted_Btn, "Tap", None),
        # (Action.defaultClick_btn, "Tap", None),
        # (Action.firstname_Btn, "GoText", fieldFirstName),
        # (Action.lastname_Btn, "GoText", fieldLastName),
        # (Action.nextt_Btn, "Tap", None),
        # (Action.selectyourname_Btn, "Tap", None),
        # (Action.nextt_Btn, "Tap", None),
        # (Action.month_Btn, "SwipeMonth", None),
        # (Action.date_Btn, "SwipeDay", None),
        # (Action.year_Btn, "SwipeYear", None),
        # (Action.sett_Btn, "Tap", None),
        # (Action.nextt_Btn, "Tap", None),
        # (random.choice([Action.female_Btn, Action.male_Btn]), "Tap", None),
        # (Action.deny_Btn, "Tap", None),
        # (Action.signupWithEmail_Btn, "Tap", None),
        # (Action.clickWhatYourEmail_Btn, "Tap", None),
        # (Action.emailfield_Btn, "GoText", emailText),
        # (Action.nextt_Btn, "Tap", None),
        # (Action.clickcreatepassword_Btn, "Tap", None),
        # (Action.passwordField_Btn, "GoText", passText),
        # (Action.nextt_Btn, "Tap", None),
        # (Action.notnow_Btn, "Tap", None),
        # (Action.agree_Btn, "Tap", None),
        # (Action.deny_Btn, "Tap", None),
        # (Action.verifycodefield_Btn, "GoText", "verifycode"),
        # (Action.ok_Btn, "Tap", None),
        # (Action.skip_Btn, "Tap", None),
        # (Action.skip_Btn, "Tap", None),
        # (Action.skip1_Btn, "Tap", None),
        # (Action.successReg_Btn, "KiemTraDangKyThanhCong", None),
        # (Action.successReg2_Btn, "KiemTraDangKyThanhCong", None),
        (Action.successReg3_Btn, "KiemTraDangKyThanhCong", None),
    ]

    for button, action, text in buttons:
        btn_location = TimAnhSauKhiChupVaSoSanh(button, index)
        if btn_location:
            if action == "Tap":
                Tap(index, btn_location[0], btn_location[1])
            elif action == "GoText":
                GoText(index, text, btn_location[0], btn_location[1])
            elif action == "SwipeMonth":
                SwipeMonth(index, btn_location[0], btn_location[1])
            elif action == "SwipeDay":
                SwipeDay(index, btn_location[0], btn_location[1])
            elif action == "SwipeYear":
                SwipeYear(index, btn_location[0], btn_location[1])
            elif action == "KiemTraDangKyThanhCong":
                isSuccess = KiemTraDangKyThanhCong(index, btn_location[0], btn_location[1])
                if(isSuccess == True):
                    TrangThaiInstance(index, f"Instance {index} đã đăng ký thành công", saveText)
                    ## Format Data
                    TrangThaiInstance(index, f"Instance {index} đang lấy Cookie", saveText)
                    CookieToken = json.loads(getAdbData(index))
                    uid = CookieToken.get("uid")
                    cookie = CookieToken.get("cookie")
                    token = CookieToken.get("token")
                    account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
                    # uid|pass|cookie|token|email
                    print(account)
                    pass
            time.sleep(1)
        
        

# if __name__ == "__main__":
#     RunLD(5555)