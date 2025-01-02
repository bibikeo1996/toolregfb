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
from include.function import DocFileExcel, Tap, GoText, TimAnhSauKhiChupVaSoSanh, KetNoiPortThietBiTheoPort, OpenApp, UnInstallAppFile, KiemTraDangKyThanhCong, CapQuyenTruyCapChoFacebookLite
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, DemThoiGian
from include.datepicker import ChonNgayThangNamSinh, DumpMap
from include.setUpDevices import ThietLapThongSoThietbi
from include.getCookieToken import getAdbData
from include.quitInstance import RebootVaXoaCache
from include.checkLocation import KetNoiLDVaUiautomator, TheoDoiGiaoDien

# from include.OpenApp import openBrave
# from include.OpenApp import getMailCode
# file_path = 'D:\\Workspace\\toolregfb\\data.xlsx'
# emails, passwords, first_names, last_names = DocFileExcel(file_path)

# for i in range(len(emails)):
#     # RunLD(i, 'apk_path', 'package_name', 'ld_path_console', emails[i], passwords[i], first_names[i], last_names[i])
#     print(f"{emails[i]}, {passwords[i]}, {first_names[i]}, {last_names[i]}")

def RunLD(index, apk_path, package_name, ld_path_console, ld_path_instance):
    emailText = 'nelay69535@matmayer.com'
    passText = '9dVhsUax@'
    fieldFirstName = 'Henry'
    fieldLastName = 'DauBui'
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


    # RebootVaXoaCache(index, ld_path_console, ld_path_instance)

    # isSetup = ThietLapThongSoThietbi(index, ld_path_console)
    # if(isSetup == True):
    #     pass

    # isStarted = KhoiDongLDPlayer(index, ld_path_console)
    # if(isStarted == True):
    #     pass

    # isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
    # if(isInstalled == True):
    #     pass

    # # DemThoiGian(1)

    # CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

    DemThoiGian(2)

    OpenApp(index)
    
    isConnected = KetNoiLDVaUiautomator(index, ld_path_console)
    if isConnected:
        print("Kết nối thành công.")
        pass
    else:
        return

    keywords = ['Create new account', 'Log in', 'Forgot password?']
    isSuccess = TheoDoiGiaoDien(isConnected, keywords)
    if isSuccess:
        print("Create Account.")
        pos = TimAnhSauKhiChupVaSoSanh(Action.createbutton_Btn, index, ld_path_console)
        if(pos != None):
            Tap(index, ld_path_console, pos[0], pos[1])

    keywords = ['Get started', 'Find my account']
    isSuccess = TheoDoiGiaoDien(isConnected, keywords)
    if isSuccess:
        print("GetStarted.")
        pos = TimAnhSauKhiChupVaSoSanh(Action.getstarted_Btn, index, ld_path_console)
        if(pos != None):
            Tap(index, ld_path_console, pos[0], pos[1]) 

    keywords = ['First name', 'Last name']
    isSuccess = TheoDoiGiaoDien(isConnected, keywords)
    if isSuccess:
        print("What is your name.")
        pos = TimAnhSauKhiChupVaSoSanh(Action.firstname3_Btn, index, ld_path_console)
        if(pos != None):
            GoText(index, ld_path_console, fieldFirstName, pos[0], pos[1])

        DemThoiGian(2)

        pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console)
        if(pos != None):
            GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])   
        
    DemThoiGian(2)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # pos = TimAnhSauKhiChupVaSoSanh(Action.selectyourname_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])
    #     pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    #     if(pos != None):
    #         Tap(index, ld_path_console, pos[0], pos[1])
    #     else:
    #         pass
    # else:
    #     pass

    # DemThoiGian(2)    

    # pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
    # if(pos != None):
    #     ChonNgayThangNamSinh(index, ld_path_console)

    # DemThoiGian(2)
    
    # pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)
    
    # pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)
    
    # pos = TimAnhSauKhiChupVaSoSanh(random.choice([Action.female_Btn, Action.male_Btn]), index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)    

    # pos = TimAnhSauKhiChupVaSoSanh(Action.signupWithEmail_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)    

    # # pos = TimAnhSauKhiChupVaSoSanh(Action.clickWhatYourEmail_Btn, index, ld_path_console)
    # # if(pos != None):
    # #     Tap(index, ld_path_console, pos[0], pos[1])   

    # # DemThoiGian(2)    

    # pos = TimAnhSauKhiChupVaSoSanh(Action.emailfieldv2_Btn, index, ld_path_console)
    # if(pos != None):
    #     GoText(index, ld_path_console, emailText, pos[0], pos[1])

    # DemThoiGian(2)    

    # pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)    
    
    # pos = TimAnhSauKhiChupVaSoSanh(Action.doyouhaveaccount_Btn, index, ld_path_console)
    # if(pos != None):
    #     pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console)
    #     if(pos != None):
    #         Tap(index, ld_path_console, pos[0], pos[1])
    #     else:
    #         pass
    # else:
    #     pass
    
    # DemThoiGian(2)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.clickcreatepassword_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)    

    # pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console)
    # if(pos != None):
    #     GoText(index, ld_path_console, passText, pos[0], pos[1])        
        
    # DemThoiGian(2)   
     
    # pos = TimAnhSauKhiChupVaSoSanh(Action.nextt_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])    

    # DemThoiGian(2)   
     
    # pos = TimAnhSauKhiChupVaSoSanh(Action.notnow_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)
    

    # ## từ khúc button agree tốn khá nhiều giây khoản > 20s

    # pos = TimAnhSauKhiChupVaSoSanh(Action.agree_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(20)
    
    # ## cần tạo function để check verify code sau đó mới chạy tiếp chỗ này bắt buộc phải có verify code mới được xử lý code bên dưới 

    # # pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console)
    # # if(pos != None):
    # #     GoText(index, ld_path_console, verifycode, pos[0], pos[1])

    # DemThoiGian(5)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(2)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(5)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])  

    # DemThoiGian(5)

    # pos = TimAnhSauKhiChupVaSoSanh(Action.skip1_Btn, index, ld_path_console)
    # if(pos != None):
    #     Tap(index, ld_path_console, pos[0], pos[1])

    # DemThoiGian(5)                                              

    # pos = TimAnhSauKhiChupVaSoSanh(Action.successReg3_Btn, index, ld_path_console)
    # if(pos != None):
    #     isSuccess = KiemTraDangKyThanhCong(index, pos[0], pos[1])
    #     if(isSuccess == True):
    #         CookieToken = json.loads(getAdbData(index, ld_path_console))
    #         uid = CookieToken.get("uid")
    #         cookie = CookieToken.get("cookie")
    #         token = CookieToken.get("token")
    #         account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
    #         print(account)
    #         print(f"Chuẩn bị xóa cache và reboot LDPlayer {index}")
    #         DemThoiGian(3)
    #         RebootVaXoaCache(index, ld_path_console, ld_path_instance)


if __name__ == "__main__":
    RunLD(5555)