import os
import subprocess
import re
import xml.etree.ElementTree as ET

def XacDinhToaDo(node):
    """Trích xuất tọa độ từ thuộc tính bounds của node."""
    if "bounds" in node.attrib:
        bounds = node.attrib["bounds"]
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
    return None, None

def get_all_interactive_elements():
    adb_path = r"C:\Users\patroids115\Desktop\platform-tools-latest-windows\platform-tools\adb.exe"  # Đường dẫn tới adb.exe
    
    try:
        # Tạo dump giao diện UI từ thiết bị
        print("Đang lấy giao diện từ thiết bị...")
        dump_command = [adb_path, "shell", "uiautomator", "dump", "/sdcard/window_dump.xml"]
        subprocess.run(dump_command, capture_output=True, text=True)
        
        # Sao chép file XML từ thiết bị về máy tính
        pull_command = [adb_path, "pull", "/sdcard/window_dump.xml", "./window_dump.xml"]
        subprocess.run(pull_command, capture_output=True, text=True)
        
        # Kiểm tra file dump có tồn tại không
        if not os.path.exists("window_dump.xml"):
            print("Không thể lấy file dump giao diện từ thiết bị.")
            return
        
        # Phân tích file XML
        print("Đang tìm kiếm các element có thể tương tác...")
        tree = ET.parse("window_dump.xml")
        root = tree.getroot()

        interactive_elements = []  # Lưu danh sách các element

        for node in root.iter("node"):
            element_info = {}
            
            # Phân tích các loại element
            if "class" in node.attrib:
                element_class = node.attrib["class"]
                element_info["class"] = element_class  # Add class name to element_info
                if "EditText" in element_class:
                    element_info["type"] = "Text Input"
                elif "Button" in element_class:
                    element_info["type"] = "Button"
                elif "CheckBox" in element_class:
                    element_info["type"] = "Checkbox"
                elif "RadioButton" in element_class:
                    element_info["type"] = "Radio Button"
                elif node.attrib.get("clickable") == "true":
                    element_info["type"] = "Clickable Element"
                else:
                    continue  # Bỏ qua các element không phải loại tương tác
            
            # Lấy thêm thông tin bổ sung nếu có
            element_info["text"] = node.attrib.get("text", "")
            element_info["content-desc"] = node.attrib.get("content-desc", "")
            element_info["resource-id"] = node.attrib.get("resource-id", "")

            # Trích xuất tọa độ
            coordinates = XacDinhToaDo(node)
            if coordinates:
                element_info["coordinates"] = coordinates
                interactive_elements.append(element_info)

        # In kết quả
        if interactive_elements:
            print(f"Tìm thấy {len(interactive_elements)} element tương tác:")
            for element in interactive_elements:
                print(f"Loại: {element['type']}"
                      f"Class: '{element['class']}'"
                      f"Text: '{element['text']}'"
                      f"Content-Desc: '{element['content-desc']}'"
                      f"Resource-ID: '{element['resource-id']}'"
                      f"Tọa độ: {element['coordinates']}'")
        else:
            print("Không tìm thấy element tương tác nào.")
        
        return interactive_elements

    except Exception as e:
        print(f"Lỗi: {e}")
        return []

# Gọi hàm
interactive_elements = get_all_interactive_elements()
