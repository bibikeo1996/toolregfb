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


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'defined'))
from dotenv import load_dotenv
from key import KeyCode, Action
from PIL import Image
from io import BytesIO
# from adb_shell.auth import Signer
# from adb_shell.transport import Transport

load_dotenv()
ld_path_console = os.getenv('LD_PATH_CONSOLE')
ld_path_exe = os.getenv('LD_PATH_EXE')
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH')
package_name = os.getenv('PACKAGE_NAME')

def OpenLDPlayer(ld_type, index):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'launch', '--index', str(index)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to launch LDPlayer: {e}")
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")

def OpenApp(ld_type, index):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open app: {e}")
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")

def InstallAppFile(ld_type, index, file_name):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'installapp', '--index', str(index), '--filename', file_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install APK: {e}")
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")

def UnInstallAppFile(ld_type, index, package_name):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall app: {e}")
    else:
        print("LD_PATH_CONSOLE environment variable is not set.")


## So sánh ảnh màn hình với ảnh action để click
def ChupAnhTrenManhinh(index):
    emulator_screenshot_path = "/sdcard/screenshot.png"
    command_screencap = f'ldconsole.exe adb --index {index} --command "shell screencap -p {emulator_screenshot_path}"'
    subprocess.run(command_screencap, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local_screenshot_path = f"./screenshot{index}.png"
    command_pull = f'ldconsole.exe adb --index {index} --command "pull {emulator_screenshot_path} {local_screenshot_path}"'
    subprocess.run(command_pull, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(local_screenshot_path):
        raise FileNotFoundError(f"File {local_screenshot_path} không tồn tại. Quá trình pull ảnh có thể đã gặp lỗi.")
    screenshot = cv2.imread(local_screenshot_path, cv2.IMREAD_GRAYSCALE)
    if screenshot is None:
        raise ValueError(f"Không thể đọc file ảnh từ {local_screenshot_path}. File có thể không hợp lệ.")

    return screenshot, local_screenshot_path

def TimAnhSauKhiChupVaSoSanh(template_path, index, confidence=0.8, max_attempts=10, delay=1):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Không tìm thấy file {template_path}")

    attempts = 0
    while attempts < max_attempts:
        screenshot, local_screenshot_path = ChupAnhTrenManhinh(index)
        try:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= confidence:
                x, y = max_loc
                h, w = template.shape
                center_x, center_y = x + w // 2, y + h // 2

                return (center_x, center_y)
            else:
                sys.stdout.write(f"\rKhông tìm thấy hình {template_path} với độ chính xác yêu cầu. Thử lại lần {attempts + 1}/{max_attempts}")
                sys.stdout.flush()
                attempts += 1
                time.sleep(delay)

        finally:
            if os.path.exists(local_screenshot_path):
                os.remove(local_screenshot_path)

    print("Không tìm thấy hình sau nhiều lần thử.")
    return None

def KetNoiPortThietBiTheoPort(adb_port):
    connect_command = f"adb connect 127.0.0.1:{adb_port}"
    result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
    if "connected" in result.stdout:
        print(f"Kết nối thành công đến 127.0.0.1:{adb_port}")
        return True
    else:
        print(f"Kết nối thất bại: {result.stdout}")
        return False
# Xử lý hành động của user 

# def GoText(index, text, x=None, y=None):
#     if x is not None and y is not None:
#         # Tap vào vị trí trước khi nhập văn bản
#         Tap(index, x, y)
    
#     if isinstance(text, int):
#         # Nếu text là một mã key event
#         cmdCommand = f"shell input keyevent {text}"
#         command = f"adb -s 127.0.0.1:{index} {cmdCommand}"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         if result.returncode == 0:
#             print(f"Đã gửi sự kiện: {text} trên index {index}")
#         else:
#             print(f"Lỗi khi gửi sự kiện: {result.stderr}")
#     else:
#         # Nếu text là một đoạn văn bản, gửi từng ký tự dưới dạng key event
#         for char in text:
#             keycode = getattr(KeyCode, f"KEYCODE_{char.upper()}", None)
#             if keycode is not None:
#                 cmdCommand = f"shell input keyevent {keycode}"
#                 command = f"adb -s 127.0.0.1:{index} {cmdCommand}"
#                 result = subprocess.run(command, shell=True, capture_output=True, text=True)
#                 if result.returncode != 0:
#                     print(f"Lỗi khi gửi sự kiện: {result.stderr}")
#             else:
#                 print(f"Không tìm thấy mã key event cho ký tự: {char}")

def GoText(index, text, x=None, y=None):
    if x is not None and y is not None:
        # Tap vào vị trí trước khi nhập văn bản
        Tap(index, x, y)
    if isinstance(text, int):
        # Nếu text là một mã key event (sử dụng ldconsole)

        command = f'ldconsole.exe adb --index {index} --command "shell input keyevent {text}"'
        print(f"Command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Đã gửi sự kiện: {text} trên index {index}")
        else:
            print(f"Lỗi khi gửi sự kiện: {result.stderr}")
    else:
        # Nếu text là một đoạn văn bản, gửi từng ký tự dưới dạng key event
        for char in text:
            keycode = getattr(KeyCode, f"KEYCODE_{char.upper()}", None)
            if keycode is not None:
                command = f'ldconsole.exe adb --index {index} --command "shell input keyevent {keycode}"'
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(f"Command: {command}")
                if result.returncode != 0:
                    print(f"Lỗi khi gửi sự kiện: {result.stderr}")
                else:
                    # Thêm độ trễ giữa các lệnh
                    time.sleep(0.05)  # Độ trễ 50ms
            else:
                print(f"Không tìm thấy mã key event cho ký tự: {char}")

def SwipeMonth(adb_port, tap_x=None, tap_y=None):
    duration = 20

    if tap_x is not None and tap_y is not None:
        Tap(adb_port, tap_x, tap_y)
    
    swipe_count = random.randint(1, 12)
    count = 0  # Initialize swipe counter

    while count < swipe_count:
        # Cập nhật lệnh để sử dụng ldconsole.exe thay vì adb
        cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y - 100} {duration}"
        command = f"ldconsole.exe adb --index {adb_port} --command \"{cmdCommand}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error performing swipe action: {result.stderr}")
            
        count += 1

def SwipeDay(adb_port, tap_x=None, tap_y=None):
    duration = 20

    if tap_x is not None and tap_y is not None:
        Tap(adb_port, tap_x, tap_y)
    
    swipe_count = random.randint(1, 30)
    count = 0  # Initialize swipe counter

    while count < swipe_count:
        cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y - 100} {duration}"
        # Cập nhật lệnh để sử dụng ldconsole.exe thay vì adb
        command = f"ldconsole.exe adb --index {adb_port} --command \"{cmdCommand}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error performing swipe action: {result.stderr}")
        count += 1

def SwipeYear(adb_port, tap_x=None, tap_y=None):
    duration = 20

    if tap_x is not None and tap_y is not None:
        Tap(adb_port, tap_x, tap_y)
    
    swipe_count = random.randint(15, 20)
    count = 0  # Initialize swipe counter

    while count < swipe_count:
        cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y - 100} {duration}"
        # Cập nhật lệnh để sử dụng ldconsole.exe thay vì adb
        command = f"ldconsole.exe adb --index {adb_port} --command \"{cmdCommand}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error performing swipe action: {result.stderr}")
        count += 1

# def SwipeMonth(adb_port, tap_x=None, tap_y=None):
#     duration = 20

#     if tap_x is not None and tap_y is not None:
#         Tap(adb_port, tap_x, tap_y)
    
#     swipe_count = random.randint(1, 12)
#     count = 0  # Initialize swipe counter

#     while count < swipe_count:
#         cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y + 100} {duration}"
#         command = f"adb -s 127.0.0.1:{adb_port} {cmdCommand}"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         if result.returncode != 0:
#             print(f"Error performing swipe action: {result.stderr}")
            
#         count += 1

# def SwipeDay(adb_port, tap_x=None, tap_y=None):
#     duration = 20

#     if tap_x is not None and tap_y is not None:
#         Tap(adb_port, tap_x, tap_y)
    
#     swipe_count = random.randint(1, 30)
#     count = 0  # Initialize swipe counter

#     while count < swipe_count:
#         cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y + 100} {duration}"
#         command = f"adb -s 127.0.0.1:{adb_port} {cmdCommand}"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         if result.returncode != 0:
#            print(f"Error performing swipe action: {result.stderr}")
#         count += 1

# def SwipeYear(adb_port, tap_x=None, tap_y=None):
#     duration = 20

#     if tap_x is not None and tap_y is not None:
#         Tap(adb_port, tap_x, tap_y)
    
#     swipe_count = random.randint(15, 50)
#     count = 0  # Initialize swipe counter

#     while count < swipe_count:
#         cmdCommand = f"shell input swipe {tap_x} {tap_y} {tap_x} {tap_y - 100} {duration}"
#         command = f"adb -s 127.0.0.1:{adb_port} {cmdCommand}"
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         if result.returncode != 0:
#             print(f"Error performing swipe action: {result.stderr}")
#         count += 1        

def Tap(index, x, y):
    # Lệnh thực hiện tap thông qua ldconsole.exe với index
    cmdCommand = f"shell input tap {x} {y}"
    command = f'ldconsole.exe adb --index {index} --command "{cmdCommand}"'

    # Thực thi lệnh
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Xử lý kết quả
    if result.returncode == 0:
        print(f"Đã tap tại vị trí: ({x}, {y}) trên LDPlayer index {index}")
    else:
        print(f"Lỗi khi thực hiện tap: {result.stderr}")
