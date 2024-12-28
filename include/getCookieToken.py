import subprocess
import re
import json

def getUID(cookie):
    match = re.search(r'c_user=(\d+)', cookie)
    return match.group(1) if match else None

# def KiemTraAdb_ROOT(adb_port):
#     command = ['adb', '-s', f'127.0.0.1:{adb_port}', 'root']
#     try:
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         if "adbd is already running as root" in result.stdout:
#             return "ADB is running as root."
#         elif "permission denied" in result.stderr:
#             return "Permission denied. ADB root access not available."
#         else:
#             return "Unexpected output: " + result.stdout + result.stderr
#     except subprocess.CalledProcessError as e:
#         return f"Command failed: {e}"

# def ChayAdbCommand(command, adb_port):
#     adb_command = ['adb', '-s', f'127.0.0.1:{adb_port}', 'shell'] + command.split()
#     try:
#         result = subprocess.run(adb_command, capture_output=True, text=True, check=True)
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         return f"Command failed: {e}"

# def KeofileTuRootVeLocal(adb_port):
#     command = "cp /data/data/com.facebook.lite/files/PropertiesStore_v02 /sdcard/"
#     ChayAdbCommand(command, adb_port)
#     pull_command = ['adb', '-s', f'127.0.0.1:{adb_port}', 'pull', '/sdcard/PropertiesStore_v02', f'./authorFiles/PropertiesStore_v02_{adb_port}']
#     try:
#         subprocess.run(pull_command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Command failed: {e}")
#     delete_command = "rm /sdcard/PropertiesStore_v02"
#     ChayAdbCommand(delete_command, adb_port)

def KiemTraAdb_ROOT(index):
    command = ['ldconsole.exe', 'adb', '--index', f'{index}', '--command', 'root']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result)
        if "adbd is already running as root" in result.stdout:
            return "ADB is running as root."
        elif "permission denied" in result.stderr:
            return "Permission denied. ADB root access not available."
        else:
            return "Unexpected output: " + result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e}"

def ChayAdbCommand(command, index):
    adb_command = ['ldconsole.exe', 'adb', '--index', f'{index}', '--command'] + command.split()
    try:
        result = subprocess.run(adb_command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e}"

def KeofileTuRootVeLocal(index):
    command = "cp /data/data/com.facebook.lite/files/PropertiesStore_v02 /sdcard/"
    ChayAdbCommand(command, index)
    pull_command = ['ldconsole.exe', 'adb', '--index', f'{index}', '--command', 'pull', '/sdcard/PropertiesStore_v02', f'./authorFiles/PropertiesStore_v02_{index}']
    try:
        subprocess.run(pull_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
    delete_command = "rm /sdcard/PropertiesStore_v02"
    ChayAdbCommand(delete_command, index)

def getCookie(index):
    local_file_path = f'./authorFiles/PropertiesStore_v02_{index}'
    try:
        with open(local_file_path, 'r', encoding='latin-1') as file:
            data = file.read()
            json_array_data = re.search(r'\[.*\]', data)
            if json_array_data:
                json_array_string = json_array_data.group(0)
                cookies = json.loads(json_array_string)
                return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def getToken(index):
    local_file_path = f'./authorFiles/PropertiesStore_v02_{index}'
    try:
        with open(local_file_path, 'r', encoding='latin-1') as file:
            data = file.read()
            access_token_match = re.search(r'"access_token":"(.*?)"', data)
            return access_token_match.group(1) if access_token_match else None
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    adb_ports = [5555]  # Add your adb_ports here
    for adb_port in adb_ports:
        print(f"Running on adb_port {adb_port}")
        KiemTraAdb_ROOT(adb_port)
        KeofileTuRootVeLocal(adb_port)
        cookie = getCookie(adb_port)
        token = getToken(adb_port)
        c_user = getUID(cookie)
        print(f"Cookie for adb_port {adb_port}: {cookie}")
        print(f"Token for adb_port {adb_port}: {token}")
        print(f"Uid for adb_port {adb_port}: {c_user}")