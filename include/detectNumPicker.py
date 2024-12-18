import os
import subprocess
import re
import random
import xml.etree.ElementTree as ET


def XacDinhToaDo(node):
    """Extract coordinates from the bounds attribute of a node."""
    if "bounds" in node.attrib:
        bounds = node.attrib["bounds"]
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return center_x, center_y
    return None, None


def ChonNgayThangNamSinh(adb_path, specific_id=None, specific_class=None):
    speed = "20"  # Default swipe speed
    try:
        # Dump UI from the device
        print(f"Đang nhập ngày tháng năm sinh...")
        dump_command = [
            adb_path,
            "shell",
            "uiautomator",
            "dump",
            "/sdcard/window_dump.xml",
        ]
        subprocess.run(dump_command, capture_output=True, text=True)

        # Pull XML file from the device to the computer
        pull_command = [
            adb_path,
            "pull",
            "/sdcard/window_dump.xml",
            "./include/window_dump.xml",
        ]
        subprocess.run(pull_command, capture_output=True, text=True)

        # Check if the dump file exists
        if not os.path.exists("./include/window_dump.xml"):
            print("Không lấy được data.")
            return []

        # Parse the XML file
        # print("Searching for interactive elements...")
        # tree = ET.parse("./include/window_dump.xml")
        tree = ET.parse("window_dump.xml")
        root = tree.getroot()

        interactive_elements = []  # List to store interactive elements

        for node in root.iter("node"):
            element_info = {}

            # Analyze element types
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
                elif node.attrib.get("resource-id") == "true":
                    element_info["type"] = "Resource Id"
                else:
                    continue  # Skip non-interactive elements

            element_info["resource-id"] = node.attrib.get("resource-id", "")

            # Extract coordinates
            coordinates = XacDinhToaDo(node)
            if coordinates:
                element_info["coordinates"] = coordinates
                if (specific_id and element_info["resource-id"] == specific_id) or (
                    specific_class and element_class == specific_class
                ):
                    x, y = coordinates
                    if (
                        specific_id
                        and element_info["resource-id"] == specific_id
                        and len(interactive_elements) == 0
                    ):
                        MONTH_LIMIT = random.randint(0, 6)
                        # print(f"Random swipe limit set to Month: {MONTH_LIMIT}")
                        month_count = 0  # Initialize swipe counter

                        while month_count < MONTH_LIMIT:
                            swipe_command = [
                                adb_path,
                                "shell",
                                "input",
                                "swipe",
                                str(x),
                                str(y),
                                str(x),
                                str(y + 100),
                                speed,
                            ]
                            subprocess.run(
                                swipe_command, capture_output=True, text=True
                            )
                            # print(f"Swiped at coordinates: {coordinates}, swipe {month_count + 1}/{MONTH_LIMIT}.")
                            month_count += 1  # Increment the swipe counter

                    if (
                        specific_id
                        and element_info["resource-id"] == specific_id
                        and len(interactive_elements) == 1
                    ):
                        DAY_LIMIT = random.randint(0, 10)
                        # print(f"Random swipe limit set to Day: {DAY_LIMIT}")
                        day_count = 0  # Initialize swipe counter

                        while day_count < DAY_LIMIT:
                            swipe_command = [
                                adb_path,
                                "shell",
                                "input",
                                "swipe",
                                str(x),
                                str(y),
                                str(x),
                                str(y + 100),
                                speed,
                            ]
                            subprocess.run(
                                swipe_command, capture_output=True, text=True
                            )
                            # print(f"Swiped at coordinates: {coordinates}, swipe {day_count + 1}/{DAY_LIMIT}.")
                            day_count += 1  # Increment the swipe counter

                    if (
                        specific_id
                        and element_info["resource-id"] == specific_id
                        and len(interactive_elements) == 2
                    ):
                        YEAR_LIMIT = random.randint(10, 15)
                        # print(f"Random swipe limit set to Year: {YEAR_LIMIT}")
                        year_count = 0  # Initialize swipe counter

                        while year_count < YEAR_LIMIT:
                            swipe_command = [
                                adb_path,
                                "shell",
                                "input",
                                "swipe",
                                str(x),
                                str(y),
                                str(x),
                                str(y + 100),
                                speed,
                            ]
                            subprocess.run(
                                swipe_command, capture_output=True, text=True
                            )
                            # print(f"Swiped at coordinates: {coordinates}, swipe {year_count + 1}/{YEAR_LIMIT}.")
                            year_count += 1  # Increment the swipe counter

                    # Append the element information after processing
                    interactive_elements.append(element_info)

        return interactive_elements

    except Exception as e:
        print(f"Error: {e}")
        return []
