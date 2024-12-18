import os
import subprocess
import time
import random
import requests
from dotenv import load_dotenv
from include.detectClick import KiemTraVaClickElement
from include.detectFields import XacDinhLoaiField, NhapTextVaoField
from include.detectNumPicker import ChonNgayThangNamSinh
# from validate.validate import KiemTraVaClickElement, KiemTraClassCoTonTai

load_dotenv()

bluestacks_path = os.getenv('BLUESTACKS_PATH')
adb_path = os.getenv('ADB_PATH')
package_name = os.getenv('PACKAGE_NAME')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')

def OpenToolRegFaceBook(adb_path, defined):
    print("Đang mở ứng dụng Facebook Lite...")
    start_app_command = [adb_path, "shell", "am", "start", "-n", "com.facebook.lite/.MainActivity"]
    subprocess.run(start_app_command)
    #time.sleep(5)  # Đợi ứng dụng khởi động

    # Nhập dữ liệu test
    print("Đang nhập dữ liệu test...")

    if KiemTraVaClickElement(adb_path, text=defined.noneOfTheABove, click=True):
        pass
    else: 
        pass

    #tạo tài khoản
    if KiemTraVaClickElement(adb_path, text=defined.createBtn, click=True):
        pass

    if KiemTraVaClickElement(adb_path, text=defined.getStartedBtn, click=True):
        pass
    else:
        pass

    textFullName = ["John", "Doe"]
    ToaDoField = XacDinhLoaiField(adb_path, "EditText")
    if NhapTextVaoField(adb_path, ToaDoField, textFullName):
        pass
    else:
        print("Không thể nhập tất cả các trường.")
        return

    if KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True):
        pass

    if KiemTraVaClickElement(adb_path, text=defined.useadifferentnameBtn, click=False, quick_check=True):
        KiemTraVaClickElement(adb_path, class_name="android.widget.RadioButton", click=True)
        KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True)
        pass
    else: 
        pass

    if KiemTraVaClickElement(adb_path, element_id="android:id/numberpicker_input", click=False, quick_check=True):
        time.sleep(1)
        interactive_elements = ChonNgayThangNamSinh(adb_path, specific_id="android:id/numberpicker_input")
    else:
        print("Không thể tìm thấy element.")
        return

    if KiemTraVaClickElement(adb_path, text=defined.setBtn, click=True):
        pass

    if KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True):
        pass    

    ## Chọn giới tính
    if KiemTraVaClickElement(adb_path, text=defined.isMale, click=False):
        gender = random.choice([defined.isMale, defined.isFemale])
        KiemTraVaClickElement(adb_path, text=gender, click=True)
        pass    

    if KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True):
        pass

    ## Kiểm tra cho phép Facebook truy cập danh bạ
    if KiemTraVaClickElement(adb_path, element_id="com.android.packageinstaller:id/permission_deny_button", click=False, quick_check=True):
        KiemTraVaClickElement(adb_path, text=defined.denyBtn, click=True)
        pass

    # Kiểm tra popup khác
    if KiemTraVaClickElement(adb_path, element_id="com.android.packageinstaller:id/permission_deny_button", click=False, quick_check=True):
        KiemTraVaClickElement(adb_path, text=defined.denyBtn, click=True)

    # Kiểm tra nút "search by email"
    if KiemTraVaClickElement(adb_path, text=defined.searchbyEmailBtn, click=False, quick_check=True):
        KiemTraVaClickElement(adb_path, text=defined.backBtn, click=True)
        
    if KiemTraVaClickElement(adb_path, text=defined.signupWithEmailBtn, click=True):
        pass
    
    # if KiemTraVaClickElement(adb_path, defined.signupWithPhoneBtn):
    #     pass

    emailText = ["daylamaitest@gmail.com"]
    ToaDoField = XacDinhLoaiField(adb_path, "EditText")
    if NhapTextVaoField(adb_path, ToaDoField, emailText):
        KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True)
        pass

    if KiemTraVaClickElement(adb_path, text=defined.showPassWordBtn, click=True, quick_check=True):
        pass

    passText = ["daylapassconcu"]
    ToaDoField = XacDinhLoaiField(adb_path, "EditText")
    if NhapTextVaoField(adb_path, ToaDoField, passText):
        KiemTraVaClickElement(adb_path, text=defined.nextBtn, click=True)
        pass

    if KiemTraVaClickElement(adb_path, text=defined.notnowBtn, click=True):
        pass

    if KiemTraVaClickElement(adb_path, text=defined.iagreeBtn, click=True):
        pass