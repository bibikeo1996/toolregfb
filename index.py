import os
from dotenv import load_dotenv
#from include.isAppRunning import is_bluestacks_running, is_app_installed

from validate.proxy import KiemTraProxy
from app import OpenToolRegFaceBook
from include.isAppRunning import isBlueStackRunning
from include.deleteApp import xoa_app
# from validate.cookie import run_cookie
import include.defined as defined

# Load biến môi trường từ tệp .env nếu có
load_dotenv()

bluestacks_path = os.getenv('BLUESTACKS_PATH')
adb_path = os.getenv('ADB_PATH')
apk_path = os.getenv('APK_PATH') 
package_name = os.getenv('PACKAGE_NAME')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')

if isBlueStackRunning(bluestacks_path, adb_path, apk_path, package_name):
    # if KiemTraProxy(adb_path):
    #     pass
    # else:
    #     return False
    OpenToolRegFaceBook(adb_path, defined)
    print("Đã hoàn thành việc nhập dữ liệu test!")
    
    # gọi hàm delete app ngay đây
    # xoa_app(adb_path, package_name)
    # run_cookie()
    
else:
    print("Không thể chạy ứng dụng do một hoặc nhiều điều kiện không thỏa mãn.")
