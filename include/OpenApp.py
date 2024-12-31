import os
import subprocess
import time
import sys
import psutil
from dotenv import load_dotenv
from tabulate import tabulate
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
# Đọc các biến môi trường
ld_path_console = os.getenv('LD_PATH_CONSOLE')  # Đường dẫn tới LDPlayer
ld_path_exe = os.getenv('LD_PATH_EXE')  # Đường dẫn tới LDPlayer
apk_path = os.getenv('APK_PATH')  # Đường dẫn tới file APK
package_name = os.getenv('PACKAGE_NAME')  # Tên gói của ứng dụng
# brave_path = os.getenv('BRAVE_PATH')  # Đường dẫn tới trình duyệt Brave
# url = os.getenv('URL')  # URL cần mở trên trình duyệt

# def openBrave():
#     try:
#         options = webdriver.ChromeOptions()
#         options.binary_location = brave_path
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         driver.get(url)
#         global email_text, firstName, lastName, mi_value, phpsessid_value
#         email_element = driver.find_element(By.ID, "email")
#         email_text = email_element.text
#         local_part = email_text.split("@")[0]
#         firstName, lastName = local_part.split(".")
#         # Lấy cookie MI
#         mi_cookie = driver.get_cookie("MI")
#         mi_value = mi_cookie["value"] if mi_cookie else "Không tìm thấy cookie MI"

#         # Lấy cookie PHPSESSID
#         phpsessid_cookie = driver.get_cookie("PHPSESSID")
#         phpsessid_value = phpsessid_cookie["value"] if phpsessid_cookie else "Không tìm thấy cookie PHPSESSID"
#     except Exception as e:
#         print(f"Lỗi xảy ra: {e}")
#     finally:
#         # input("Nhấn Enter để đóng trình duyệt...")
#         driver.quit()
#         return {
#             "emailText": email_text,
#             "passText": firstName + lastName + '123456',
#             "fieldFirstName": firstName,
#             "fieldLastName": lastName,
#             "MI": mi_value,
#             "PHPSESSID": phpsessid_value
#         }

# def getMailCode(mi_value, phpsessid_value):
    # try:
    #     options = webdriver.ChromeOptions()
    #     options.binary_location = brave_path
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #     driver.get(url)
    #     driver.add_cookie({"name": "MI", "value": mi_value})
    #     driver.add_cookie({"name": "PHPSESSID", "value": phpsessid_value})
    #     driver.refresh()
    #     #get mail code
    #     confirmation_code_element = driver.find_element(By.CLASS_NAME, "predmet")
    #     confirmation_code_text = confirmation_code_element.text
    #     confirmation_code = confirmation_code_text.split(" ")[0]
    #     return confirmation_code

        
    # except Exception as e:
    #     print(f"Lỗi xảy ra: {e}")
    # finally:
    #     # input("Nhấn Enter để đóng trình duyệt...")
    #     driver.quit()

def ADBKillAndStartServer():
    kill_command = ["adb", "kill-server"]
    subprocess.run(kill_command)
    # print("ADB server stopped")
    start_command = ["adb", "start-server"]
    subprocess.run(start_command)
    # print("ADB server started")

def KhoiDongLDPlayer(index, ld_path_console=None):
    ldplayer_running = False
    while not ldplayer_running:
        command = f'{ld_path_console} adb --index {index} --command "shell getprop"'
        # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell getprop"]
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if "not found" in result.stdout.lower() or "not found" in result.stderr.lower():
            start_command = [ld_path_console, "launch", "--index", str(index)]
            subprocess.run(start_command)
            # print(f"{result.stdout}")
            time.sleep(1)
        else:
            # print(f"LDPlayer {index} is already running")
            ldplayer_running = True
    return True       

def DemThoiGian(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rThời gian đợi: {remaining} giây")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("")

# TrangThaiInstance(index, f"Instance {index} đã setup xong", saveText)
# def TrangThaiInstance(index, text, saveText={}):
#     saveText[index] = text
#     headers = [f"Index {i}" for i in saveText.keys()]
#     data = [[saveText[idx] for idx in saveText.keys()]]
#     table = tabulate(data, headers=headers, tablefmt="grid")
#     sys.stdout.write("\033[F" * (len(table.split("\n"))))
#     sys.stdout.write(table + "\n")
#     sys.stdout.flush()
            
def KiemTraDaCaiAppFaceBookLiteChua(index, target_app, apk_path, ld_path_console=None):
    command = f'{ld_path_console} adb --index {index} --command "shell pm list packages"'
    # command = [ld_path_console, "adb", "--index", str(index), "--command", "shell pm list packages"]
    result = subprocess.run(command, capture_output=True, text=True)
    # print(result.returncode)
    if result.returncode == 0:
        packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if ":" in line]
        for app in packages:
            if target_app.lower() in app.lower():
                return True
        install_command = f'{ld_path_console} adb --index {index} --command "install {apk_path}"'
        # install_command = [ld_path_console, "adb", "--index", str(index), "--command", f"install {apk_path}"]
        install_result = subprocess.run(install_command, capture_output=True, text=True)
        
        if install_result.returncode == 0:
            return True  # Sau khi cài thành công, trả về True
        else:
            print(f"Error installing {target_app}: {install_result.stderr}")
            return False  # Nếu cài không thành công, trả về False
    else:
        print(f"Error getting installed apps: {result.stderr}")
        return False  # Nếu không thể lấy danh sách ứng dụng, trả về False
