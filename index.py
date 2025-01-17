import time
import os
import argparse
import threading
import concurrent.futures
import signal

from include.run import RunLD
from include.quitInstance import *
from dotenv import load_dotenv

load_dotenv()
ld_path_console = os.getenv('LD_PATH_CONSOLE')
ld_path_exe = os.getenv('LD_PATH_EXE')
ld_path_instance = os.getenv('LD_PATH_INSTANCE')
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH')
package_name = os.getenv('PACKAGE_NAME')
fileTxtPath = os.getenv('FILE_TXT')
proxy_ip = os.getenv('PROXY_IP')
proxy_port = os.getenv('PROXY_PORT')
proxy_username = os.getenv('PROXY_USER')
proxy_password = os.getenv('PROXY_PASS')
null = None


# Biến toàn cục để xử lý dừng bằng Ctrl+C
is_running = True


def signal_handler(sig, frame):
    global is_running
    print("Đang dừng...")
    is_running = False


signal.signal(signal.SIGINT, signal_handler)  # Bắt tín hiệu Ctrl+C


def task(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath):
    """
    Hàm task để chạy từng instance LDPlayer độc lập.
    """
    print(f"Khởi động instance {i}")
    while is_running:
        try:
            # Thay RunLD bằng logic thực tế của bạn để chạy một instance LDPlayer
            RunLD(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath)
            print(f"Instance {i} đang chạy...")
            break
        except Exception as e:
            print(f"Lỗi trong instance {i}: {e}")
            time.sleep(1)  # Đợi trước khi thử lại nếu có lỗi


if __name__ == "__main__":
    try:
        # Bắt đầu server ADB
        ADBKillAndStartServer()
        # Chạy 3 instance độc lập
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for i in range(2):  # Tạo 3 instance
                futures.append(executor.submit(task, i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath))

            # Duy trì vòng lặp để xử lý ngắt Ctrl+C
            while is_running:
                time.sleep(0.1)  # Giảm tải CPU

            # Chờ tất cả các thread hoàn thành
            for future in futures:
                future.cancel()  # Hủy thread còn đang chạy (nếu có)
    except Exception as e:
        print(f"Lỗi chính: {e}")
    finally:
        print("Đã thoát chương trình.")
