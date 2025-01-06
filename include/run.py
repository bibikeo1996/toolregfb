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
from include.function import DocFileExcel, XuLyNextButton, Tap, GoText, TimAnhSauKhiChupVaSoSanh, KetNoiPortThietBiTheoPort, OpenApp, UnInstallAppFile, KiemTraDangKyThanhCong, CapQuyenTruyCapChoFacebookLite
from include.OpenApp import KiemTraDaCaiAppFaceBookLiteChua, KhoiDongLDPlayer, DemThoiGian
from include.datepicker import ChonNgayThangNamSinh, DumpMap
from include.setUpDevices import ThietLapThongSoThietbi
from include.getCookieToken import getAdbData
from include.quitInstance import RebootVaXoaCache

# from include.OpenApp import openBrave
from data.getCode import getMailCode
from data.getCode import getDataInFileEmails
# file_path = 'D:\\Workspace\\toolregfb\\data.xlsx'
# emails, passwords, first_names, last_names = DocFileExcel(file_path)

# for i in range(len(emails)):
#     # RunLD(i, 'apk_path', 'package_name', 'ld_path_console', emails[i], passwords[i], first_names[i], last_names[i])
#     print(f"{emails[i]}, {passwords[i]}, {first_names[i]}, {last_names[i]}")

def RunLD(index, apk_path, package_name, ld_path_console, ld_path_instance):
    data = getDataInFileEmails(4)
    emailText = data["email"]
    passText = data["passWord"]
    fieldFirstName = data["firstName"]
    fieldLastName = data["lastName"]
    mi = data["mi"]
    phpsessid = data["phpsessid"]

    # emailText = "dofafe9582@pixdd.com"
    # passText = "9dVhsUax@"
    # fieldFirstName = "Tony"
    # fieldLastName = "Nguyen"
    # mi = data["mi"]
    # phpsessid = data["phpsessid"]
    print(f"Email: {emailText} - Pass: {passText} - First Name: {fieldFirstName} - Last Name: {fieldLastName} - MI: {mi} - PHPSESSID: {phpsessid}")
    # Tạo các flag để kiểm soát từng điều kiện

    # isStarted = RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance)
    # if(isStarted == True):
    #     isStarted = True
    #     pass

    isStarted = False
    createbutton_done = False
    getstarted_done = False
    firstname_done = False
    lastname_done = False
    selectyourname_done = False
    setDate_done = False
    sett_done = False
    gender_done = False
    signup_done = False
    email_done = False
    doyouhaveaccount_done = False
    password_done = False
    agree_done = False
    verifycode_done = False
    skip_done = False
    successReg_done = False
    notnow_done = False
    passwordField_done = False
    agree_done = False
    issue282_done = False
    okbtn_done = False

    saveText = {}
    while True:

        check = KhoiDongLDPlayer(index, ld_path_console)
        print(f"Check: {check}")
        quit()
        
        # Kiểm tra createbutton nếu chưa hoàn thành
        if not createbutton_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.createbutton_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                createbutton_done = True

        # Kiểm tra getstarted nếu chưa hoàn thành
        if not getstarted_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.getstarted_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                getstarted_done = True

        # Kiểm tra firstname nếu chưa hoàn thành
        if not firstname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.firstname3_Btn, index, ld_path_console)
            if pos is not None:
                GoText(index, ld_path_console, fieldFirstName, pos[0], pos[1])
                print("Đã nhập firstname")
                firstname_done = True

        # Kiểm tra lastname nếu chưa hoàn thành
        if not lastname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console)
            if pos is not None:
                GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])
                print("Đã nhập lastname")
                lastname_done = True

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next 1")

        # Kiểm tra selectyourname nếu chưa hoàn thành
        if not selectyourname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.selectyourname_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                selectyourname_done = True
                # Kiểm tra nextt nếu chưa hoàn thành
                if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                    print("Đã click Next 2")

        # Kiểm tra setDate nếu chưa hoàn thành
        if not setDate_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
            if pos is not None:
                ChonNgayThangNamSinh(index, ld_path_console)
                setDate_done = True

        # Kiểm tra sett nếu chưa hoàn thành
        if not sett_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                sett_done = True

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next 3")                

        # Kiểm tra gender nếu chưa hoàn thành
        if not gender_done:
            pos = TimAnhSauKhiChupVaSoSanh(random.choice([Action.female_Btn, Action.male_Btn]), index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                gender_done = True

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next 4")

        # Kiểm tra signup nếu chưa hoàn thành
        if not signup_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.signupWithEmail_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                signup_done = True

        # Kiểm tra email nếu chưa hoàn thành
        if not email_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.emailfieldv2_Btn, index, ld_path_console)
            if pos is not None:
                GoText(index, ld_path_console, emailText, pos[0], pos[1])
                email_done = True

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next 5")        

        # Kiểm tra doyouhaveaccount nếu chưa hoàn thành
        if not doyouhaveaccount_done:
            ### Chỗ này có max_attempts để tăng số lần kiểm tra Element (hiện tại là 1)
            ### Check_attempt=True là cho phép kiểm tra element
            pos = TimAnhSauKhiChupVaSoSanh(Action.doyouhaveaccount_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if pos is not None:
                pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    doyouhaveaccount_done = True

        # Kiểm tra password nếu chưa hoàn thành
        if not password_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.clickcreatepassword_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                password_done = True

        # Kiểm tra agree nếu chưa hoàn thành
        if not passwordField_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console)
            if(pos != None):
                GoText(index, ld_path_console, passText, pos[0], pos[1])                   

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next 6")

        if not notnow_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.notnow_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])  

        if not agree_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.agree_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])                    

        ## Kiểm tra có bị dính issue 282 nếu có thì reboot xóa cache chạy lại
        if not issue282_done:
            is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=5, check_attempt=True)
            if(is282 != None):
                issue282_done = True
                print(f"Email: {emailText} bị dính 282")
                DemThoiGian(2)
                RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance)

        # Kiểm tra verifycode nếu chưa hoàn thành
        if not verifycode_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console)
            if pos is not None:

                # Chỗ này phải đảm bảo verify code đã được lấy mới chạy tiếp
                verifycode = getMailCode(mi, phpsessid)
                if verifycode is None:
                    print("Không lấy được mã code == Reboot và xóa cache")
                    RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance)
                    return
                GoText(index, ld_path_console, verifycode, pos[0], pos[1])
                # DemThoiGian(30)
                verifycode_done = True
        
        if not okbtn_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])   
                okbtn_done = True 

        if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
            print("Đã click skip")


        if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
            print("Đã click skip lần 2") 


        if XuLyNextButton(index, ld_path_console, Action.skip1_Btn):
            print("Đã click skip lần 3")                        
             

        # Kiểm tra successReg nếu chưa hoàn thành
        if not successReg_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.successReg3_Btn, index, ld_path_console)
            if pos is not None:
                isSuccess = KiemTraDangKyThanhCong(index, pos[0], pos[1])
                if isSuccess:
                    CookieToken = json.loads(getAdbData(index, ld_path_console))
                    uid = CookieToken.get("uid")
                    cookie = CookieToken.get("cookie")
                    token = CookieToken.get("token")
                    account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
                    print(account)
                    print(f"Chuẩn bị xóa cache và reboot LDPlayer {index}")
                    DemThoiGian(3)
                    successReg_done = True
                    RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance)

        # Nếu tất cả các điều kiện đã hoàn thành, thoát khỏi vòng lặp
        if (createbutton_done and getstarted_done and firstname_done and lastname_done and nextt_done and
            selectyourname_done and setDate_done and sett_done and gender_done and signup_done and email_done and
            doyouhaveaccount_done and password_done and verifycode_done and successReg_done and notnow_done and passwordField_done and agree_done and issue282_done and okbtn_done):
            break
