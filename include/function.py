import sys
import os
import subprocess
import cv2
import numpy as np
import time
import random
import string
import requests
import threading
import shutil
import pandas as pd
import pyautogui


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'defined'))
from dotenv import load_dotenv
from key import KeyCode, Action
from PIL import Image
from io import BytesIO
from mss import mss

load_dotenv()
ld_path_console = os.getenv('LD_PATH_CONSOLE')
ld_path_exe = os.getenv('LD_PATH_EXE')
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH')
package_name = os.getenv('PACKAGE_NAME')

def TimAnhSauKhiChupVaSoSanh(template_path, index, ld_path_console, confidence=0.8, max_attempts=2, delay=1, check_attempt=False):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Không tìm thấy file {template_path}")

    attempts = 0
    while True:
        screenshot, local_screenshot_path = ChupAnhTrenManhinh(index, template_path, ld_path_console)
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            file_name = os.path.basename(template_path)
            # print(f"Độ khớp {file_name}: {max_val * 100:.2f}%")
            if max_val >= confidence:
                x, y = max_loc
                h, w = template.shape
                center_x, center_y = x + w // 2, y + h // 2

                return (center_x, center_y)
            else:
                if check_attempt:
                    sys.stdout.write(f"\rKhông tìm thấy hình {template_path} với độ chính xác yêu cầu. Thử lại lần {attempts + 1}/{max_attempts}")
                    sys.stdout.flush()
                    attempts += 1
                    if attempts >= max_attempts:
                        print("Không tìm thấy hình sau nhiều lần thử.")
                        return None
                    time.sleep(delay)

        finally:
            if os.path.exists(local_screenshot_path):
                os.remove(local_screenshot_path)

# def TimAnhSauKhiChupVaSoSanh(template_path, index, ld_path_console, confidence=0.8, max_attempts=2, delay=3, timeout=20, check_attempt=False):
#     template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
#     if template is None:
#         raise FileNotFoundError(f"Không tìm thấy file {template_path}")

#     start_time = time.time()  # Lưu thời điểm bắt đầu
#     attempts = 0

#     while True:
#         # Kiểm tra thời gian đã vượt quá timeout chưa
#         elapsed_time = time.time() - start_time
#         if elapsed_time > timeout:
#             print(f"Hết thời gian {timeout} giây. Không tìm thấy hình.")
#             return None

#         # Chụp ảnh màn hình và xử lý so sánh
#         screenshot, local_screenshot_path = ChupAnhTrenManhinh(index, template_path, ld_path_console)
#         try:
#             result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#             file_name = os.path.basename(template_path)
#             print(f"Độ khớp {file_name}: {max_val * 100:.2f}%")
#             if max_val >= confidence:
#                 x, y = max_loc
#                 h, w = template.shape
#                 center_x, center_y = x + w // 2, y + h // 2
#                 return (center_x, center_y)
#             else:
#                 if check_attempt:
#                     sys.stdout.write(f"\rKhông tìm thấy hình {template_path} với độ chính xác yêu cầu. Thử lại lần {attempts + 1}/{max_attempts}\n")
#                     sys.stdout.flush()
#                     attempts += 1
#                     if attempts >= max_attempts:
#                         print("\nKhông tìm thấy hình sau nhiều lần thử.")
#                         return None

#         finally:
#             if os.path.exists(local_screenshot_path):
#                 pass
#                 # os.remove(local_screenshot_path)

#         # Chờ delay giữa các lần thử
#         time.sleep(delay)


# def TimAnhSauKhiChupVaSoSanh(template_path, index, ld_path_console, timeout=10):
#     FileName = os.path.basename(template_path)
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         location = pyautogui.locateOnScreen(template_path, confidence=0.8)
#         if location:
#             print(f'Đã click {FileName}')
#             return location
#         time.sleep(0.5)
#     return None

def ChupAnhTrenManhinh(index, filename, ld_path_console):
    emulator_screenshot_path = "/sdcard/screenshot.png"
    command_screencap = f'{ld_path_console} adb --index {index} --command "shell screencap -p {emulator_screenshot_path}"'
    subprocess.run(command_screencap, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local_screenshot_path = f"./screenshot{index}.png"
    command_pull = f'{ld_path_console} adb --index {index} --command "pull {emulator_screenshot_path} {local_screenshot_path}"'
    subprocess.run(command_pull, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(local_screenshot_path):
        raise FileNotFoundError(f"File {local_screenshot_path} không tồn tại. Quá trình pull ảnh có thể đã gặp lỗi.")
    
    screenshot = cv2.imread(local_screenshot_path, cv2.IMREAD_GRAYSCALE)
    if screenshot is None:
        raise ValueError(f"Không thể đọc file ảnh từ {local_screenshot_path}. File có thể không hợp lệ.")

    return screenshot, local_screenshot_path

def LayoutThayDoi(before_image, after_image, similarity_threshold):
    # So sánh ảnh Before và After bằng matchTemplate
    result = cv2.matchTemplate(before_image, after_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    # Đếm số lượng điểm tương đồng
    diff = cv2.absdiff(before_image, after_image)
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    non_zero_count = cv2.countNonZero(thresh)

    ## điểm tương đồng > 3 nghĩa là layout chưa đổi 
    ## còn < 3 nghĩa là đã đổi ==> pass
    print(f"Số điểm tương đồng: {non_zero_count}")

    # Kiểm tra nếu số điểm tương đồng <= similarity_threshold thì coi như layout đã thay đổi
    return non_zero_count <= similarity_threshold

def KetNoiPortThietBiTheoPort(adb_port):
    connect_command = f"adb connect 127.0.0.1:{adb_port}"
    result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
    if "connected" in result.stdout:
        print(f"Kết nối thành công đến 127.0.0.1:{adb_port}")
        return True
    else:
        print(f"Kết nối thất bại: {result.stdout}")
        return False

def DocFileExcel(file_path):
    df = pd.read_excel(file_path)
    # print(df)
    emails = df['email'].tolist()
    passwords = df['password'].tolist()
    first_names = df['name'].tolist()
    last_names = df['first name'].tolist()
    return emails, passwords, first_names, last_names

def CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name):
    permissions = [
        "android.permission.MANAGE_EXTERNAL_STORAGE",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_CALENDAR",
        "android.permission.READ_PHONE_STATE",
        "android.permission.READ_CALL_LOG",
        "android.permission.CAMERA",
        # "android.permission.WRITE_CALL_LOG",
        # "android.permission.ACCESS_FINE_LOCATION",
        # "android.permission.ACCESS_COARSE_LOCATION",
        # "android.permission.RECORD_AUDIO",
        # "android.permission.READ_EXTERNAL_STORAGE",
        # "android.permission.WRITE_EXTERNAL_STORAGE"
    ]
    
    for permission in permissions:
        command = f'{ld_path_console} adb --index {index} --command "shell pm grant {package_name} {permission}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Đang cấp quyền {permission}: {result.stderr}")
        if result.returncode != 0:
            print(f"Failed to grant {permission}: {result.stderr}")

# Xử lý hành động của user 
def GoText(index, ld_path_console, text, x, y):
    if x is not None and y is not None:
        # Tap vào vị trí trước khi nhập văn bản
        Tap(index, ld_path_console, x, y)
        
    if isinstance(text, int):
        # Nếu text là một mã key event (sử dụng ldconsole)
        command = f'{ld_path_console} adb --index {index} --command "shell input keyevent {text}"'
        print(f"Command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Lỗi khi gửi sự kiện: {result.stderr}")
    else:
        # Nếu text là một đoạn văn bản, gửi toàn bộ văn bản dưới dạng input text
        command = f'{ld_path_console} adb --index {index} --command "shell input text \\"{text}\\""'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Lỗi khi gửi văn bản: {result.stderr}")
        else:
            # Thêm độ trễ sau khi gửi lệnh
            time.sleep(0.05)  # Độ trễ 50ms

def Tap(index, ld_path_console, x, y):
    # print(f"Tap at {x}, {y}")
    command = f'{ld_path_console} adb --index {index} --command "shell input tap {x} {y}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    return True
     
def KiemTraDangKyThanhCong(index, x, y):
    if x is not None and y is not None:
        return True
    else:
        print("Đăng ký không thành công!")
        return False

def XuLyNextButton(index, ld_path_console, actionURL):
    pos = TimAnhSauKhiChupVaSoSanh(actionURL, index, ld_path_console)
    if pos is not None:
        Tap(index, ld_path_console, pos[0], pos[1])
        return True
    return False

def MoAppThanhCong(index, x, y):
    if x is not None and y is not None:
        return True
    else:
        print("Mở app không thành công!")
        return False
