import subprocess
import time
import xml.etree.ElementTree as ET


# Ví dụ sử dụng
# result = KiemTraVaClickElement(adb_path, text=noneOfTheABove, click=True)
# if result is True:
#     # Phần này dùng để click
# else:
#     print(result)
#
# result = KiemTraVaClickElement(adb_path, text=noneOfTheABove, click=False)
# if result is True:
#     # Phần này dùng để kiểm tra
# else:
#     print(result)

def KiemTraVaClickElement(adb_path, text=None, element_id=None, class_name=None, click=False, timeout=30, quick_check=False):
    def dump_ui():
        command = [adb_path, "shell", "uiautomator", "dump", "/sdcard/window_dump.xml"]
        subprocess.run(command, capture_output=True, text=True)
        command = [adb_path, "pull", "/sdcard/window_dump.xml", "./window_dump.xml"]
        subprocess.run(command, capture_output=True, text=True)

    def parse_xml():
        tree = ET.parse('window_dump.xml')
        return tree.getroot()

    def click_element(bounds):
        bounds = bounds.replace('][', ',').replace('[', '').replace(']', '')
        coords = bounds.split(',')
        x = (int(coords[0]) + int(coords[2])) // 2
        y = (int(coords[1]) + int(coords[3])) // 2
        command = [adb_path, "shell", "input", "tap", str(x), str(y)]
        subprocess.run(command, capture_output=True, text=True)
        print(f"Clicked vào tọa độ: ({x}, {y})")

    start_time = time.time()
    dump_ui()
    root = parse_xml()
    while time.time() - start_time < timeout:
        for elem in root.iter('node'):
            if text:
                for t in text:
                    if elem.attrib.get('text', '').lower() == t.lower():
                        if click:
                            # Phần này dùng để click
                            click_element(elem.attrib['bounds'])
                        return True
            if element_id and elem.attrib.get('resource-id') == element_id:
                if click:
                    # Phần này dùng để click
                    click_element(elem.attrib['bounds'])
                return True
            if class_name and elem.attrib.get('class') == class_name:
                if click:
                    # Phần này dùng để click
                    click_element(elem.attrib['bounds'])
                return True
        if quick_check:
            return False
            
        #time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại

    if text:
        return f"Error: Element with text '{text}' not found within {timeout} seconds."
    if element_id:
        return f"Error: Element with ID '{element_id}' not found within {timeout} seconds."
    if class_name:
        return f"Error: Element with class name '{class_name}' not found within {timeout} seconds."

    return "Error: No validation criteria provided."