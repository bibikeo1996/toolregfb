import subprocess
import xml.etree.ElementTree as ET
import time

def click_button_by_text(adb_path, text_label):
    def get_elements_with_text(adb_path, text_label):
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
                pass
                #print(f"Element with text: {elem.attrib['text']}")
                if elem.attrib['text'].lower() == text_label.lower():
                    bounds = elem.attrib['bounds']
                    click_button_by_bounds(adb_path, bounds)
                    return True
            if 'content-desc' in elem.attrib and elem.attrib['content-desc']:
                pass
                #print(f"Element with content-desc: {elem.attrib['content-desc']}")
        return False

    def click_button_by_bounds(adb_path, bounds):
        # Phân tích tọa độ từ thuộc tính bounds
        bounds = bounds.replace('][', ',').replace('[', '').replace(']', '')
        coords = bounds.split(',')
        x = (int(coords[0]) + int(coords[2])) // 2
        y = (int(coords[1]) + int(coords[3])) // 2

        # Sử dụng adb để nhấp vào tọa độ
        command = [adb_path, "shell", "input", "tap", str(x), str(y)]
        subprocess.run(command, capture_output=True, text=True)
        print(f"Đã nhấp vào '{text_label}' tại tọa độ: ({x}, {y})")

    # Gọi hàm để hiển thị các phần tử có văn bản là nút và nhấp vào nút có văn bản tương ứng
    return get_elements_with_text(adb_path, text_label)

def wait_for_element(adb_path, text_label, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if click_button_by_text(adb_path, text_label):
            return True
        time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
    return False