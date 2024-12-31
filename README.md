# Tool Reg Facebook

Cài Python 

Cài thư viện
Mở command line và chạy các lệnh sau để cài đặt các thư viện cần thiết:

For Code
```sh
pip install pyautogui pytest python-dotenv requests
```
For Test
```sh
pip install setuptools
```

Cài đặt ADB
Tải và cài đặt ADB từ đây
```sh
https://developer.android.com/studio/releases/platform-tools
```
Mã nguồn này chạy qua Adb của ldconsole.exe
Các comment Adb ldconsole.exe thông dụng
```sh
launch <--name mnq_name | --index mnq_idx>

reboot <--name mnq_name | --index mnq_idx>

installapp <--name mnq_name | --index mnq_idx> --filename <apk_file_name>

installapp <--name mnq_name | --index mnq_idx> --packagename <apk_package_name>

uninstallapp <--name mnq_name | --index mnq_idx> --packagename <apk_package_name>

runapp <--name mnq_name | --index mnq_idx> --packagename <apk_package_name>

killapp <--name mnq_name | --index mnq_idx> --packagename <apk_package_name>

list

list2

list3 [--index <mnq_idx>]

```
# Lưu ý phải thêm ldconsole.exe phía trước 
```sh
ldconsole.exe launch <--name mnq_name | --index mnq_idx>
```


Run index.py
```sh
python index.py
```

# Trường hợp Port bị block
1. Nhấn Windows + R, gõ wf.msc và chạy với quyền admin.
2. Trong cửa sổ Windows Firewall with Advanced Security, chọn Inbound Rules ở thanh bên trái.
3. Tạo một quy tắc mới cho cổng 5037:
- Chọn Inbound Rules, sau đó chọn New Rule....
- Trong cửa sổ New Inbound Rule Wizard:
  - Chọn Port và nhấn Next.
  - Chọn TCP và nhập 5037 vào ô Specific local ports.
  - Nhấn Next.
- Chọn Allow the connection và nhấn Next.
- Chọn tất cả các tùy chọn mạng (Domain, Private, Public), sau đó nhấn Next.
- Đặt tên cho quy tắc, ví dụ: Allow ADB Port 5037, rồi nhấn Finish.

# Khởi động lại ADB server
```sh
adb kill-server
adb start-server
```
Sau đó, thử kiểm tra lại các thiết bị:
```sh
adb devices
```
Lưu ý:
```sh
Nếu hiển thị emulator-5554 device có nghĩa là BlueStacks đã kết nối thành công.
Nếu hiển thị emulator-5556 device có nghĩa là BlueStacks đã kết nối thành công.
Nếu hiển thị emulator-5558 device có nghĩa là BlueStacks đã kết nối thành công.
```
Nếu không hiển thị như trên thì hãy kiểm tra Thông số kỹ thuật của thiết bị LDplayer nếu bị trùng nó sẽ không hiện
```sh
Mở LDMultiPlayer => chọn setting => check Model tab
```
# Các lệnh ldconsole.exe
```sh
{ld_path_console} adb --index {index} --command "shell input keyevent {keycode}"
{ld_path_console} adb --index {index} --command "shell pm grant {com.facebook.lite} {android.permission.READ_CONTACTS}"
{ld_path_console} adb --index {index} --command root
{ld_path_console} adb --index {index} --command shell
{ld_path_console} adb --index {index} --command su
{ld_path_console} launch --index {index}
etc
```

# Các lệnh Adb
```sh
adb connect 127.0.0.1:{port LD cần check}

adb -s 127.0.0.1:{port LD cần check} root  => chạy 2 lần để xác định đã root hay chưa

adb -s 127.0.0.1:5555 shell => để vô shell

adb -s 127.0.0.1:5555 su => để truy cập với quyền superadmin

cd /data/data/com.facebook.lite/filesPropertiesStore_v02 => file cookie của facebook
```


Kiểm tra danh sách IP

```sh
netstat -aon | findstr LISTENING
```

# Thiết lập biến môi trường cho ADB

1. Nhấn Win + S, tìm Environment Variables hoặc gõ Edit the system environment variables, rồi bấm vào đó.
2. Trong cửa sổ System Properties, chọn tab Advanced, bấm nút Environment Variables.
3. Chỉnh sửa PATH:
- Trong phần System Variables, tìm biến có tên Path và bấm Edit.
- Bấm New và thêm đường dẫn đầy đủ đến thư mục chứa adb.exe (ví dụ: C:\platform-tools).
4. Lưu thay đổi:
- Nhấn OK trong mọi cửa sổ để lưu lại.

- pip install opencv-python
- pip install opencv-python-headless
- pip install adb-shell
- pip install adbutils
- pip install mss
- pip install psutil
- pip install tabulate
- pip install selenium
- pip install webdriver-manager
- pip install pandas
- pip install openpyxl
