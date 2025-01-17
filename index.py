import time
import os
import argparse
import threading
import concurrent.futures
import signal
import multiprocessing
import sys

from include.run import *
from dotenv import load_dotenv
from colorama import init, Fore

# Khởi tạo colorama
init(autoreset=True)

# Danh sách màu sắc để phân biệt các instance
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA]


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


is_running = True

def signal_handler(sig, frame, processes):
    global is_running
    print("Đang dừng...")
    is_running = False

    # Dừng tất cả các tiến trình
    for p in processes:
        p.terminate()
    print("Tất cả các tiến trình đã dừng.")
    
    # Thoát chương trình
    sys.exit(0)  # Dừng hoàn toàn chương trình

signal.signal(signal.SIGINT, signal_handler)  # Bắt tín hiệu Ctrl+C
def task(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy, fileTxtPath):
    color = colors[i % len(colors)]
    print(f"{color} Khởi động instance {i}")
    while is_running:
        try:
            # Thay RunLD bằng logic thực tế của bạn để chạy một instance LDPlayer
            RunLD(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy, fileTxtPath, color)
            print(f"Instance {i} đang chạy...")
            break
        except Exception as e:
            print(f"Lỗi trong instance {i}: {e}")
            time.sleep(1)  # Đợi trước khi thử lại nếu có lỗi

if __name__ == "__main__":
    try:
        # Bắt đầu server ADB
        ADBKillAndStartServer()
        # https://tq.lunaproxy.com/getflowip?neek=1518493&num=6&regions=us&ip_si=2&level=1&sb=
        # Chạy 3 instance độc lập
        proxy_list = [
            '43.159.29.44:20356',
            '43.159.29.44:20419',
            '43.159.29.44:20246',
            '43.159.29.44:20274',
            '43.159.29.44:20058',
            '43.159.29.44:20347'
        ]
        processes = []
        
        # Khởi tạo các tiến trình mới cho mỗi proxy trong danh sách
        for i, proxy in enumerate(proxy_list):
            if i > 0:
                time.sleep(3)
            p = multiprocessing.Process(target=task, args=(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy, fileTxtPath))
            p.start()  # Bắt đầu tiến trình
            processes.append(p)

        # Đăng ký xử lý tín hiệu Ctrl+C
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, processes))

        # Duy trì vòng lặp để xử lý ngắt Ctrl+C
        while True:
            try:
                time.sleep(0.1)  # Giảm tải CPU
            except KeyboardInterrupt:
                print("Process interrupted by user")
                break

        # Chờ tất cả các tiến trình hoàn thành
        for p in processes:
            p.join()

    except Exception as e:
        print(f"Lỗi chính: {e}")
    finally:
        print("Đã thoát chương trình.")


