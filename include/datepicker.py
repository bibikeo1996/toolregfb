import os
import xml.etree.ElementTree as ET
import re
import time
import random
import subprocess  # Thêm import cho subprocess


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

def XuatToaDo(file_path, resource_id):
    """Extract coordinates for all nodes with the specified resource-id."""
    try:
        print(f"Parsing XML file at {file_path}")
        tree = ET.parse(file_path)
        root = tree.getroot()

        coordinates_list = []

        for node in root.iter("node"):
            if (
                "resource-id" in node.attrib
                and node.attrib["resource-id"] == resource_id
            ):
                coordinates = XacDinhToaDo(node)
                if coordinates != (None, None):
                    coordinates_list.append(coordinates)

        return coordinates_list

    except FileNotFoundError:
        print(f"XML file not found: {file_path}")
        return []
    except ET.ParseError as pe:
        print(f"Error parsing XML file: {pe}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def VuotChon(index, ld_path_console, x, y, direction="up", duration=20, times=1):
    for _ in range(times):
        if direction == "up":
            x_end, y_end = x, y - random.randint(100, 200)
        elif direction == "down":
            x_end, y_end = x, y + random.randint(100, 200)
        else:
            raise ValueError("Direction must be 'up' or 'down'")

        command = f'{ld_path_console} adb --index {index} --command "shell input swipe {x} {y} {x_end} {y_end} {duration}"'
        # print(f"Executing command: {command}")
        os.system(command)

def ChonNgayThangNamSinh(index, ld_path_console):
    # Dump UI map first
    DumpMap(ld_path_console)

    # Then proceed with extracting coordinates
    file_path = "./include/map/datePickerLocation.xml"
    resource_id = "android:id/numberpicker_input"

    result = XuatToaDo(file_path, resource_id)
    coordinates = {f"col {i+1}": coord for i, coord in enumerate(result)}

    config = {
        "col 1": {
            "direction": "down",
            "min_swipes": 1,
            "max_swipes": 12,
            "min_delay": 1,
            "max_delay": 1,
        },
        "col 2": {
            "direction": "down",
            "min_swipes": 1,
            "max_swipes": 30,
            "min_delay": 0,
            "max_delay": 1,
        },
        "col 3": {
            "direction": "up",
            "min_swipes": 15,
            "max_swipes": 25,
            "min_delay": 1,
            "max_delay": 1,
        },
    }

    selected_date = {}

    for name, coord in coordinates.items():
        if name in config:
            x, y = coord
            col_config = config[name]
            direction = col_config["direction"]
            min_swipes = col_config["min_swipes"]
            max_swipes = col_config["max_swipes"]
            min_delay = col_config["min_delay"]
            max_delay = col_config["max_delay"]

            times = random.randint(min_swipes, max_swipes)
            delay = random.uniform(min_delay, max_delay)

            # Perform the swipe action
            VuotChon(index, ld_path_console, x, y, direction=direction, times=times)
            time.sleep(delay)

            # Capture the selected value (this part is hypothetical and depends on your implementation)
            selected_value = LayGiaTriDaChon(ld_path_console, x, y)
            selected_date[name] = selected_value

    return selected_date

def LayGiaTriDaChon(ld_path_console, x, y):
    # This function should implement the logic to capture the selected value from the date picker
    # For example, it could use OCR or another method to read the value at the given coordinates
    pass

def DumpMap(ld_path_console, dump_file_path="include/map/datePickerLocation.xml"):
    try:
        # print(f"Creating directories for {dump_file_path}")
        os.makedirs(os.path.dirname(dump_file_path), exist_ok=True)
        dump_command = f'{ld_path_console} adb --index 0 --command "shell uiautomator dump"'
        # print(dump_command)
        result = subprocess.run(dump_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            print(f"Error while dumping UI: {result.stderr}")
            return False
        pull_command = f'{ld_path_console} adb --index 0 --command "pull /sdcard/window_dump.xml {dump_file_path}"'
        # print(pull_command)
        pull_result = subprocess.run(pull_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if pull_result.returncode != 0:
            print(f"Error while pulling XML file: {pull_result.stderr}")
            return False

        # print(f"File XML has been successfully dumped and pulled to: {dump_file_path}")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False



# def XuatToaDo(file_path, resource_id):
#     """Extract coordinates for all nodes with the specified resource-id."""
#     tree = ET.parse(file_path)
#     root = tree.getroot()

#     coordinates_list = []

#     for node in root.iter("node"):
#         if "resource-id" in node.attrib and node.attrib["resource-id"] == resource_id:
#             coordinates = XacDinhToaDo(node)
#             if coordinates != (None, None):
#                 coordinates_list.append(coordinates)

#     return coordinates_list

# if __name__ == "__main__":
#     DumpMap(0)
