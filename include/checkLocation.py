import subprocess
import uiautomator2 as u2
import time
import xml.etree.ElementTree as ET
import re

def KetNoiLDVaUiautomator(index, ldconsole_path):
    try:
        adb_command = [ldconsole_path, "adb", "--index", str(index), "--command", "devices"]
        result = subprocess.check_output(adb_command, universal_newlines=True)
        if "device" not in result:
            print(f"Không tìm thấy thiết bị ADB nào cho instance LDPlayer index {index}.")
            return None
        port = LayPortTheoIndex(index)
        device_ip_port = f"127.0.0.1:{port}"
        device = u2.connect(device_ip_port)
        if device:
            return device
        print(f"Không tìm thấy cổng ADB cho instance LDPlayer index {index}.")
        return None
    except Exception as e:
        print(f"Lỗi khi kết nối LDPlayer hoặc uiautomator2: {e}")
        return None


def LayThongTinElement(ui_hierarchy):
    try:
        root = ET.fromstring(ui_hierarchy)
        element_infos = []
        for node in root.iter():
            element_info = {}
            if "class" in node.attrib and (node.attrib["class"] == "android.widget.Button" or node.attrib["class"] == "android.widget.EditText"):
                content_desc = node.attrib.get("content-desc")
                if content_desc:
                    element_info["content-desc"] = content_desc
                if element_info:
                    element_infos.append(element_info)
        return element_infos
    except Exception as e:
        print(f"Lỗi khi phân tích XML cây giao diện: {e}")
        return []


def TheoDoiGiaoDien(device, check_keywords):
    if not device:
        print("Không có thiết bị để theo dõi.")
        return False

    ui_state_before = device.dump_hierarchy()
    try:
        while True:
            ui_state_after = device.dump_hierarchy()
            if ui_state_before != ui_state_after:
                element_infos = LayThongTinElement(ui_state_after)
                if element_infos:
                    found_keywords = 0
                    for keyword in check_keywords:
                        for info in element_infos:
                            if 'content-desc' in info and keyword.lower() in info['content-desc'].lower():
                                found_keywords += 1
                                break
                    if found_keywords == len(check_keywords):
                        return True
                ui_state_before = ui_state_after
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Dừng theo dõi giao diện.")
        return False
    except Exception as e:
        print(f"Lỗi trong quá trình theo dõi: {e}")
        return False


def LayPortTheoIndex(index):
    try:
        result = subprocess.run(
            ['adb', 'devices'],
            stdout=subprocess.PIPE, text=True
        )
        output = result.stdout
        emulator_matches = re.findall(r'emulator-(\d+)', output)
        if emulator_matches:
            if index < len(emulator_matches):
                emulator = emulator_matches[index]
                adb_port = int(emulator) + 1
                return adb_port
            else:
                return f"Index {index} không hợp lệ. Có {len(emulator_matches)} emulator đang chạy."
        else:
            return "Không tìm thấy emulator nào đang kết nối."
    except Exception as e:
        print(f"Lỗi khi lấy thông tin ADB: {e}")
        return None


# def main():
#     ldconsole_path = r"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" 
#     index = 1
#     device = KetNoiLDVaUiautomator(index, ldconsole_path)

#     check_keywords = ['Create new account', 'Log in', 'Forgot password?', 'English (US)']
#     isCreatePage = TheoDoiGiaoDien(device, check_keywords)
#     if isCreatePage:
#         print("Đã mở trang tạo tài khoản thành công.")
    
#     check_keywords = ['Get started', 'Find my account']
#     isGetStarted = TheoDoiGiaoDien(device, check_keywords)
#     if isGetStarted:
#         print("Đã mở trang tìm tài khoản thành công.")

# if __name__ == "__main__":
#     main()
