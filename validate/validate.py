import subprocess
import xml.etree.ElementTree as ET
import time
import random

## Hàm này chỉ kiểm tra Element có tồn tại không, không tự động click
def KiemTraElementCoTonTaiKhong(adb_path, text=None, element_id=None, class_name=None):
    if text:
        command = [adb_path, "shell", "uiautomator", "dump"]
        subprocess.run(command)
        command = [adb_path, "shell", "grep", text, "/sdcard/window_dump.xml"]
        result = subprocess.run(command, capture_output=True, text=True)
        if text in result.stdout:
            return True
        else:
            return f"Error: Element with text '{text}' not found."
    
    if element_id:
        command = [adb_path, "shell", "uiautomator", "dump"]
        subprocess.run(command)
        command = [adb_path, "shell", "grep", element_id, "/sdcard/window_dump.xml"]
        result = subprocess.run(command, capture_output=True, text=True)
        if element_id in result.stdout:
            return True
        else:
            return f"Error: Element with ID '{element_id}' not found."
    
    if class_name:
        command = [adb_path, "shell", "uiautomator", "dump"]
        subprocess.run(command)
        command = [adb_path, "shell", "grep", class_name, "/sdcard/window_dump.xml"]
        result = subprocess.run(command, capture_output=True, text=True)
        if class_name in result.stdout:
            return True
        else:
            return f"Error: Element with class name '{class_name}' not found."
    
    return "Error: No validation criteria provided."

## Kiẻm tra class có tồn tại không - Hàm này sẽ không tự động click chỉ kiểm tra cho if else
# Example validate id class name hay text 
# print(validate_element(adb_path, text="example_text"))
# print(validate_element(adb_path, element_id="example_id"))
# print(validate_element(adb_path, class_name="example_class"))
def KiemTraClassCoTonTai(adb_path, text_label, timeout=30):
    def element_exists(adb_path, text_label):
        # Sử dụng uiautomator để tạo bản dump của giao diện người dùng
        command = [
            adb_path, "shell", "uiautomator", "dump", "/sdcard/window_dump.xml"
        ]
        subprocess.run(command, capture_output=True, text=True)

        # Kéo tệp XML về máy tính
        command = [
            adb_path, "pull", "/sdcard/window_dump.xml", "./window_dump.xml"
        ]
        subprocess.run(command, capture_output=True, text=True)

        # Phân tích tệp XML và tìm phần tử có thuộc tính text hoặc content-desc
        tree = ET.parse('window_dump.xml')
        root = tree.getroot()

        for elem in root.iter():
            if 'text' in elem.attrib and elem.attrib['text']:
                if elem.attrib['text'].lower() == text_label.lower():
                    return True
            if 'content-desc' in elem.attrib and elem.attrib['content-desc']:
                pass
        return False

    start_time = time.time()
    while time.time() - start_time < timeout:
        if element_exists(adb_path, text_label):
            return True
        time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
    return False    