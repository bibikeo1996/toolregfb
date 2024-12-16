# toolregfb

## Cài Python 

## Open command line chạy command pip install pyautogui pytest để cài thư viện

## Cài ADB https://developer.android.com/studio/releases/platform-tools

# RUN APP 

# python openApp.py => chạy app 

# python locationTest.py => Test chức năng 

# python getLocation.py => Lấy tọa độ 

## Trường hợp Port bị block thì vô 

## Window + R gõ wf.msc quyền admin

## Trong cửa sổ Windows Firewall with Advanced Security, bạn sẽ thấy Inbound Rules và Outbound Rules ở thanh bên trái.

## Chọn Inbound Rules (Quy tắc vào), sau đó  tạo một quy tắc mới. 

## Tạo quy tắc cho cổng 5037

## 1. Trong cửa sổ Windows Firewall with Advanced Security, ở bên trái, chọn Inbound Rules.
## 2. Ở bên phải, chọn New Rule....
## 3. Trong cửa sổ New Inbound Rule Wizard:
## - Chọn Port và nhấn Next.
## - Chọn TCP và nhập 5037 vào ô Specific local ports.
## - Nhấn Next.

## 4. Chọn Allow the connection và nhấn Next.
## 5. Chọn tất cả các tùy chọn mạng (Domain, Private, Public), sau đó nhấn Next.
## 6. Đặt tên cho quy tắc, ví dụ: Allow ADB Port 5037, rồi nhấn Finish.

## restart ADB - tắt mở command line

# Khởi động lại ADB server: Đôi khi ADB có thể gặp sự cố với việc kết nối, vì vậy thử khởi động lạ
# adb kill-server
# adb start-server

# Sau đó, thử kiểm tra lại các thiết bị:
# adb devices

## Show ra Emulator là đã kết nối thành công
# emulator-5554 device có thể là phiên bản BlueStacks bạn đang sử dụng, và nó đang kết nối thành công.

## check List IP 
# netstat -aon | findstr LISTENING


## Setup Command for adb
## 1. Nhấn Win + S, tìm Environment Variables hoặc gõ Edit the system environment variables, rồi bấm vào đó.
## - Trong cửa sổ System Properties, chọn tab Advanced, bấm nút Environment Variables.
## 2. Chỉnh sửa PATH:
## - Trong phần System Variables, tìm biến có tên Path và bấm Edit.
## - Bấm New và thêm đường dẫn đầy đủ đến thư mục chứa adb.exe (ví dụ: C:\platform-tools).
## 3. Lưu thay đổi:
## - Nhấn OK trong mọi cửa sổ để lưu lại.
