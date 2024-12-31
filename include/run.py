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
from include.function import Tap, GoText, TimAnhSauKhiChupVaSoSanh, KetNoiPortThietBiTheoPort, OpenApp, UnInstallAppFile, KiemTraDangKyThanhCong, CapQuyenTruyCapChoFacebookLite
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, DemThoiGian
from include.datepicker import ChonNgayThangNamSinh, DumpMap
from include.setUpDevices import ThietLapThongSoThietbi
from include.getCookieToken import getAdbData

# from include.OpenApp import openBrave
# from include.OpenApp import getMailCode

saveText = {}
def RunLD(index, apk_path, package_name, ld_path_console):
    emailText = 'dyland.wolfram@moonapps.org'
    passText = '9dVhsUax@'
    fieldFirstName = 'John'
    fieldLastName = 'Tran'
    verifycode = '123456'
    # data = openBrave()
    # emailText = data.get("emailText")
    # passText = data.get("passText")
    # fieldFirstName = data.get("fieldFirstName")
    # fieldLastName = data.get("fieldLastName")
    # cookie_mi = data.get("MI")
    # cookie_phpsessid = data.get("PHPSESSID")
    # verifycode = getMailCode(cookie_mi, cookie_phpsessid)
    # print("Mã xác nhận:" ,verifycode)

    isSetup = ThietLapThongSoThietbi(index, ld_path_console)
    if(isSetup == True):
        pass

    isStarted = KhoiDongLDPlayer(index, ld_path_console)
    if(isStarted == True):
        pass

    isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
    if(isInstalled == True):
        pass

    # DemThoiGian(1)

    CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

    DemThoiGian(1)

    OpenApp(index)

    pos = TimAnhSauKhiChupVaSoSanh(Action.createbutton_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.getstarted_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1]) 

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.firstname3_Btn, index, ld_path_console)
    if(pos != None):
        GoText(index, ld_path_console, fieldFirstName, pos[0], pos[1])

    DemThoiGian(1)

    pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console)
    if(pos != None):
        GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])              

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    pos = TimAnhSauKhiChupVaSoSanh(Action.selectyourname_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])
        pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
        if(pos != None):
            Tap(index, ld_path_console, pos[0], pos[1])
        else:
            pass
    else:
        pass

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
    if(pos != None):
        ChonNgayThangNamSinh(index, ld_path_console)

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.signupWithEmail_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.clickWhatYourEmail_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])   

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.emailfield_Btn, index, ld_path_console)
    if(pos != None):
        GoText(index, ld_path_console, emailText, pos[0], pos[1])

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.clickcreatepassword_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)    

    pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console)
    if(pos != None):
        GoText(index, ld_path_console, passText, pos[0], pos[1])        

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.notnow_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.agree_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console)
    if(pos != None):
        GoText(index, ld_path_console, verifycode, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])  

    DemThoiGian(2)

    pos = TimAnhSauKhiChupVaSoSanh(Action.skip1_Btn, index, ld_path_console)
    if(pos != None):
        Tap(index, ld_path_console, pos[0], pos[1])

    DemThoiGian(2)                                              

    pos = TimAnhSauKhiChupVaSoSanh(Action.successReg3_Btn, index, ld_path_console)
    if(pos != None):
        isSuccess = KiemTraDangKyThanhCong(index, pos[0], pos[1])
        if(isSuccess == True):
            CookieToken = json.loads(getAdbData(index, ld_path_console))
            uid = CookieToken.get("uid")
            cookie = CookieToken.get("cookie")
            token = CookieToken.get("token")
            account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
            print(account)
            print(f"Chuẩn bị xóa cache và reboot LDPlayer {index}")
            DemThoiGian(3)
            RebootVaXoaCache(index, ld_path_console, ld_path_instance)

        

# if __name__ == "__main__":
#     RunLD(5555)