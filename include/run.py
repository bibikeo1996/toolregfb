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
from include.function import *
from include.OpenApp import *
from include.datepicker import *
from include.setUpDevices import *
from include.getCookieToken import *
from include.quitInstance import *

# from include.OpenApp import openBrave
from data.getCode import *
# file_path = 'D:\\Workspace\\toolregfb\\data.xlsx'
# emails, passwords, first_names, last_names = DocFileExcel(file_path)

# for i in range(len(emails)):
#     # RunLD(i, 'apk_path', 'package_name', 'ld_path_console', emails[i], passwords[i], first_names[i], last_names[i])
#     print(f"{emails[i]}, {passwords[i]}, {first_names[i]}, {last_names[i]}")

def RunLD(index, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath):
    emailText = TaoEmail()
    passText = ''.join(random.choice(string.ascii_letters) for i in range(15))
    fieldFirstName = getHoTenRandom(fileTxtPath+'ho.txt')  
    fieldLastName = getHoTenRandom(fileTxtPath+'ten.txt')
    # verifycode = None
    print(f"Email: {emailText}, Firstname: {fieldFirstName}, Lastname: {fieldLastName}, Pass: {passText}")
    # quit()

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
    issue282_done = False
    issue282_v1_done = False

    # New
    sStartLD = False
    isFacebookInstall_done = False
    isInvalidEmail_done = False    
    isInvalidBirth_done = False    
    isInvalidaccount_done = False

    # New register
    sendviaSMS_done = False
    sendViaEmail_done = False
    newEmail_done = False
    phonenumber_done = False
    continueCreate_done = False
    confirmviaemail_done = False
    nextviaEmail_done = False
    sendcodeviaSMS_done = False

    saveText = {}
    while True:
        
        isSetup = ThietLapThongSoThietbi(index, ld_path_console)
        if isSetup:
            print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")
        StartLD(index, ld_path_console)

        InstallFacebook(Action.isFacebookExist_Btn, index, ld_path_console, apk_path)

        CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

        OpenApp(Action.isOpenApp_Btn, index, ld_path_console, package_name)
        
        # Kiểm tra createbutton nếu chưa hoàn thành
        if not createbutton_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.createbutton_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                createbutton_done = True

        # time.sleep(2)

        # Kiểm tra getstarted nếu chưa hoàn thành
        if not getstarted_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.getstarted_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                getstarted_done = True

        # time.sleep(2)

        # Kiểm tra firstname nếu chưa hoàn thành
        if not firstname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.firstname3_Btn, index, ld_path_console)
            if pos is not None:
                GoText(index, ld_path_console, fieldFirstName, pos[0], pos[1])
                # print("Đã nhập firstname")
                pass
                firstname_done = True

        # time.sleep(2)

        # Kiểm tra lastname nếu chưa hoàn thành
        if not lastname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console)
            if pos is not None:
                GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])
                # print("Đã nhập lastname")
                pass
                lastname_done = True

        # time.sleep(2)

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            # print("Đã click Next 1")
            pass

        # Kiểm tra selectyourname nếu chưa hoàn thành
        if not selectyourname_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.selectyourname_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                selectyourname_done = True
                # Kiểm tra nextt nếu chưa hoàn thành
                if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                    # print("Đã click Next 2")
                    pass

        # time.sleep(2)

        # Kiểm tra setDate nếu chưa hoàn thành
        if not setDate_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
            if pos is not None:
                ChonNgayThangNamSinh(index, ld_path_console)
                setDate_done = True

        # time.sleep(2)

        # Kiểm tra sett nếu chưa hoàn thành
        if not sett_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                sett_done = True

        # time.sleep(2)

        if not isInvalidBirth_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidBirth_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(pos != None):
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            # print("Đã click Next 3")           
            pass     

        # time.sleep(2)

        # Kiểm tra gender nếu chưa hoàn thành
        if not gender_done:
            pos = TimAnhSauKhiChupVaSoSanh(random.choice([Action.female_Btn, Action.male_Btn]), index, ld_path_console)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                gender_done = True

        # time.sleep(2)

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            # print("Đã click Next 4")
            pass

        # time.sleep(2)

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            # print("Đã click Next 5")        
            pass

        # time.sleep(2)

        if not isInvalidEmail_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidEmail_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(pos != None):
                print("Email không hợp lệ")
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return


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

        if not continueCreate_done:
            ### Chỗ này có max_attempts để tăng số lần kiểm tra Element (hiện tại là 1)
            ### Check_attempt=True là cho phép kiểm tra element
            pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if pos is not None:
                Tap(index, ld_path_console, pos[0], pos[1])
                continueCreate_done = True

        # Kiểm tra agree nếu chưa hoàn thành
        if not passwordField_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console, confidence=0.5)
            if(pos != None):
                GoText(index, ld_path_console, passText, pos[0], pos[1])                   

        # time.sleep(2)

        # Kiểm tra nextt nếu chưa hoàn thành
        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            # print("Đã click Next 6")
            pass

        # time.sleep(2)

        if not notnow_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.notnow_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])  

        # time.sleep(2)

        if not agree_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.agree_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])                    

        # time.sleep(2)   
        if not issue282_done:
            is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(is282 != None):
                issue282_done = True
                print(f"Email: {emailText} bị dính 282")
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return           

        if not isInvalidaccount_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidAccount_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(pos != None):
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return

        if not sendviaSMS_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.sendviasmsField_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])    
                sendviaSMS_done = True

        if not issue282_done:
            is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(is282 != None):
                issue282_done = True
                print(f"Email: {emailText} bị dính 282")
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return               

        if not sendcodeviaSMS_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.sendcodeviasms_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])    
                sendcodeviaSMS_done = True

            ###
        # if not sendViaEmail_done:
        #     pos = TimAnhSauKhiChupVaSoSanh(Action.sendviaemail_Btn, index, ld_path_console, confidence=0.5)
        #     if(pos != None):
        #         Tap(index, ld_path_console, pos[0], pos[1]) 
        #         sendViaEmail_done = True

        if not confirmviaemail_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.confirmviaemail_Btn, index, ld_path_console)
            if(pos != None):
                GoText(index, ld_path_console, emailText, pos[0], pos[1])
                confirmviaemail_done = True

            ###

        if not newEmail_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.newEmailField_Btn, index, ld_path_console)
            if(pos != None):
                GoText(index, ld_path_console, emailText, pos[0], pos[1])
                newEmail_done = True

        if not nextviaEmail_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.nextviaemail_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])    
                nextviaEmail_done = True

        DemThoiGian(40)

        if not issue282_done:
            is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
            if(is282 != None):
                issue282_done = True
                print(f"Email: {emailText} bị dính 282")
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console)
                return

        # time.sleep(2)

        # Kiểm tra verifycode nếu chưa hoàn thành
        if not verifycode_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console)
            if pos is not None:
                # Chỗ này phải đảm bảo verify code đã được lấy mới chạy tiếp
                verifycode = GetOTP(emailText)
                if verifycode is None:
                    print("Không lấy được mã code == Reboot và xóa cache")
                    # UninstallFacebook(index, ld_path_console, package_name)
                    # QuitLD(index, ld_path_console)
                    return
                GoText(index, ld_path_console, verifycode, pos[0], pos[1])
                DemThoiGian(60)
                verifycode_done = True
        
        # time.sleep(2)

        if not okbtn_done:
            pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
            if(pos != None):
                Tap(index, ld_path_console, pos[0], pos[1])   
                okbtn_done = True 

        # time.sleep(2)

        if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
            # print("Đã click skip")
            pass

        # time.sleep(2)

        if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
            # print("Đã click skip lần 2") 
            pass

        # time.sleep(2)

        if XuLyNextButton(index, ld_path_console, Action.skip1_Btn):
            # print("Đã click skip lần 3") 
            pass                       
             
        # time.sleep(2)             

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
                    # print(f"Chuẩn bị xóa cache và reboot LDPlayer {index}")
                    DemThoiGian(3)
                    successReg_done = True
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console)

        # Nếu tất cả các điều kiện đã hoàn thành, thoát khỏi vòng lặp
        if (sendcodeviaSMS_done and nextviaEmail_done and confirmviaemail_done and continueCreate_done and sendviaSMS_done and sendViaEmail_done and newEmail_done and createbutton_done and getstarted_done and firstname_done and lastname_done and
            selectyourname_done and setDate_done and sett_done and gender_done and signup_done and email_done and
            doyouhaveaccount_done and password_done and verifycode_done and successReg_done and notnow_done and passwordField_done and agree_done and okbtn_done):
            break
