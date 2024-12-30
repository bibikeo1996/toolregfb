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
from include.function import Tap, GoText, TimAnhSauKhiChupVaSoSanh, KetNoiPortThietBiTheoPort, OpenApp, UnInstallAppFile, KiemTraDangKyThanhCong
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, TrangThaiInstance
from include.datepicker import ChonNgayThangNamSinh, DumpMap
from include.setUpDevices import ThietLapThongSoThietbi
from include.getCookieToken import getAdbData

saveText = {}
def RunLD(index, apk_path, package_name, ld_path_console):
    emailText = 'dyland.wolfram@moonapps.org'
    passText = '9dVhsUax@'
    fieldFirstName = 'Hwee'
    fieldLastName = 'Oh'

    isSetup = ThietLapThongSoThietbi(index, ld_path_console)
    if(isSetup == True):
        TrangThaiInstance(index, f"Instance {index} đã setup xong", saveText)
        pass
    time.sleep(1)


    isStarted = KhoiDongLDPlayer(index)
    if(isStarted == True):
        TrangThaiInstance(index, f"Instance {index} đã khởi động xong", saveText)
        pass

    isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path)
    if(isInstalled == True):
        TrangThaiInstance(index, f"Instance {index} đã cài xong app", saveText)
        pass

    OpenApp(index) 

    # time.sleep(1)

    buttons = [
        (Action.createbutton_Btn, "Tap", None),
        (Action.getstarted_Btn, "Tap", None),
        # (Action.defaultClick_btn, "Tap", None),
        (Action.firstname3_Btn, "GoText", fieldFirstName),
        (Action.lastname_Btn, "GoText", fieldLastName),
        (Action.nextt_Btn, "Tap", None),
        (Action.selectyourname_Btn, "Tap", None, True),  # Thỉnh thoảng hiện
        (Action.nextt_Btn, "Tap", None),
        (Action.setDate_Btn, "ChonNgayThangNamSinh", None),
        (Action.sett_Btn, "Tap", None),
        (Action.nextt_Btn, "Tap", None),
        (random.choice([Action.female_Btn, Action.male_Btn]), "Tap", None),
        (Action.nextt_Btn, "Tap", None),
        (Action.deny_Btn, "Tap", None, True),  # Thỉnh thoảng hiện
        (Action.signupWithEmail_Btn, "Tap", None),
        (Action.clickWhatYourEmail_Btn, "Tap", None),
        (Action.emailfield_Btn, "GoText", emailText),
        (Action.nextt_Btn, "Tap", None),
        (Action.clickcreatepassword_Btn, "Tap", None),
        (Action.passwordField_Btn, "GoText", passText),
        (Action.nextt_Btn, "Tap", None),
        (Action.notnow_Btn, "Tap", None),
        (Action.agree_Btn, "Tap", None),
        (Action.deny_Btn, "Tap", None),
        (Action.verifycodefield_Btn, "GoText", "verifycode"),
        (Action.ok_Btn, "Tap", None),
        (Action.skip_Btn, "Tap", None),
        (Action.skip_Btn, "Tap", None),
        (Action.skip1_Btn, "Tap", None),
        # (Action.successReg_Btn, "KiemTraDangKyThanhCong", None),
        # (Action.successReg2_Btn, "KiemTraDangKyThanhCong", None),
        (Action.successReg3_Btn, "KiemTraDangKyThanhCong", None),
    ]

    for button, action, text, *optional in buttons:
        thinhthoang = optional[0] if optional else False  # Kiểm tra xem có phải "thỉnh thoảng hiện" không
        btn_location = TimAnhSauKhiChupVaSoSanh(button, index)

        if btn_location:
            if action == "Tap":
                Tap(index, btn_location[0], btn_location[1])
            elif action == "GoText":
                GoText(index, text, btn_location[0], btn_location[1])
            elif action == "ChonNgayThangNamSinh":
                ChonNgayThangNamSinh(index, ld_path_console)
            elif action == "KiemTraDangKyThanhCong":
                isSuccess = KiemTraDangKyThanhCong(index, btn_location[0], btn_location[1])
                if isSuccess:
                    TrangThaiInstance(index, f"Instance {index} đã đăng ký thành công", saveText)
                    TrangThaiInstance(index, f"Instance {index} đang lấy Cookie", saveText)
                    CookieToken = json.loads(getAdbData(index, ld_path_console))
                    uid = CookieToken.get("uid")
                    cookie = CookieToken.get("cookie")
                    token = CookieToken.get("token")
                    account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
                    print(account)
            time.sleep(1)
        elif thinhthoang:
            # Nếu button "thỉnh thoảng hiện" không tồn tại, bỏ qua
            print(f"Button {button} không tồn tại, bỏ qua.")
            continue

        
        

# if __name__ == "__main__":
#     RunLD(5555)