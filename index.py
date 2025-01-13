import time
import os
import argparse
import threading

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

if __name__ == "__main__":
    try:    
        try:
            ADBKillAndStartServer()

            def task(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath):
                RunLD(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath)

            threads = []
            for i in range(1):
                t = threading.Thread(target=task, args=(i, apk_path, package_name, ld_path_console, ld_path_instance, proxy_username, proxy_password, proxy_ip, proxy_port, fileTxtPath))
                threads.append(t)
                t.start()
                time.sleep(5)  # Delay of 1 second before starting the next thread

            for t in threads:
                t.join()
        except Exception as e:
            print(f"Lỗi index: {e}")
    except KeyboardInterrupt:
        print("Đã dừng.")        