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
from include.setUpDevices import GetPhone

# from include.OpenApp import openBrave
from data.getCode import *

def RunLD(index, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath):
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

            mobilePhone_done = False

            skip_lan1_done = False
            skip_lan2_done = False
            skip_lan3_done = False
            skip_lan4_done = False

            openapp_done = False

            isConnected_done = False
            isProxifier_done = False
            Isaccountexist_done = False

            isInvalidPhone_done = False

            emailText = TaoEmail()
            passText = ''.join(random.choice(string.ascii_letters) for i in range(15))
            fieldFirstName = getHoTenRandom(fileTxtPath+'ho.txt')  
            fieldLastName = getHoTenRandom(fileTxtPath+'ten.txt')
            # fieldFirstName = "Baker"
            # fieldLastName = "Louis"
            print(f"Email: {emailText}, Firstname: {fieldFirstName}, Lastname: {fieldLastName}, Pass: {passText}")

            isSetup = ThietLapThongSoThietbi(index, ld_path_console)
            if isSetup:
                pass
                # print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

            StartLD(index, ld_path_console)


            ## Connect LD với proxy
            if not isConnected_done:
                isConnected = ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port)
                if isConnected is True:
                    isConnected_done = True
                    pass
                else:
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue

            InstallFacebook(Action.isFacebookExist_Btn, index, ld_path_console, apk_path)

            CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

            OpenApp(index, ld_path_console, package_name)

            # Kiểm tra Facebook đã cài mở chưa
            if not openapp_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.isOpenApp_Btn, index, ld_path_console, confidence=0.6)
                if pos is not None:
                    openapp_done = True
                    pass
                else:
                    OpenApp(Action.isOpenApp_Btn, index, ld_path_console, package_name)
            # quit()

            # Tìm nút Create button
            if not createbutton_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.createbutton_Btn, index, ld_path_console)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    createbutton_done = True

            # Tìm nút get started
            if not getstarted_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.getstarted_Btn, index, ld_path_console)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    getstarted_done = True

            # Nhập tên 
            if not firstname_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.firstname3_Btn, index, ld_path_console)
                if pos is not None:
                    GoText(index, ld_path_console, fieldFirstName, pos[0], pos[1])
                    # print("Đã nhập firstname")
                    pass
                    firstname_done = True

            # Nhập họ
            if not lastname_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console, confidence=0.5)
                if pos is not None:
                    GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])
                    # print("Đã nhập lastname")
                    pass
                    lastname_done = True

            # Click nút next
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                pass

            validateName = [Action.validateName_Btn, Action.selectyourname_Btn, Action.setDate_Btn]
            # Kiểm tra ngày tháng năm sinh
            if not setDate_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(template_path=validateName, index=index, ld_path_console=ld_path_console)
                if(pos is not None and pos[2] == 0):
                    # Check nếu Validate name tìm thấy => Nghĩa là họ tên không hợp lệ => nhập lại
                    pos3 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console)
                    if pos3 is not None:
                        Tap(index, ld_path_console, pos3[0], pos3[1])
                        fieldLastName = getHoTenRandom(fileTxtPath+'ho.txt')
                        GoText(index, ld_path_console, fieldLastName, pos3[0], pos3[1])
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            validateName_done = True
                            pass
                    # Nếu Bắt chọn Name => Sẽ chọn name ngẫu nhiên 
                elif(pos[2] == 1):
                    pos = TimAnhSauKhiChupVaSoSanh(Action.pickname_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                    if pos is not None:
                        Tap(index, ld_path_console, pos[0], pos[1])
                        selectyourname_done = True
                        # Kiểm tra nextt nếu chưa hoàn thành
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            pass
                            # print("Đang chọn ngày tháng năm sinh")
                            pos3 = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
                            if pos3 is not None:
                                ChonNgayThangNamSinh(index, ld_path_console)
                                setDate_done = True
                                if not sett_done:
                                    pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
                                    if pos is not None:
                                        Tap(index, ld_path_console, pos[0], pos[1])
                                        sett_done = True
                                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):         
                                            pass
                                    # Nếu ngày tháng năm sinh bị sai => Xóa chọn lại cho đúng 
                                if not isInvalidBirth_done:
                                    pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidBirth_Btn, index, ld_path_console, confidence=0.5, max_attempts=1, check_attempt=True)
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
                else:
                    # Click vào nút Set ngày 
                    pos = TimAnhSauKhiChupVaSoSanhv2(Action.sett_Btn, index, ld_path_console)
                    if pos is not None:
                        Tap(index, ld_path_console, pos[0], pos[1])
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            pass
                            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                pass
                                pos2 = TimAnhSauKhiChupVaSoSanh(Action.agefield_Btn, index, ld_path_console)
                                if pos2 is not None:
                                    randomAge = str(random.randint(18, 36))
                                    GoText(index, ld_path_console, randomAge, pos2[0], pos2[1])
                                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                        pass
                                        pos3 = TimAnhSauKhiChupVaSoSanh(Action.okHideBirthDate_Btn, index, ld_path_console, confidence=0.55)
                                        if pos3 is not None:
                                            Tap(index, ld_path_console, pos3[0], pos3[1])
                                            setDate_done = True

                    # pos = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
                    # if pos is not None:
                    #     ChonNgayThangNamSinh(index, ld_path_console)
                    #     setDate_done = True
                    # else: 
                    #     pass                        

            # Kiểm tra sett nếu chưa hoàn thành

            # DemThoiGian(20)                       
            # if not sett_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
            #     if pos is not None:
            #         Tap(index, ld_path_console, pos[0], pos[1])
            #         sett_done = True
            #         if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):         
            #             pass
            # if not isInvalidBirth_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidBirth_Btn, index, ld_path_console, confidence=0.5, max_attempts=1, check_attempt=True)
            #     if(pos != None):
            #         Tap(index, ld_path_console, pos[0], pos[1])
            #         pos2 = TimAnhSauKhiChupVaSoSanh(Action.setDate_Btn, index, ld_path_console)
            #         if pos2 is not None:
            #             ChonNgayThangNamSinh(index, ld_path_console)
            #             isInvalidBirth_done = True
            #         else:
            #             pass
            #     else:
            #         pass

            # Chọn giới tính
            if not gender_done:
                pos = TimAnhSauKhiChupVaSoSanh(random.choice([Action.female_Btn, Action.male_Btn]), index, ld_path_console, confidence=0.6)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    gender_done = True

            # CLick next
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                pass

            # Nhập sdt 
            if not mobilePhone_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.phonenumberfield_Btn, index, ld_path_console)
                if pos is not None:
                    GoText(index, ld_path_console, GetPhone("USA"), pos[0], pos[1])
                    mobilePhone_done = True    

            # click next
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                # Kiểm tra sdt đã được sử dụng chưa
                pos = TimAnhSauKhiChupVaSoSanh(Action.isphonenumused_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if pos is not None:
                    mobilePhone_done = False
                    print("Số điện thoại đã được sử dụng")
                    ## xóa text trong field và nhập lại
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console, confidence=0.6, max_attempts=2, check_attempt=True)
                    if pos2 is not None:
                        Tap(index, ld_path_console, pos2[0], pos2[1])
                        pos3 = TimAnhSauKhiChupVaSoSanh(Action.phonenumberfield_Btn, index, ld_path_console)
                        if pos3 is not None:
                            GoText(index, ld_path_console, GetPhone("USA"), pos[0], pos[1])
                            mobilePhone_done = True
                else:
                    pass                    

            ## Kiểm tra email không họp lệ thì out làm lại 
            if not isInvalidEmail_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidEmail_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if(pos != None):
                    print("Email không hợp lệ")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue


            # Kiểm tra popup Do you have account
            if not doyouhaveaccount_done:
                ### Chỗ này có max_attempts để tăng số lần kiểm tra Element (hiện tại là 1)
                ### Check_attempt=True là cho phép kiểm tra element
                pos = TimAnhSauKhiChupVaSoSanh(Action.doyouhaveaccount_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if pos is not None:
                    pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console)
                    if pos is not None:
                        Tap(index, ld_path_console, pos[0], pos[1])
                        doyouhaveaccount_done = True

            # Kiểm tra popup Continue Create account
            if not continueCreate_done:
                ### Chỗ này có max_attempts để tăng số lần kiểm tra Element (hiện tại là 1)
                ### Check_attempt=True là cho phép kiểm tra element
                pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    Tap(index, ld_path_console, pos[0], pos[1])
                    continueCreate_done = True

            # Kiểm tra số điện thoại bị sai format
            if not isInvalidPhone_done:
                # Nếu sdt sai format xóa nhập lại 
                pos = TimAnhSauKhiChupVaSoSanh(Action.wrongphonenumber_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if(pos != None):
                    mobilePhone_done = False
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console)
                    if pos2 is not None:
                        Tap(index, ld_path_console, pos2[0], pos2[1])
                        if not mobilePhone_done:
                            pos3 = TimAnhSauKhiChupVaSoSanh(Action.phonenumberfield_Btn, index, ld_path_console)
                            if pos3 is not None:
                                GoText(index, ld_path_console, GetPhone("USA"), pos3[0], pos3[1])
                                mobilePhone_done = True
                                if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                    validateName_done = True
                                    pass

            # Nhập password
            if not passwordField_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console, confidence=0.5)
                if(pos != None):
                    GoText(index, ld_path_console, passText, pos[0], pos[1])                   

            # time.sleep(2)

            # Click next
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                # print("Đã click Next 6")
                pass

            # time.sleep(2)

            ## Chỗ này sẽ xuất hiện TH trùng password do sdt bị trùng từ trước => phải xử lý ở đây => Thoát app làm lại
            isAccountExist = [Action.idontseemyaccountv2_Btn, Action.idontseemyaccountv3_Btn, Action.tryanotherway_Btn]
            if not Isaccountexist_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(template_path=isAccountExist, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1 or pos[2] == 2):
                    print("Account đã tồn tại")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue

            # Click not now hoặc save account 
            if not notnow_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.notnow_Btn, index, ld_path_console, confidence=0.5)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])  

            # time.sleep(2)
            # Click agree
            if not agree_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.agree_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])                    

            # time.sleep(2)   
            # Kiểm tra có dính 282 không => Có thì out app 
            if not issue282_done:
                is282 = TimAnhSauKhiChupVaSoSanhv2(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if(is282 != None):
                    issue282_done = True
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            # validateAccountName = [Action.isInvalidAccount_Btn, Action.validateName_Btn]
            # if not isInvalidaccount_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(template_path=validateAccountName, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
            #     if pos is not None:
            #         if pos[2] == 0 or pos[2] == 1:
            #             UninstallFacebook(index, ld_path_console, package_name)
            #             QuitLD(index, ld_path_console, ld_path_instance)
            #             continue
            #     else:
            #         isInvalidaccount_done = True
            #         pass

            # Kiểm tra account bị sai => out app làm lại
            if not isInvalidaccount_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.isInvalidAccount_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if pos is not None:
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue

            # if not sendviaSMS_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(Action.sendviasmsField_Btn, index, ld_path_console)
            #     if(pos != None):
            #         Tap(index, ld_path_console, pos[0], pos[1])    
            #         sendviaSMS_done = True
            
            # Kiểm tra nút gủi SMS => Có 2 nút phải check 2 trường hợp để chọn đúng 
            sendviasmsField_Btn = [Action.sendviasmsField_Btn, Action.sendviasmsFieldv2_Btn]
            if not sendviasmsv2_done:
                pos = TimAnhSauKhiChupVaSoSanh(template_path=sendviasmsField_Btn, index=index, ld_path_console=ld_path_console)
                # Nếu là trường hợp 1 
                if(pos[2] == 0):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    sendviasmsv2_done = True
                    if not issue282_done:
                        # Kiểm tra die thì out app 
                        is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(is282 != None):
                            print(f"Email: {emailText} bị dính 282")
                            UninstallFacebook(index, ld_path_console, package_name)
                            QuitLD(index, ld_path_console, ld_path_instance)
                            continue

                    # Kiểm tra đã chọn gửi SMS chưa
                    if not sendcodeviaSMS_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.sendcodeviasms_Btn, index, ld_path_console)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            sendcodeviaSMS_done = True

                    # Kiểm tra đã click vào button verify via email
                    if not confirmviaemail_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.confirmviaemail_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            confirmviaemail_done = True

                    # Kiểm tra đã click vào button verify by email 
                    if not confirmviaemail_done:
                        pos = TimAnhSauKhiChupVaSoSanh(Action.confirmviaemailv2_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if(pos != None):
                            Tap(index, ld_path_console, pos[0], pos[1])    
                            confirmviaemail_done = True

                    # Tìm thấy field email => nhập email
                    if not newEmail_done:
                        pos1 = TimAnhSauKhiChupVaSoSanh(Action.newEmailField_Btn, index, ld_path_console)
                        if(pos1 != None):
                            GoText(index, ld_path_console, emailText, pos1[0], pos1[1])
                            newEmail_done = True

                    # Click next 
                    if not nextviaEmail_done:
                        pos2 = TimAnhSauKhiChupVaSoSanh(Action.nextviaemail_Btn, index, ld_path_console)
                        if(pos2 != None):
                            Tap(index, ld_path_console, pos2[0], pos2[1])    
                            nextviaEmail_done = True
                else:
                    # Trường hợp 2
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.sendviasmsFieldv2_Btn, index, ld_path_console)
                    if(pos2 != None):
                        Tap(index, ld_path_console, pos[0], pos[1])
                        # CLick chọn nút i didnt get the code => để được chọn confirm by email
                        pos3 = TimAnhSauKhiChupVaSoSanh(Action.ididntgethecode_Btn, index, ld_path_console)
                        if(pos3 != None):
                            Tap(index, ld_path_console, pos[0], pos[1])
                            # Click chọn confirm by email
                            pos4 = TimAnhSauKhiChupVaSoSanh(Action.confimbyemailbtn_Btn, index, ld_path_console)
                            if(pos4 != None):
                                Tap(index, ld_path_console, pos[0], pos[1])
                                # Chọn field và nhập Email 
                                pos5 = TimAnhSauKhiChupVaSoSanh(Action.emailfieldv2_Btn, index, ld_path_console)
                                if(pos5 != None):
                                    GoText(index, ld_path_console, emailText, pos[0], pos[1])
                                    # Click next
                                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                        sendviasmsv2_done = True

            # DemThoiGian(30)
                           
            # Check die or live
            if not issue282_done:
                is282 = TimAnhSauKhiChupVaSoSanh(Action.issue282_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if(is282 != None):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue
            # time.sleep(2)

            # Check dính sms limit => out app 
            if not smslimitreached_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.smslimitreached_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if(pos != None):
                    print("SMS limit reached")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue


            # Check verify code field => Có nhập code
            if not verifycode_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.verifycodefield_Btn, index, ld_path_console, confidence=0.75)
                if pos is not None:
                    # Chỗ này phải đảm bảo verify code đã được lấy mới chạy tiếp
                    verifycode = GetOTP(email=emailText)
                    print(f"Verify code {index} {emailText}: {verifycode}")
                    DemThoiGian(1)
                    # Ko tìm được code out thoát app
                    if verifycode is None:
                        print("Không lấy được mã code == Reboot và xóa cache")
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        continue
                    GoText(index, ld_path_console, verifycode, pos[0], pos[1])
                    DemThoiGian(1)
                    verifycode_done = True
            
            # time.sleep(2)

            ## CLick submit code  
            if not okbtn_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.ok_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])   
                    okbtn_done = True 

            # time.sleep(2)
            # DemThoiGian(2)

            # Chcek code sai => out app
            if not incorrectcode_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(Action.incorrectemail_Btn, index, ld_path_console, max_attempts=1, check_attempt=True)
                if(pos != None):
                    print("Mã code không chính xác")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue

            # CLick next
            if XuLyNextButton(index, ld_path_console, Action.skip_Btn):
                # print("Đã click skip")
                pass
                
            # if not skip_lan1_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
            #     if(pos != None):
            #         Tap(index, ld_path_console, pos[0], pos[1])
            #         skip_lan1_done = True

            # issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            # if not issue282v2_done:
            #     pos = TimAnhSauKhiChupVaSoSanh(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=1, check_attempt=True)
            #     if pos is not None and (pos[2] == 0 or pos[2] == 1):
            #         print(f"Email: {emailText} bị dính 282")
            #         UninstallFacebook(index, ld_path_console, package_name)
            #         QuitLD(index, ld_path_console, ld_path_instance)
            #         continue 

            # Click skip lần 1
            if not skip_lan2_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(Action.skip_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan2_done = True

            # Check die or live 
            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue 

            # Click skip lần 2
            if not skip_lan3_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(Action.skip1_Btn, index, ld_path_console)
                if(pos != None):
                    Tap(index, ld_path_console, pos[0], pos[1])
                    skip_lan3_done = True

            # Check die or live 
            issue282v2_btn_check = [Action.somethingwrongpopup_Btn, Action.issue282v2_Btn]
            if not issue282v2_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(template_path=issue282v2_btn_check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None and (pos[2] == 0 or pos[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                    UninstallFacebook(index, ld_path_console, package_name)
                    QuitLD(index, ld_path_console, ld_path_instance)
                    continue

            # Check thành công thì get cookie => in vào file txt => out app
            if not successReg_done:
                pos = TimAnhSauKhiChupVaSoSanhv2(Action.successReg3_Btn, index, ld_path_console)
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
                            with open('uid.txt', 'a') as file:
                                file.write(uid + '\n')
                        DemThoiGian(1)
                        successReg_done = True
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        quit()
            counter += 1
    except KeyboardInterrupt:
        print("Vòng lặp đã bị ngừng bằng Ctrl+C.")