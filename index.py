import time
import os
import argparse
import threading

from include.run import RunLD
from include.OpenApp import ADBKillAndStartServer
# from include.OpenApp import install_apk, start_ldplayer, is_ldplayer_running, KiemTraLD_ChayChua
from dotenv import load_dotenv

load_dotenv()
ld_path_console = os.getenv('LD_PATH_CONSOLE')
ld_path_exe = os.getenv('LD_PATH_EXE')
ld_path_instance = os.getenv('LD_PATH_INSTANCE')
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH')
package_name = os.getenv('PACKAGE_NAME')
null = None

if __name__ == "__main__":
    try:    
        try:
            ADBKillAndStartServer()

            def task(i, apk_path, package_name, ld_path_console, ld_path_instance):
                RunLD(i, apk_path, package_name, ld_path_console, ld_path_instance)

            threads = []
            for i in range(5):
                t = threading.Thread(target=task, args=(i, apk_path, package_name, ld_path_console, ld_path_instance))
                threads.append(t)
                t.start()
                time.sleep(2)  # Delay of 1 second before starting the next thread

            for t in threads:
                t.join()
        except Exception as e:
            print(f"Lỗi: {e}")
    except KeyboardInterrupt:
        print("Đã dừng.")        