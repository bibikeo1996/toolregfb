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
    # StartLD(index, ld_path_console)

    # ADBKillAndStartServer()

    # ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port)
    # quit()

    # CookieToken = json.loads(getAdbData(index, ld_path_console))
    # uid = CookieToken.get("uid")
    # cookie = CookieToken.get("cookie")
    # token = CookieToken.get("token")
    # # account = f"{uid}|{passText}|{cookie}|{token}|{emailText}"
    # account = f"{uid}|{cookie}|{token}"
    # print(account)
    # quit()
    max_iterations = 1  # Số lần lặp tối đa
    counter = 0
    try:
        while counter < max_iterations:
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
            issue282v2_done = False
            somethingwrongpopup_done = False

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
            sendviasmsv2_done = False
            smslimitreached_done = False
            validateName_done = False
            incorrectcode_done = False

            skip_lan1_done = False
            skip_lan2_done = False
            skip_lan3_done = False
            skip_lan4_done = False

            openapp_done = False

            emailText = TaoEmail()
            passText = ''.join(random.choice(string.ascii_letters) for i in range(15))
            fieldFirstName = getHoTenRandom(fileTxtPath+'ho.txt')  
            fieldLastName = getHoTenRandom(fileTxtPath+'ten.txt')
            print(f"Email: {emailText}, Firstname: {fieldFirstName}, Lastname: {fieldLastName}, Pass: {passText}")

            print("Vòng lặp đang chạy... Ấn Ctrl+C để dừng.")
            isSetup = ThietLapThongSoThietbi(index, ld_path_console)
            if isSetup:
                print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

            StartLD(index, ld_path_console)

            ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port)

            InstallFacebook(Action.isFacebookExist_Btn, index, ld_path_console, apk_path)

            CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

            
            OpenApp(Action.isOpenApp_Btn, index, ld_path_console, package_name)

            if not openapp_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.isOpenApp_Btn, index, ld_path_console)
                if pos is not None:
                    openapp_done = True
                    pass
                else:
                    OpenApp(Action.isOpenApp_Btn, index, ld_path_console, package_name)
            
            # # Kiểm tra createbutton nếu chưa hoàn thành
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
                pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console, confidence=0.5)
                if pos is not None:
                    GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])
                    # print("Đã nhập lastname")
                    pass
                    lastname_done = True

            time.sleep(2)

            # Kiểm tra nextt nếu chưa hoàn thành
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                # print("Đã click Next 1")
                pass

            validateName = [Action.validateName_Btn, Action.selectyourname_Btn, Action.setDate_Btn]
            # Kiểm tra setDate nếu chưa hoàn thành
            if not setDate_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=validateName, index=index, ld_path_console=ld_path_console)
                if(pos[2] == 0):
                    validateName_done = True
                    print(f"Wrong Fullname: {fieldFirstName} {fieldLastName}")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue
                elif(pos[2] == 1):
                    pos = TimAnhSauKhiChupVaSoSanh(Action.pickname_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                    if pos is not None:
                        Tap(index, ld_path_console, pos[0], pos[1])
                        selectyourname_done = True
                        # Kiểm tra nextt nếu chưa hoàn thành
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            # print("Đã click Next 2")
                            pass
                            print("Đang chọn ngày tháng năm sinh")
                            pos3 = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
                            if pos3 is not None:
                                ChonNgayThangNamSinh(index, ld_path_console)
                                setDate_done = True
                else:
                    pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
                    if pos is not None:
                        ChonNgayThangNamSinh(index, ld_path_console)
                        setDate_done = True
                    else: 
                        pass                        

            # Kiểm tra sett nếu chưa hoàn thành

            if not sett_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    sett_done = True
                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                        print("Đã click Next 3")           
                        pass

            # time.sleep(2)

            if not isInvalidBirth_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidBirth_Btn, index, ld_path_console, confidence=0.5, max_attempts=2, check_attempt=True)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
                    if pos2 is not None:
                        ChonNgayThangNamSinh(index, ld_path_console)
                        isInvalidBirth_done = True
                    else:
                        pass
                else:
                    pass                        
                    # UninstallFacebook(index, ld_path_console, package_name)
                    # QuitLD(index, ld_path_console, ld_path_instance)
                    # continue

            # Kiểm tra nextt nếu chưa hoàn thành
        
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
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue


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
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            validateAccountName = [Action.isInvalidAccount_Btn, Action.validateName_Btn]
            if not isInvalidaccount_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=validateAccountName, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    if pos[2] == 0 or pos[2] == 1:
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        continue
                else:
                    isInvalidaccount_done = True
                    pass

            # if not sendviaSMS_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(Action.sendviasmsField_Btn, index, ld_path_console)
            #     if(pos != None):
            #         Tap(index, ld_path_console, pos[0], pos[1])    
            #         sendviaSMS_done = True
            
            sendviasmsField_Btn = [Action.sendviasmsField_Btn, Action.sendviasmsFieldv2_Btn]
            if not sendviasmsv2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=sendviasmsField_Btn, index=index, ld_path_console=ld_path_console)
                print(pos)
                if(pos[2] == 0):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    sendviasmsv2_done = True
                    if not issue282_done:
                        is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(is282 != None):
                            print(f"Email: {emailText} bị dính 282")
                            UninstallFacebook(index, ld_path_console, package_name)
                            QuitLD(index, ld_path_console, ld_path_instance)
                            continue
                    if not sendcodeviaSMS_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.sendcodeviasms_Btn, index, ld_path_console)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            sendcodeviaSMS_done = True

                    if not confirmviaemail_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.confirmviaemail_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            confirmviaemail_done = True

                    if not confirmviaemail_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.confirmviaemailv2_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            confirmviaemail_done = True

                    if not newEmail_done:
                        pos1 = TimAnhSauKhiChupVaSoSanh(Action.newEmailField_Btn, index, ld_path_console)
                        if(pos1 != None):
                            GoText(index, ld_path_console, emailText, pos1[0], pos1[1])
                            newEmail_done = True

                    if not nextviaEmail_done:
                        pos2 = TimAnhSauKhiChupVaSoSanh(Action.nextviaemail_Btn, index, ld_path_console)
                        if(pos2 != None):
                            Tap(index, ld_path_console, pos2[0], pos2[1])    
                            nextviaEmail_done = True
                            pass
                else:
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.sendviasmsFieldv2_Btn, index, ld_path_console)
                    if(pos2 != None):
                        Tap(index, ld_path_console, pos[0], pos[1])
                        pos3 = TimAnhSauKhiChupVaSoSanh(Action.ididntgethecode_Btn, index, ld_path_console)
                        if(pos3 != None):
                            Tap(index, ld_path_console, pos[0], pos[1])
                            pos4 = TimAnhSauKhiChupVaSoSanh(Action.confimbyemailbtn_Btn, index, ld_path_console)
                            if(pos4 != None):
                                Tap(index, ld_path_console, pos[0], pos[1])
                                pos5 = TimAnhSauKhiChupVaSoSanh(Action.emailfieldv2_Btn, index, ld_path_console)
                                if(pos5 != None):
                                    GoText(index, ld_path_console, emailText, pos[0], pos[1])
                                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                        sendviasmsv2_done = True
                                        pass

            # DemThoiGian(30)
                           

            if not issue282_done:
                is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if(is282 != None):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue
            # time.sleep(2)

            if not smslimitreached_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.smslimitreached_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if(pos != None):
                    print("SMS limit reached")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue


            # Kiểm tra verifycode nếu chưa hoàn thành
            if not verifycode_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console, confidence=0.75)
                if pos is not None:
                    # Chỗ này phải đảm bảo verify code đã được lấy mới chạy tiếp
                    verifycode = GetOTP(email=emailText)
                    print(f"Verify code {index} {emailText}: {verifycode}")
                    DemThoiGian(1)
                    if verifycode is None:
                        print("Không lấy được mã code == Reboot và xóa cache")
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        continue
                    GoText(index, ld_path_console, verifycode, pos[0], pos[1])
                    DemThoiGian(1)
                    verifycode_done = True
            
            # time.sleep(2)
            if not okbtn_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])   
                    okbtn_done = True 

            # time.sleep(2)
            DemThoiGian(2)

            if not incorrectcode_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.incorrectemail_Btn, index, ld_path_console, max_attempts=3, check_attempt=True)
                if(pos != None):
                    print("Mã code không chính xác")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue


            # if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
            #     # print("Đã click skip")
            #     pass
                
            if not skip_lan1_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan1_done = True


            time.sleep(2)

            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            if not skip_lan2_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan2_done = True

            time.sleep(2) 

            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            if not skip_lan3_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.skip1_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan3_done = True                
                
            time.sleep(2)   

            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            if not skip_lan4_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.skip1_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan4_done = True

            time.sleep(2)          

            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

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
                        print(uid)
                        if account is not None:
                            with open('success.txt', 'a') as file:
                                file.write(account + '\n')
                        # print(f"Chuẩn bị xóa cache và reboot LDPlayer {index}")
                        DemThoiGian(2)
                        successReg_done = True
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        continue
            counter += 1
    except KeyboardInterrupt:
        print("Vòng lặp đã bị ngừng bằng Ctrl+C.")