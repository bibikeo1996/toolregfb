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

def get_text_input_fields():
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
            return []
        
        # Phân tích file XML
        print("Đang tìm kiếm các trường nhập liệu văn bản...")
        tree = ET.parse("window_dump.xml")
        root = tree.getroot()

        text_input_fields = []  # Lưu danh sách các trường nhập liệu văn bản

        for node in root.iter("node"):
            element_info = {}
            
            # Phân tích các loại trường nhập liệu văn bản
            if "class" in node.attrib:
                element_class = node.attrib["class"]
                if "EditText" in element_class:
                    element_info["type"] = "Text Input"
                else:
                    continue  # Bỏ qua các element không phải trường nhập liệu văn bản
            
            # Lấy thêm thông tin bổ sung nếu có
            element_info["text"] = node.attrib.get("text", "")
            element_info["content-desc"] = node.attrib.get("content-desc", "")
            element_info["resource-id"] = node.attrib.get("resource-id", "")
            element_info["hint"] = node.attrib.get("hint", "")
            element_info["label"] = node.attrib.get("label", "")
            element_info["placeholder"] = node.attrib.get("placeholder", "")

            # Trích xuất tọa độ
            coordinates = XacDinhToaDo(node)
            if coordinates:
                element_info["coordinates"] = coordinates
                text_input_fields.append(element_info)

        # In kết quả
        if text_input_fields:
            print(f"Tìm thấy {len(text_input_fields)} trường nhập liệu văn bản:")
            for field in text_input_fields:
                print(f"Text: '{field['text']}', Content-Desc: '{field['content-desc']}', "
                      f"Resource-ID: '{field['resource-id']}', Hint: '{field['hint']}', "
                      f"Label: '{field['label']}', Placeholder: '{field['placeholder']}', "
                      f"Tọa độ: {field['coordinates']}")
        else:
            print("Không tìm thấy trường nhập liệu văn bản nào.")
        
        return text_input_fields

    except Exception as e:
        print(f"Lỗi: {e}")
        return []

# Gọi hàm
text_input_fields = get_text_input_fields()