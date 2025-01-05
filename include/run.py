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
    data = getDataInFileEmails(3)
    emailText = data["email"]
    passText = data["passWord"]
    fieldFirstName = data["firstName"]
    fieldLastName = data["lastName"]
    mi = data["mi"]
    phpsessid = data["phpsessid"]

    # emailText = "kavif45498@myweblaw.com"
    # passText = "9dVhsUax@"
    # fieldFirstName = "Yen"
    # fieldLastName = "Pham"
    # mi = data["mi"]
    # phpsessid = data["phpsessid"]
    # print(f"Email: {emailText} - Pass: {passText} - First Name: {fieldFirstName} - Last Name: {fieldLastName} - MI: {mi} - PHPSESSID: {phpsessid}")

    # RebootVaXoaCache(index, apk_path, package_name, ld_path_console, ld_path_instance)
    # quit
    isSetup = ThietLapThongSoThietbi(index, ld_path_console)
    if(isSetup == True):
        pass

    isStarted = KhoiDongLDPlayer(index, ld_path_console)
    if(isStarted == True):
        pass

    isInstalled = KiemTraDaCaiAppFaceBookLiteChua(index, package_name, apk_path, ld_path_console)
    if(isInstalled == True):
        pass

    DemThoiGian(1)

    CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name)

    DemThoiGian(2)

    OpenApp(index)
    
    DemThoiGian(5)

    def process_step(condition, action, *args):
        """
        Kiểm tra và thực hiện một bước nếu điều kiện chưa hoàn thành.
        
        :param condition: Biến trạng thái kiểm tra điều kiện.
        :param action: Hàm hành động cần thực hiện.
        :param args: Các tham số cần truyền vào hàm hành động.
        :return: Trạng thái mới của điều kiện.
        """
        if not condition:
            pos = TimAnhSauKhiChupVaSoSanh(*args)
            if pos is not None:
                action(*pos)
                return True
        return condition

    # Tạo các flag để kiểm soát từng điều kiện
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

    while True:
        # Danh sách các bước tuần tự
        steps = [
            (createbutton_done, lambda x, y: Tap(index, ld_path_console, x, y), Action.createbutton_Btn),
            (getstarted_done, lambda x, y: Tap(index, ld_path_console, x, y), Action.getstarted_Btn),
            (firstname_done, lambda x, y: GoText(index, ld_path_console, fieldFirstName, x, y), Action.firstname3_Btn),
            (lastname_done, lambda x, y: GoText(index, ld_path_console, fieldLastName, x, y), Action.lastname_Btn),
            (selectyourname_done, lambda x, y: Tap(index, ld_path_console, x, y), Action.selectyourname_Btn),
            (setDate_done, lambda: ChonNgayThangNamSinh(index, ld_path_console), Action.setDate_Btn),
            # Thêm các bước khác theo cấu trúc tương tự
        ]

        # Duyệt qua các bước
        for i, (condition, action, *action_args) in enumerate(steps):
            if all(step[0] for step in steps[:i]):  # Chỉ chạy nếu tất cả bước trước đó đã hoàn thành
                steps[i] = (process_step(condition, action, index, ld_path_console, *action_args), action, *action_args)

        # Kiểm tra Next Button nếu cần thiết
        if all(step[0] for step in steps[:4]) and XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            print("Đã click Next")

        # Kiểm tra nếu tất cả các điều kiện đã hoàn thành, thoát vòng lặp
        if all(step[0] for step in steps):
            break