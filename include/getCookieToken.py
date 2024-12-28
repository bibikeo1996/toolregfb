import subprocess
import re
import json

def getUID(cookie):
    match = re.search(r'c_user=(\d+)', cookie)
    return match.group(1) if match else None

# ldconsole.exe adb --index 0 --command "shell su -c 'ls /data/data/com.facebook.lite/files/'"
# pull file ldconsole.exe adb --index 0 --command "shell su -c 'cp /data/data/com.facebook.lite/files/PropertiesStore_v02 /sdcard/'"


def getAdbData(index):
    result_data = {
        "uid": None,
        "cookie": None,
        "token": None
    }

    def XuLyAdbCommand(index):
        # print(f"Starting XuLyAdbCommand with index: {index}")

        # Kiểm tra ADB root
        command = ['ldconsole.exe', 'adb', '--index', f'{index}', '--command', 'root']
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            if "adbd is already running as root" in result.stdout:
                # print("ADB is running as root.")
                pass
            elif "permission denied" in result.stderr:
                print("Permission denied. ADB root access not available.")
                return None
            else:
                print("Unexpected output: " + result.stdout + result.stderr)
                return None
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return None

        # Lệnh 1: Copy file từ root vào SD card
        adb_command = f"ldconsole.exe adb --index {index} --command \"shell su -c 'cp /data/data/com.facebook.lite/files/PropertiesStore_v02 /sdcard/'\""
        try:
            result = subprocess.run(adb_command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            return None

        # Lệnh 2: Pull file từ SD card về local
        pull_command = [
            'ldconsole.exe', 
            'adb', 
            '--index', str(index), 
            '--command', 
            f'pull /sdcard/PropertiesStore_v02 include/authorFiles/PropertiesStore_v02_{index}'
        ]

        try:
            subprocess.run(['adb', 'devices'])
            result = subprocess.run(pull_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            return None

        #Lệnh 3: Xóa file từ SD card
        delete_command = "rm /sdcard/PropertiesStore_v02"
        adb_delete_command = ['ldconsole.exe', 'adb', '--index', f'{index}', '--command', "shell", "su", "-c"] + delete_command.split()
        try:
            subprocess.run(adb_delete_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Delete command failed: {e}")
            return None

        return "All commands executed successfully."

    def getCookie(index):
        local_file_path = f'include/authorFiles/PropertiesStore_v02_{index}'
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

        return None, None

    def getToken(index):
        local_file_path = f'include/authorFiles/PropertiesStore_v02_{index}'
        try:
            with open(local_file_path, 'r', encoding='latin-1') as file:
                data = file.read()
                access_token_match = re.search(r'"access_token":"(.*?)"', data)
                return access_token_match.group(1) if access_token_match else None
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Execute the commands
    XuLyAdbCommand(index)
    result_data = {
        "uid": getUID(getCookie(index)),
        "cookie": getCookie(index),
        "token":  getToken(index)
    }
    return json.dumps(result_data)

    
# if __name__ == "__main__":
#     print(f"Running on adb_port {0}")
#     print(getAdbData(0))