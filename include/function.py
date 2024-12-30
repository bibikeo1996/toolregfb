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

def OpenApp(index):
    if ld_path_console:
        try:
            subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open app: {e}")
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

def TimAnhSauKhiChupVaSoSanh(template_path, index, confidence=0.8, max_attempts=2, delay=1):
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
# Hàm gửi sự kiện keyevent
def CommandGoText(index, keycode, delay):
    command = f'ldconsole.exe adb --index {index} --command "shell input keyevent {keycode}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Lỗi khi gửi sự kiện {keycode}: {result.stderr}")
    else:
        print(f"Đã gửi sự kiện {keycode} thành công.")
    time.sleep(delay)  # Độ trễ sau mỗi lệnh

# Hàm GoText
def GoText(index, text, x=None, y=None):
    # Nếu có tọa độ, thực hiện tap vào vị trí đó
    if x is not None and y is not None:
        Tap(index, x, y)

    if isinstance(text, int):
        # Nếu text là một mã key event
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
                CommandGoText(index, keycode, delay=0.0000001)
            else:
                print(f"Không tìm thấy mã key event cho ký tự: {char}")

    print("Tất cả các sự kiện đã được gửi.")

def Tap(index, x, y, max_attempts=2, delay=1):
    """
    Thực hiện lệnh tap qua ldconsole.exe với index, thử tối đa max_attempts lần.
    
    :param index: Index của LDPlayer
    :param x: Tọa độ X
    :param y: Tọa độ Y
    :param max_attempts: Số lần thử tối đa (mặc định 5)
    :param delay: Thời gian chờ giữa các lần thử (mặc định 1 giây)
    :return: True nếu tap thành công, False nếu không thành công sau max_attempts lần
    """
    cmdCommand = f"shell input tap {x} {y}"
    command = f'ldconsole.exe adb --index {index} --command "{cmdCommand}"'

    for attempt in range(1, max_attempts + 1):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            sys.stdout.write(f"\rĐã tap tại vị trí: ({x}, {y}) trên LDPlayer index {index} (Lần thử {attempt})\n")
            sys.stdout.flush()
            return True  # Thành công
        else:
            sys.stdout.write(f"\rThử tap tại vị trí ({x}, {y}), lần {attempt}/{max_attempts}... ")
            sys.stdout.flush()
            time.sleep(delay)

    sys.stdout.write(f"\nKhông thể thực hiện tap tại vị trí: ({x}, {y}) trên LDPlayer index {index} sau {max_attempts} lần thử.\n")
    sys.stdout.flush()
    return False  # Thất bại

        
def KiemTraDangKyThanhCong(index, x=None, y=None):
    if x is not None and y is not None:
        return True
    else:
        print("Đăng ký không thành công!")
        return False
        