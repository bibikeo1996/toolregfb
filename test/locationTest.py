import os
import subprocess
import re
import random
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

def extract_element_info(node):
    # Extract information from an XML ElementTree.Element
    element_info = {
        "resource-id": node.attrib.get("resource-id", ""),  # Access an attribute safely
        "text": node.text.strip() if node.text else "",  # Safely retrieve text content
        "coordinates": XacDinhToaDo(node)  # Call your existing function to get coordinates
    }
    return element_info

def get_all_interactive_elements(specific_id=None, specific_class=None):
    adb_path = r"C:\Users\patroids115\Desktop\platform-tools-latest-windows\platform-tools\adb.exe"  # Đường dẫn tới adb.exe
    speed = "50"  # Tốc độ swipe mặc định
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
                if (specific_id and element_info["resource-id"] == specific_id) or (specific_class and element_class == specific_class):

                    if specific_id and element_info["resource-id"] == specific_id and len(interactive_elements) == 0:
                        x, y = coordinates
                        MONTH_LIMIT = random.randint(0, 12)
                        print(f"Random swipe limit set to Month: {MONTH_LIMIT}")
                        month_count = 0  # Initialize swipe counter
                        
                        while month_count < MONTH_LIMIT:
                            swipe_command = [
                                adb_path, "shell", "input", "swipe",
                                str(x), str(y), str(x), str(y + 100), speed
                            ]
                            subprocess.run(swipe_command, capture_output=True, text=True)
                            print(f"Swiped at coordinates: {coordinates}, swipe {month_count + 1}/{MONTH_LIMIT}.")
                            month_count += 1  # Increment the swipe counter
                        else:
                            print(f"Swipe limit of {MONTH_LIMIT} reached.")

                    if specific_id and element_info["resource-id"] == specific_id and len(interactive_elements) == 1:
                        x, y = coordinates
                        DAY_LIMIT = random.randint(0, 31)
                        print(f"Random swipe limit set to Day: {DAY_LIMIT}")
                        day_count = 0  # Initialize swipe counter
                        
                        while day_count < DAY_LIMIT:
                            swipe_command = [
                                adb_path, "shell", "input", "swipe",
                                str(x), str(y), str(x), str(y + 100), speed
                            ]
                            subprocess.run(swipe_command, capture_output=True, text=True)
                            print(f"Swiped at coordinates: {coordinates}, swipe {day_count + 1}/{DAY_LIMIT}.")
                            day_count += 1  # Increment the swipe counter
                        else:
                            print(f"Swipe limit of {DAY_LIMIT} reached.")

                    if specific_id and element_info["resource-id"] == specific_id and len(interactive_elements) == 2:
                        x, y = coordinates
                        YEAR_LIMIT = random.randint(15, 31)
                        print(f"Random swipe limit set to Year: {YEAR_LIMIT}")
                        year_count = 0  # Initialize swipe counter
                        
                        while year_count < YEAR_LIMIT:
                            swipe_command = [
                                adb_path, "shell", "input", "swipe",
                                str(x), str(y), str(x), str(y + 100), speed
                            ]
                            subprocess.run(swipe_command, capture_output=True, text=True)
                            print(f"Swiped at coordinates: {coordinates}, swipe {year_count + 1}/{YEAR_LIMIT}.")
                            year_count += 1  # Increment the swipe counter
                        else:
                            print(f"Swipe limit of {YEAR_LIMIT} reached.")

                    # Append the element information after processing
                    interactive_elements.append(element_info)


        return interactive_elements

    except Exception as e:
        print(f"Lỗi: {e}")
        return []

# Gọi hàm với specific_id hoặc specific_class
interactive_elements = get_all_interactive_elements(specific_id="android:id/numberpicker_input")
