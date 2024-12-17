import subprocess
import xml.etree.ElementTree as ET
import time
import re
def extract_coordinates(node):
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

def detect_field_type(adb_path, field_type="EditText"):
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

    # Phân tích tệp XML và tìm các trường nhập liệu theo loại
    tree = ET.parse('window_dump.xml')
    root = tree.getroot()

    field_coordinates = []
    for elem in root.iter():
        if 'class' in elem.attrib and field_type in elem.attrib['class']:
            coordinates = extract_coordinates(elem)
            if coordinates:
                field_coordinates.append(coordinates)

    return field_coordinates

def input_text_into_fields(adb_path, field_coordinates, texts):
    """Nhập văn bản vào các trường nhập liệu tại tọa độ đã cho."""
    if len(field_coordinates) != len(texts):
        print("Số lượng trường nhập liệu và văn bản không khớp.")
        return False

    for coordinates, text in zip(field_coordinates, texts):
        x, y = coordinates
        # Nhấp vào trường nhập liệu để kích hoạt bàn phím
        subprocess.run([adb_path, "shell", "input", "tap", str(x), str(y)])
        time.sleep(1)  # Chờ một chút để bàn phím xuất hiện
        # Nhập văn bản
        subprocess.run([adb_path, "shell", "input", "text", text])
        print(f"Đã nhập '{text}' vào tọa độ ({x}, {y})")

    return True