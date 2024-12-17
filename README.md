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
Run index.py
```sh
python index.py
```

Run test thì vào folder Test rồi run 
```sh
python locationTest.py => Test chức năng 
python getLocation.py => Lấy tọa độ 
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