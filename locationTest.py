import subprocess
import time

adb_path = r"C:\Users\patroids115\Desktop\platform-tools-latest-windows\platform-tools\adb.exe"   # Thay thế bằng đường dẫn thực tế đến adb

coordinates = {
    1: (150, 1285),
    2: (450, 1285),
    3: (750, 1285),
    4: (150, 1375),
    5: (450, 1375),
    6: (750, 1375),
    7: (150, 1465),
    8: (450, 1465),
    9: (750, 1465),
    0: (450, 1555)
}
date_string = "15/10/1996"

# Tap vào button Login (thay tọa độ thực tế)
# click tạo tại khoản
# subprocess.run([adb_path, "shell", "input", "tap", "450", "551"])
# time.sleep(1)
# #Click tip
# subprocess.run([adb_path, "shell", "input", "tap", "450", "551"])
# time.sleep(1)
# # nhập tên và họ 
# subprocess.run([adb_path, "shell", "input", "tap", "232", "319"])
# subprocess.run([adb_path, "shell", "input", "text", "John"])
# time.sleep(1)
# subprocess.run([adb_path, "shell", "input", "tap", "667", "319"])
# subprocess.run([adb_path, "shell", "input", "text", "Pham"])
# time.sleep(1)
# #  click tiếp 
# subprocess.run([adb_path, "shell", "input", "tap", "450", "388"])
# # Chọn email 
# subprocess.run([adb_path, "shell", "input", "tap", "450", "475"])
# click tiếp sau khi nhập email
#subprocess.run([adb_path, "shell", "input", "tap", "450", "376"])


# # Nhập ngày sinh theo định dạng dd/mm/yyyy
# tap_commands = []
# for char in date_string:
#     if char.isdigit():  # Kiểm tra nếu ký tự là số
#         num = int(char)
#         if num in coordinates:  # Kiểm tra tọa độ hợp lệ
#             x, y = coordinates[num]
#             tap_commands.append([adb_path, "shell", "input", "tap", str(x), str(y)])

# for command in tap_commands:
#     subprocess.run(command)
#     print(f"Tapped at {command[4]}, {command[5]}")

#click tiếp sau khi chọn ngày sinh 
#subprocess.run([adb_path, "shell", "input", "tap", "450", "416"]) 

#chọn giới tính 
#subprocess.run([adb_path, "shell", "input", "tap", "450", "382"]) 

#subprocess.run([adb_path, "shell", "input", "tap", "449", "327"])
#subprocess.run([adb_path, "shell", "input", "text", "John@123"])
#time.sleep(1)
#click tiếp sau khi nhập mật khẩu
#subprocess.run([adb_path, "shell", "input", "tap", "450", "396"])

# chọn ngày tháng năm sinh
# subprocess.run([adb_path, "shell", "input", "swipe", "116", "826", "116", "926", "300"])
# time.sleep(1)
# subprocess.run([adb_path, "shell", "input", "swipe", "236", "826", "236", "926", "300"])
# time.sleep(1)
# subprocess.run([adb_path, "shell", "input", "swipe", "356", "826", "356", "2826", "300"])
# time.sleep(1)
# subprocess.run([adb_path, "shell", "input", "tap", "656", "1078"])
# time.sleep(1)

# click tiếp
# subprocess.run([adb_path, "shell", "input", "tap", "450", "418"])

time.sleep(10)
subprocess.run([adb_path, "shell", "input", "tap", "574", "857"])

