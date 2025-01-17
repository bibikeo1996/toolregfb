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
# from include.function import *
# from include.OpenApp import *
# from include.datepicker import *
# from include.setUpDevices import *
# from include.getCookieToken import *
# from include.quitInstance import *

def ADBKillAndStartServer():
    kill_command = ["adb", "kill-server"]
    subprocess.run(kill_command)
    time.sleep(1)
    # print("ADB server stopped")
    start_command = ["adb", "start-server"]
    subprocess.run(start_command)
    time.sleep(2)

## Khởi dộng LDPlayer
def StartLD(template_path, index, ld_path_console):
    command = f'{ld_path_console} launch --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    for _ in range(30):  # Lặp tối đa 30 lần (tương đương với 1 phút nếu sleep 2 giây)
        try:
            pos = TimAnhSauKhiChupVaSoSanhv2(template_path, index, ld_path_console)
            if pos is not None:
                print("Start LDPlayer successfully")
                return True  # Thoát khỏi hàm khi tìm thấy
            else:
                time.sleep(2)
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(2)

    print("Không tìm thấy pos trong thời gian giới hạn.")
    return False  # Trả về `False` nếu hết thời gian

def ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port):
    try: 
        # ADBKillAndStartServer()
        start_command = ["adb", "devices"]
        subprocess.run(start_command)
        DemThoiGian(2)
        """
        Cấu hình proxy cho emulator dựa trên index.
        
        :param index: Index của emulator (bắt đầu từ 0).
        :param proxy_ip: Địa chỉ IP của proxy.
        :param proxy_port: Cổng của proxy.
        """
        # Tính port dựa trên index
        port = 5555 + index * 2
        removeproxy = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy :0'
        result = subprocess.run(removeproxy, capture_output=True, text=True)
        # Lệnh ADB để cấu hình proxy
        DemThoiGian(1)
        command = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy {proxy_ip}:{proxy_port}'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
            print(f"Proxy set thành công trên {index} (port {port})")
        else:
            return False
            print(f"Lỗi khi set proxy trên emulator {index} (port {port}): {result.stderr}")
    except FileNotFoundError:
        print(f"Không tìm thấy ldconsole.exe tại: {ldconsole_path}")
    DemThoiGian(2)
    # checkProxy = f'{ld_path_console} adb --index {index} --command "shell settings get global http_proxy"' 

def RemoveProxy(index, ld_path_console):
    try:
        port = 5555 + index * 2
        command = f'adb -s 127.0.0.1:{port} shell settings put global http_proxy :0'
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
            print(f"Tắt proxy thành công trên {index} (port {port})")
        else:
            return False
            print("Ko thể remove Proxy:", result.stderr)
    except FileNotFoundError:
        print(f"Không tìm thấy ldconsole.exe tại: {ldconsole_path}")        

## Check facebook có tồn tại hay không sau đó uninstall
def UninstallFacebook(index, ld_path_console, package_name, timeout=20):
    subprocess.run([ld_path_console, 'uninstallapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(2)
    return True

## Cài facebook
def InstallFacebook(template_path, index, ld_path_console, apk_path, timeout=20):
    command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # print("Installing Facebook...")
    DemThoiGian(5)
    return True

## Mở app Facebook
def OpenApp(index, ld_path_console, package_name):
    subprocess.run([ld_path_console, 'runapp', '--index', str(index), '--packagename', package_name], check=True)
    DemThoiGian(4)
    return True

def QuitLD(index, ld_path_console, ld_path_instance):
    RemoveProxy(index, ld_path_console)
    DemThoiGian(2)
    command = f'{ld_path_console} quit --index {index}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    DemThoiGian(1)
    # ClearCache(index, ld_path_instance)
    return True

def DemThoiGian(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\nThời gian đợi: {remaining} giây")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")
    sys.stdout.flush()

def TimAnhSauKhiChupVaSoSanhv2(template_path, index, ld_path_console, confidence=0.7, max_attempts=2, delay=0.25, check_attempt=False):
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
                print(f"\nĐộ khớp v2 instance {index} {file_name}: {max_val * 100:.2f}%")
                
                if max_val >= confidence:
                    # Nếu khớp, trả về chỉ số template và tọa độ
                    x, y = max_loc
                    h, w = template.shape
                    center_x, center_y = x + w // 2, y + h // 2
                    return (center_x, center_y, i)  # Trả về index của template cùng với tọa độ

            # Nếu không có template nào khớp
            if check_attempt:
                sys.stdout.write(f"\nKhông tìm thấy template phù hợp. Thử lại lần {attempts + 1}/{max_attempts}")
                sys.stdout.flush()
                attempts += 1
                if attempts >= max_attempts:
                    print("\nKhông tìm thấy hình sau nhiều lần thử.")
                    return None
                time.sleep(delay)
        finally:
            if os.path.exists(local_screenshot_path):
                pass
                # os.remove(local_screenshot_path)

def TimAnhTheoTextVaSoSanh(multiple_texts, index, ld_path_console, max_attempts=2, delay=2, check_attempt=False):
    xml_dump_path = f"./window_dump{index}.xml"
    if isinstance(multiple_texts, str):
        multiple_texts = [multiple_texts]
    elif isinstance(multiple_texts, list):
        # Đảm bảo multiple_texts là danh sách, không cần thay đổi gì thêm
        pass
    else:
        raise ValueError("multiple_texts phải là một chuỗi hoặc danh sách chuỗi")    

    def DumpXML(index, xml_path, ld_path_console):
        """
        Hàm dump file XML từ LDPlayer.
        """
        command = f'{ld_path_console} adb --index {index} --command "shell uiautomator dump /sdcard/window_dump.xml"'
        subprocess.run(command, shell=True, stderr=subprocess.DEVNULL)
        pull_command = f'{ld_path_console} adb --index {index} --command "pull /sdcard/window_dump.xml {xml_path}"'
        subprocess.run(pull_command, shell=True, stderr=subprocess.DEVNULL)

    attempts = 0
    while True:
        try:
            # Dump file XML
            DumpXML(index, xml_dump_path, ld_path_console)

            # Kiểm tra file XML dump
            if not os.path.exists(xml_dump_path):
                raise FileNotFoundError(f"Không tìm thấy file dump XML tại {xml_dump_path}")

            # Parse file XML
            tree = ET.parse(xml_dump_path)
            root = tree.getroot()

            # Tìm kiếm từng văn bản trong danh sách
            for array_index, text in enumerate(multiple_texts):
                for node in root.iter("node"):
                    if text in node.attrib.get("text", ""):
                        # Lấy tọa độ từ thuộc tính bounds
                        bounds = node.attrib.get("bounds", "")
                        if bounds:
                            # Phân tích tọa độ từ bounds (vd: [x1,y1][x2,y2])
                            bounds = bounds.replace("]", ",").replace("[", "").strip(",")
                            coords = list(map(int, bounds.split(",")))
                            if len(coords) == 4:
                                x1, y1, x2, y2 = coords
                                center_x = (x1 + x2) // 2
                                center_y = (y1 + y2) // 2
                                return (center_x, center_y, array_index)
                                # results.append((center_x, center_y, array_index))

            # if results:
            #     return results

            # Nếu không tìm thấy text
            if check_attempt:
                sys.stdout.write(f"\nKhông tìm thấy văn bản phù hợp. Thử lại lần {attempts + 1}/{max_attempts}")
                sys.stdout.flush()

            attempts += 1
            if attempts >= max_attempts:
                print("\nKhông tìm thấy văn bản sau nhiều lần thử.")
                return None

            time.sleep(delay)
        finally:
            # Dọn dẹp file dump nếu cần thiết
            if os.path.exists(xml_dump_path):
                # os.remove(xml_dump_path)  # Bỏ comment nếu muốn tự động xóa file dump
                pass

def TimAnhSauKhiChupVaSoSanh(template_path, index, ld_path_console, confidence=0.7, max_attempts=2, delay=2, check_attempt=False):
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
                print(f"\nĐộ khớp instance {index} {file_name}: {max_val * 100:.2f}%")
                
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

def CapQuyenTruyCapChoFacebookLite(index, ld_path_console, package_name):
    permissions = [
        "android.permission.MANAGE_EXTERNAL_STORAGE",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_CALENDAR",
        "android.permission.READ_PHONE_STATE",
        "android.permission.READ_CALL_LOG",
        "android.permission.CAMERA",
    ]
    print(f"Đang cấp quyền Facebook... cho {index}")
    for permission in permissions:
        command = f'{ld_path_console} adb --index {index} --command "shell pm grant {package_name} {permission}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # print(f"Đang cấp quyền {permission}: {result.stderr}")
        if result.returncode != 0:
            print(f"Failed to grant {permission}: {result.stderr}")

# Xử lý hành động của user 
def GoText(index, ld_path_console, text, x, y):
    if x is not None and y is not None:
        # Tap vào vị trí trước khi nhập văn bản
        Tap(index, ld_path_console, x, y)

    for char in text:
        if char.isdigit():
            keycode = getattr(KeyCode, f"KEYCODE_{char}", None)
        elif char.isalpha():
            keycode = getattr(KeyCode, f"KEYCODE_{char.upper()}", None)
        elif char == ' ':
            keycode = KeyCode.KEYCODE_SPACE
        elif char == '.':
            keycode = KeyCode.KEYCODE_PERIOD
        elif char == '@':
            keycode = KeyCode.KEYCODE_AT
        elif char == '+':
            keycode = KeyCode.KEYCODE_PLUS
        else:
            print(f"Không hỗ trợ ký tự: {char}")
            continue

        if keycode is not None:
            command = f'{ld_path_console} adb --index {index} --command "shell input keyevent {keycode}"'
            # print(f"Command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Lỗi khi gửi sự kiện: {result.stderr}")

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
    if response.status_code == 200:
        EmailAdd = response.json().get("email")
        return EmailAdd
    return None  

def getHoTenRandom(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return random.choice(lines).strip()      

def calculate_luhn_check_digit(imei):
    sum_digits = 0
    for i in range(14):
        digit = imei[i]
        if i % 2 == 1:  # If the position is odd (0-based index), double it
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_digits += digit
    return (10 - (sum_digits % 10)) % 10

def generate_imei():
    imei = [random.randint(0, 9) for _ in range(14)]
    imei.append(calculate_luhn_check_digit(imei))
    return "".join(map(str, imei))

def GetPhone(country):
    if country == "VN":
        prefix = random.choice(["077", "093"])
        random_phone_number = prefix + ''.join(random.choices('0123456789', k=7))
    elif country == "USA":
        area_code = random.choice([
            "201", "305", "408", "617", "702", "818", "203", "860", "475", "959", "207", 
            "339", "351", "413", "617", "508", "774", "781", "857", "978", "603", "201", "551", "609", 
            "640", "732", "848", "856", "862", "908", "973", "212", "315", "332", "347", "516", "518", "585", 
            "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929", "934", "401", "215", 
            "223", "267", "272", "412", "484", "610", "717", "724", "814", "878", "802", "217", "224", "309", 
            "312", "331", "630", "618", "708", "773", "779", "815", "847", "872", "219", "260", "317", "765", 
            "574", "812", "930", "319", "515", "563", "641", "712", "316", "620", "785", "913", "231", "248", 
            "269", "313", "586", "517", "616", "734", "810", "906", "947", "989", "679", "218", "320", "507", 
            "612", "651", "763", "952", "314", "417", "573", "636", "660", "816", "308", "402", "531", "701", 
            "216", "234", "326", "330", "380", "419", "440", "513", "567", "614", "740", "937", "220", "605", 
            "262", "414", "608", "534", "715", "920", "274", "205", "251", "256", "334", "938", "479", "501", 
            "870", "302", "239", "305", "321", "352", "386", "407", "686", "561", "727", "754", "772", "786", 
            "813", "850", "863", "904", "941", "954", "229", "404", "470", "478", "678", "706", "762", "770", 
            "912", "270", "364", "606", "502", "859", "225", "318", "337", "504", "985", "240", "301", "410", 
            "443", "667", "228", "601", "662", "769", "252", "336", "704", "743", "828", "910", "919", "980", 
            "984", "405", "580", "918", "539", "803", "843", "854", "864", "423", "615", "629", "731", "865", 
            "901", "931", "210", "214", "254", "325", "281", "346", "361", "409", "430", "432", "469", "512", 
            "682", "713", "726", "737", "806", "817", "830", "832", "903", "915", "936", "940", "956", "972", 
            "979", "276", "434", "540", "571", "703", "757", "804", "304", "681", "907", "479", "501", "870", 
            "209", "213", "279", "310", "323", "341", "408", "415", "424", "442", "510", "530", "559", "562", 
            "619", "626", "628", "650", "657", "661", "669", "707", "714", "747", "760", "805", "818", "820", 
            "831", "858", "909", "916", "925", "949", "951", "303", "719", "720", "970", "808", "208", "986", 
            "406", "702", "725", "775", "505", "575", "503", "541", "971", "458", "435", "801", "385", "206", 
            "253", "360", "425", "509", "564", "307"
        ])
        central_office_code = ''.join(random.choices('0123456789', k=3))
        line_number = ''.join(random.choices('0123456789', k=4))
        random_phone_number = f"+1{area_code}{central_office_code}{line_number}"
    elif country == "TW":
        prefix = random.choice(["8862", "8863", "8864", "8866", "8867", "8868", "8869"])
        local_number = ''.join(random.choices('0123456789', k=6))
        random_phone_number = f"{prefix}{local_number}"
    else:
        raise ValueError("Unsupported country. Please use 'VN', 'USA', or 'TW'.")
    
    return random_phone_number

def ThietLapThongSoThietbi(index, ld_path_console):
    resolutions = [
        (1080, 1920),
        (900, 1600),
        (720, 1280),
        (540, 960),
        (1440, 2560),  # Additional common phone resolutions
        (1080, 2400),
        (720, 1520),
    ]

    manufacturers_and_models = {
        "samsung": [
            "SM-S9180",
            "SM-X910N",
            "SM-X810N",
            "SM-X710N",
            "SM-S906B",
            "SM-S906N",
            "SM-S9280",
            "SM-S9260",
            "SM-S9210",
            "SM-S9160",
            "SM-S9110",
            "SM-N9860",
            "SM-N9810",
        ],
        "Xiaomi": ["23116PN5BC", "23127PN0CC", "2304FPN6DG", "2210132C", "2211133C", "2203121C", "MI 9"],
        "Redmi": ["23133RKC6C", "2311DRK48C", "22127RK46C", "23078RKD5C", "22081212C"],
        "Google phone": ["G576D", "GFE4J", "G82U8"],
        "ROG": ["ASUS_AI2401_A", "ROG Phone 7 Ultimate", "ASUS_AI2205_A", "ASUS AI2201_B"],
        "OnePlus": ["PJD110", "PHB110", "NE210", "HD1910", "HD1900", "GM1910", "GM1900"],
        "SONY": ["XQ-BE42", "XQ-AQ05", "SO-41B", "SO-02L", "SOV44"],
        "AQUOS": ["A208SH", "SH-M24", "SHG07"],
        "vivo": ["V2329A", "V2307A", "V2218A", "V2217A", "V2324A", "V2309A", "V2266A", "V2229A", "V2242A", "V2241A", "V2339A", "V2338A"],
        "OPPO": ["PJJ110", "PJH110", "PHW110", "PHM110", "PHY110", "PHZ110", "PGEM10", "PGFM10"],
    }

    manufacturer = random.choice(list(manufacturers_and_models.keys()))
    model = random.choice(manufacturers_and_models[manufacturer])
    resolution = random.choice(resolutions)
    cpu_cores = random.randint(1, 3)
    ram = random.choice([2048, 4096])
    imei = generate_imei()

    device = {
        "manufacturer": manufacturer,
        "model": model,
        "resolution": f"{resolution[0]}x{resolution[1]}",
        "cpu_cores": cpu_cores,
        "ram": ram,
        "imei": imei,
    }

    try:
        # Command to set LDPlayer properties using ldconsole.exe modify
        modify_command = [
            ld_path_console,
            "modify",
            "--index",
            f"{index}",
            "--cpu",
            f"{device['cpu_cores']}",
            "--memory",
            f"{device['ram']}",
            "--imei",
            f"{device['imei']}",
            "--manufacturer",
            f"{device['manufacturer']}",
            "--model",
            f"{device['model']}",
            "--pnumber",
            "",
            # GetPhone(),
        ]
        subprocess.run(modify_command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to set device properties: {e}")
        return False

def XacDinhToaDo(node):
    """Extract coordinates from the bounds attribute of a node."""
    if "bounds" in node.attrib:
        bounds = node.attrib["bounds"]
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
    return None, None

def XuatToaDo(file_path, resource_id):
    """Extract coordinates for all nodes with the specified resource-id."""
    try:
        print(f"Parsing XML file at {file_path}")
        tree = ET.parse(file_path)
        root = tree.getroot()

        coordinates_list = []

        for node in root.iter("node"):
            if (
                "resource-id" in node.attrib
                and node.attrib["resource-id"] == resource_id
            ):
                coordinates = XacDinhToaDo(node)
                if coordinates != (None, None):
                    coordinates_list.append(coordinates)

        return coordinates_list

    except FileNotFoundError:
        print(f"XML file not found: {file_path}")
        return []
    except ET.ParseError as pe:
        print(f"Error parsing XML file: {pe}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def VuotChon(index, ld_path_console, x, y, direction="up", duration=20, times=1):
    for _ in range(times):
        if direction == "up":
            x_end, y_end = x, y - random.randint(100, 200)
        elif direction == "down":
            x_end, y_end = x, y + random.randint(100, 200)
        else:
            raise ValueError("Direction must be 'up' or 'down'")

        command = f'{ld_path_console} adb --index {index} --command "shell input swipe {x} {y} {x_end} {y_end} {duration}"'
        # print(f"Executing command: {command}")
        os.system(command)

def ChonNgayThangNamSinh(index, ld_path_console):
    # Dump UI map first
    DumpMap(ld_path_console)

    # Then proceed with extracting coordinates
    file_path = "./include/map/datePickerLocation.xml"
    resource_id = "android:id/numberpicker_input"

    result = XuatToaDo(file_path, resource_id)
    coordinates = {f"col {i+1}": coord for i, coord in enumerate(result)}

    config = {
        "col 1": {
            "direction": "down",
            "min_swipes": 1,
            "max_swipes": 6,
            "min_delay": 1,
            "max_delay": 1,
        },
        "col 2": {
            "direction": "down",
            "min_swipes": 1,
            "max_swipes": 30,
            "min_delay": 0,
            "max_delay": 1,
        },
        "col 3": {
            "direction": "up",
            "min_swipes": 12,
            "max_swipes": 18,
            "min_delay": 1,
            "max_delay": 1,
        },
    }

    selected_date = {}

    for name, coord in coordinates.items():
        if name in config:
            x, y = coord
            col_config = config[name]
            direction = col_config["direction"]
            min_swipes = col_config["min_swipes"]
            max_swipes = col_config["max_swipes"]
            min_delay = col_config["min_delay"]
            max_delay = col_config["max_delay"]

            times = random.randint(min_swipes, max_swipes)
            delay = random.uniform(min_delay, max_delay)

            # Perform the swipe action
            VuotChon(index, ld_path_console, x, y, direction=direction, times=times)
            time.sleep(delay)

            # Capture the selected value (this part is hypothetical and depends on your implementation)
            selected_value = LayGiaTriDaChon(ld_path_console, x, y)
            selected_date[name] = selected_value

    return selected_date

def LayGiaTriDaChon(ld_path_console, x, y):
    # This function should implement the logic to capture the selected value from the date picker
    # For example, it could use OCR or another method to read the value at the given coordinates
    pass

def DumpMap(ld_path_console, dump_file_path="include/map/datePickerLocation.xml"):
    try:
        # print(f"Creating directories for {dump_file_path}")
        os.makedirs(os.path.dirname(dump_file_path), exist_ok=True)
        dump_command = f'{ld_path_console} adb --index 0 --command "shell uiautomator dump"'
        # print(dump_command)
        result = subprocess.run(dump_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            print(f"Error while dumping UI: {result.stderr}")
            return False
        pull_command = f'{ld_path_console} adb --index 0 --command "pull /sdcard/window_dump.xml {dump_file_path}"'
        # print(pull_command)
        pull_result = subprocess.run(pull_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if pull_result.returncode != 0:
            print(f"Error while pulling XML file: {pull_result.stderr}")
            return False

        # print(f"File XML has been successfully dumped and pulled to: {dump_file_path}")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def getUID(cookie):
    match = re.search(r'c_user=(\d+)', cookie)
    return match.group(1) if match else None

def getAdbData(index, ld_path_console):
    result_data = {
        "uid": None,
        "cookie": None,
        "token": None
    }

    def XuLyAdbCommand(index, ld_path_console):
        # print(f"Starting XuLyAdbCommand with index: {index}")

        # Kiểm tra ADB root
        command = [ld_path_console, 'adb', '--index', f'{str(index)}', '--command', 'root']
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if "adbd is already running as root" in result.stdout:
                # print("ADB is running as root.")
                pass
            elif "permission denied" in result.stderr:
                print("Permission denied. ADB root access not available.")
                return None
            else:
                print("Unexpected output: " + result.stdout + result.stderr)
                return None
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return None

        # Lệnh 1: Copy file từ root vào SD card
        adb_command = f"{ld_path_console} adb --index {str(index)} --command \"shell su -c 'cp /data/data/com.facebook.lite/files/PropertiesStore_v02 /sdcard/'\""
        try:
            result = subprocess.run(adb_command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return None

        # Lệnh 2: Pull file từ SD card về local
        pull_command = [
            ld_path_console, 
            'adb', 
            '--index', str(index), 
            '--command', 
            f'pull /sdcard/PropertiesStore_v02 include/authorFiles/PropertiesStore_v02_{index}'
        ]

        try:
            # subprocess.run(['adb', 'devices'])
            result = subprocess.run(pull_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            return None

        #Lệnh 3: Xóa file từ SD card
        delete_command = "rm /sdcard/PropertiesStore_v02"
        adb_delete_command = [ld_path_console, 'adb', '--index', f'{str(index)}', '--command', "shell", "su", "-c"] + delete_command.split()
        try:
            subprocess.run(adb_delete_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Delete command failed: {e}")
            return None

        return "All commands executed successfully."

    def getCookie(index):
        local_file_path = f'include/authorFiles/PropertiesStore_v02_{index}'
        try:
            with open(local_file_path, 'r', encoding='latin-1') as file:
                data = file.read()
                json_array_data = re.search(r'\[.*\]', data)
                if json_array_data:
                    json_array_string = json_array_data.group(0)
                    cookies = json.loads(json_array_string)
                    return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return None, None

    def getToken(index):
        local_file_path = f'include/authorFiles/PropertiesStore_v02_{index}'
        try:
            with open(local_file_path, 'r', encoding='latin-1') as file:
                data = file.read()
                access_token_match = re.search(r'"access_token":"(.*?)"', data)
                return access_token_match.group(1) if access_token_match else None
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Execute the commands
    XuLyAdbCommand(index, ld_path_console)
    result_data = {
        "uid": getUID(getCookie(index)),
        "cookie": getCookie(index),
        "token":  getToken(index)
    }
    return json.dumps(result_data)

def RunLD(index, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath):
    max_iterations = 100  # Số lần lặp tối đa
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
            Isaccountexist1_done = False

            isInvalidPhone_done = False

            isStartedLD_done = False

            emailText = TaoEmail()
            passText = ''.join(random.choice(string.ascii_letters) for i in range(15))
            fieldFirstName = getHoTenRandom(fileTxtPath+'ho.txt')  
            fieldLastName = getHoTenRandom(fileTxtPath+'ten.txt')
            region = "USA"
            
            print(f"Email: {emailText}, Firstname: {fieldFirstName}, Lastname: {fieldLastName}, Pass: {passText}")

            isSetup = ThietLapThongSoThietbi(index, ld_path_console)
            if isSetup:
                pass
                # print(f"Đã thiết lập thông số thiết bị cho LDPlayer ld{index}.")

            if not isStartedLD_done:
                isStartLD = StartLD(Action.isStartedLD_Btn, index, ld_path_console)
                if isStartLD:
                    isStartedLD_done = True

            ## Connect LD với proxy
            if not isConnected_done:
                isConnected = ConnectProxy(index, ld_path_console, proxy_username, proxy_password, proxy_ip, proxy_port)
                if isConnected is True:
                    isConnected_done = True
                    pass
                else:
                    print(f"Không thể kết nối proxy {index}")
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
                    firstname_done = True

            # Nhập họ
            if not lastname_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.lastname_Btn, index, ld_path_console, confidence=0.5)
                if pos is not None:
                    GoText(index, ld_path_console, fieldLastName, pos[0], pos[1])
                    lastname_done = True

            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                pass

            validateNameSection = ['Select your name', 'We require everyone to use the name they use in everyday life, what their friends call them, on Facebook.', 'Set date']
            pos = TimAnhTheoTextVaSoSanh(validateNameSection, index, ld_path_console)
            if pos is not None and pos[2] == 0:
                print("Chọn họ tên")
                pos2 = TimAnhSauKhiChupVaSoSanh(Action.pickname_Btn, index, ld_path_console)
                Tap(index, ld_path_console, pos[0], pos[1])
            elif pos is not None and pos[2] == 1:
                print("Xóa text")
                pos2 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console)
                Tap(index, ld_path_console, pos[0], pos[1])
            else:
                if random.choice([True, False]):
                    print("Chọn ngày tháng năm sinh")
                    ChonNgayThangNamSinh(index, ld_path_console)
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
                    if pos2 is not None:
                        Tap(index, ld_path_console, pos2[0], pos2[1])
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            pass
                else:
                    print("Nhập ngày tháng năm sinh")
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.sett_Btn, index, ld_path_console)
                    if pos2 is not None:
                        Tap(index, ld_path_console, pos2[0], pos2[1])
                        print(pos2)

                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                        print("Click next 1")

                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                        print("Click next 2")
                                # pass
                    pos3 = TimAnhSauKhiChupVaSoSanh(Action.agefield_Btn, index, ld_path_console)
                    if pos3 is not None:
                        randomAge = str(random.randint(18, 36))
                        GoText(index, ld_path_console, randomAge, pos3[0], pos3[1])

                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                        pos4 = TimAnhSauKhiChupVaSoSanh(Action.okHideBirthDate_Btn, index, ld_path_console, confidence=0.5)
                        print("Click OK")

                    if pos4 is not None:
                        Tap(index, ld_path_console, pos4[0], pos4[1])

            # Click nút next
            # if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
            #     pass

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
                    GoText(index, ld_path_console, GetPhone(region), pos[0], pos[1])
                    mobilePhone_done = True    

            # click next
            if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                # Kiểm tra sdt đã được sử dụng chưa 2 trường hợp 
                # 1 là số điện thoại đã được sử dụng
                # 2 là không tìm thấy tài khoản(dựa theo sdt)
                pos = TimAnhSauKhiChupVaSoSanhv2(Action.wecounldntfindyouaccount_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    print("Không tìm thấy tài khoản")
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.wecoulndfindyouraccountOk_Btn, index, ld_path_console)
                    if pos2 is not None:
                        Tap(index, ld_path_console, pos2[0], pos2[1])
                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            Isaccountexist1_done = True
                            pass
                else:
                    isPhoneEmailSection = ['The phone number you’re trying to verify was recently used to verify a different account. Please try a different number.',
                    'Looks like your mobile number may be incorrect. Try entering your full number, including the country code.']
                    pos = TimAnhTheoTextVaSoSanh(isPhoneEmailSection, index, ld_path_console)
                    print("Phone Email Section: ", pos)
                    if pos is not None and (pos[2] == 0):
                        mobilePhone_done = False
                        print("Số điện thoại đã được sử dụng")
                        ## xóa text trong field và nhập lại
                        pos2 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console, confidence=0.6, max_attempts=2, check_attempt=True)
                        if pos2 is not None:
                            Tap(index, ld_path_console, pos2[0], pos2[1])
                            pos3 = TimAnhTheoTextVaSoSanh('Mobile number', index, ld_path_console)
                            if pos3 is not None:
                                GoText(index, ld_path_console, GetPhone(region), pos3[0], pos3[1])
                                mobilePhone_done = True
                                if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                                    pass
                    elif pos is not None and (pos[2] == 1):
                        print('Số điện thoại không hợp lệ')
                        # UninstallFacebook(index, ld_path_console, package_name)
                        # QuitLD(index, ld_path_console, ld_path_instance)
                        # continue
                        pos2 = TimAnhSauKhiChupVaSoSanh(Action.clearField_Btn, index, ld_path_console)
                        if pos2 is not None:
                            Tap(index, ld_path_console, pos2[0], pos2[1])

                        pos3 = TimAnhTheoTextVaSoSanh('Mobile number', index, ld_path_console)
                        if pos3 is not None:
                            GoText(index, ld_path_console, GetPhone(region), pos3[0], pos3[1])
                            mobilePhone_done = True

                        if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                            pass
                    else:
                        pass
                    

            if not doyouhaveaccount_done or not continueCreate_done:
                checkAccountPopupSection = [Action.doyouhaveaccount_Btn, Action.continuecreate_Btn]
                pos = TimAnhSauKhiChupVaSoSanhv2(template_path=checkAccountPopupSection, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    if pos[2] == 0:
                        print("Số điện thoại đã được sử dụng")
                        pos = TimAnhSauKhiChupVaSoSanh(Action.continuecreate_Btn, index, ld_path_console)
                        if pos is not None:
                            Tap(index, ld_path_console, pos[0], pos[1])
                            continueCreate_done = True
                    else:
                        print("Không tìm thấy tài khoản")
                        pos = TimAnhSauKhiChupVaSoSanh(Action.doyouhaveaccount_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                        if pos is not None:
                            Tap(index, ld_path_console, pos[0], pos[1])
                            doyouhaveaccount_done = True

            # Nhập password
            if not passwordField_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.passwordField_Btn, index, ld_path_console, confidence=0.5)
                if(pos != None):
                    GoText(index, ld_path_console, passText, pos[0], pos[1])      
                    # Click next
                    if XuLyNextButton(index, ld_path_console, Action.nextt_Btn):
                        pass             

            ## Chỗ này sẽ xuất hiện TH trùng account do sdt bị trùng từ trước => phải xử lý ở đây => Thoát app làm lại
            isAccountExist = ['Try another way', 'i don’t see my account', 'Choose your account']
            if not Isaccountexist_done:
                pos = TimAnhTheoTextVaSoSanh(isAccountExist, index, ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    print("Kiểm tra account đã tồn tại")
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
            issue282Check = [Action.issue282_Btn, Action.issue282v3_Btn, Action.isInvalidAccount_Btn, Action.wecounldntfindyouaccountv2_Btn]
            if not issue282_done:
                is282 = TimAnhSauKhiChupVaSoSanhv2(template_path=issue282Check, index=index, ld_path_console=ld_path_console, max_attempts=2, check_attempt=True)
                if is282 is not None and (is282[2] == 0 or is282[2] == 1):
                    print(f"Email: {emailText} bị dính 282")
                else:
                    print(f"Ko thể tạo tài khoản với email: {emailText}")
                UninstallFacebook(index, ld_path_console, package_name)
                QuitLD(index, ld_path_console, ld_path_instance)
                continue                                           

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

            # Check dính sms limit => gõ lại email
            if not smslimitreached_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.smslimitreached_Btn, index, ld_path_console, max_attempts=2, check_attempt=True)
                if pos is not None:
                    pos2 = TimAnhSauKhiChupVaSoSanh(Action.smsreachlimitfield_Btn, index, ld_path_console)
                    if pos2 is not None:
                        GoText(index, ld_path_console, emailText, pos2[0], pos2[1])
                        pos3 = TimAnhSauKhiChupVaSoSanh(Action.smsreachlimitAdd_Btn, index, ld_path_console)
                        if pos3 is not None:
                            Tap(index, ld_path_console, pos3[0], pos3[1])
                            smslimitreached_done = True

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
                
            # Click skip lần 1
            if not skip_lan2_done:
                pos = TimAnhSauKhiChupVaSoSanh(Action.skip_Btn, index, ld_path_console)
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
                            with open('uid.txt', 'a') as file2:
                                file2.write(uid + '\n')
                        successReg_done = True
                        DemThoiGian(2)
                        UninstallFacebook(index, ld_path_console, package_name)
                        QuitLD(index, ld_path_console, ld_path_instance)
                        # quit()
            time.sleep(1)
            counter += 1
    except KeyboardInterrupt:
        print("Vòng lặp đã bị ngừng bằng Ctrl+C.")