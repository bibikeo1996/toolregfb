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
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH')
package_name = os.getenv('PACKAGE_NAME')
null = None

if __name__ == "__main__":
    try:
        ADBKillAndStartServer()

        def task(i, apk_path, package_name):
            RunLD(i, apk_path, package_name)

        threads = []
        i = 1
        for i in range(4):
            t = threading.Thread(target=task, args=(i, apk_path, package_name))
            threads.append(t)
            t.start()
            time.sleep(1)  # Delay of 1 second before starting the next thread

        for t in threads:
            t.join()
    except Exception as e:
        print(f"Lỗi: {e}")