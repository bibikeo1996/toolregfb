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
import urllib.parse


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

def TimAnhSauKhiChupVaSoSanh(template_path, index, ld_path_console, confidence=0.7, max_attempts=2, delay=1, check_attempt=False):
    """
    Hàm này so sánh ảnh chụp màn hình với 1 hoặc nhiều template. Nếu bất kỳ template nào đạt độ chính xác yêu cầu,
    hàm sẽ trả về tọa độ và chỉ số của template trong mảng.

    Parameters:
    - template_path: Đường dẫn tới template (có thể là chuỗi hoặc danh sách chuỗi).
    - index: Instance index.
    - ld_path_console: Đường dẫn console LDPlayer.
    - confidence: Độ chính xác tối thiểu để chấp nhận template.
    - max_attempts: Số lần thử tối đa.
    - delay: Thời gian chờ giữa các lần thử (giây).
    - check_attempt: Nếu True, in ra số lần thử.

    Returns:
    - Tuple (index_of_template, center_x, center_y) nếu tìm thấy một template phù hợp, None nếu không tìm thấy.
    """
    # Xử lý để hỗ trợ 1 hoặc nhiều template
    if isinstance(template_path, str):
        template_paths = [template_path]
    elif isinstance(template_path, list):
        template_paths = template_path
    else:
        raise ValueError("template_path phải là một chuỗi hoặc danh sách chuỗi")

    # Đọc tất cả các template từ danh sách
    templates = []
    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Không tìm thấy file {path}")
        templates.append((path, template))

    attempts = 0
    while True:
        screenshot, local_screenshot_path = ChupAnhTrenManhinh(index, template_path, ld_path_console)
        try:
            for i, (template_path, template) in enumerate(templates):
                # So sánh template với ảnh chụp màn hình
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                file_name = os.path.basename(template_path)
                print(f"Độ khớp instance {index} {file_name}: {max_val * 100:.2f}%")
                
                if max_val >= confidence:
                    # Nếu khớp, trả về chỉ số template và tọa độ
                    x, y = max_loc
                    h, w = template.shape
                    center_x, center_y = x + w // 2, y + h // 2
                    return (center_x, center_y, i)  # Trả về index của template cùng với tọa độ

            # Nếu không có template nào khớp
            if check_attempt:
                sys.stdout.write(f"\rKhông tìm thấy template phù hợp. Thử lại lần {attempts + 1}/{max_attempts}")
                sys.stdout.flush()
                attempts += 1
                if attempts >= max_attempts:
                    print("\nKhông tìm thấy hình sau nhiều lần thử.")
                    return None
                time.sleep(delay)
        finally:
            if os.path.exists(local_screenshot_path):
                # os.remove(local_screenshot_path)
                pass


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
        print("text là văn bảng số")
        # Nếu text là một mã key event (sử dụng ldconsole)
        command = f'{ld_path_console} adb --index {index} --command "shell input keyevent {text}"'
        print(f"Command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Lỗi khi gửi sự kiện: {result.stderr}")
    else:
        print("text là văn bảng chữ và số")
        # Nếu text là một đoạn văn bản, gửi toàn bộ văn bản dưới dạng input text
        command = f'{ld_path_console} adb --index {index} --command "shell input text \\"{text}\\""'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Lỗi khi gửi văn bản: {result.stderr}")
        else:
            # Thêm độ trễ sau khi gửi lệnh
            time.sleep(1)  # Độ trễ 50ms

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

def GetOTP(email, max_attempts=10, delay=3):
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                messages = response.json()
                
                # Kiểm tra từng email trong danh sách
                for message in messages:
                    subject = message.get("subject", "")
                    if "FB-" in subject:
                        # Bóc tách mã OTP từ subject
                        otp = subject.split("FB-")[1].split()[0]
                        print(f"OTP Found: {otp}")
                        return otp
                    elif "is your confirmation code" in subject:
                        # Extract confirmation code from subject
                        otp = subject.split()[0]
                        print(f"Confirmation Code Found: {otp}")
                        return otp
            else:
                print(f"Request failed with status: {response.status_code}")
        
        except Exception as e:
            print(f"Error occurred: {e}")
        
        # Chờ trước khi thử lại
        print(f"Attempt {attempt + 1}/{max_attempts}. Retrying in {delay} seconds...")
        time.sleep(delay)
    
    print("OTP not found after maximum attempts.")
    return None

def TaoEmail():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "application-name": "web",
        "application-version": "2.4.2",
        "priority": "u=1, i",
        "referer": "https://temp-mail.io/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    # Payload
    payload = {
        "min_name_length": 6,
        "max_name_length": 10
    }
    response = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", headers=headers, json=payload)
    print(response.text)

    if response.status_code == 200:
        EmailAdd = response.json().get("email")
        return EmailAdd
    return None  

def getHoTenRandom(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return random.choice(lines).strip()      

        