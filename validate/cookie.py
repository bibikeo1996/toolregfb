import os
import sqlite3
import subprocess

# Đường dẫn file cookie trên BlueStacks (Facebook Lite)
REMOTE_COOKIE_PATH = "/data/data/com.facebook.lite/app_webview/Cookies"
LOCAL_COOKIE_PATH = "./Cookies"

# Tên ứng dụng cần xử lý (Facebook Lite)
APP_PACKAGE = "com.facebook.lite"


def adb_command(command):
    """Hàm thực hiện lệnh adb"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Lỗi khi chạy lệnh ADB: {e}")
        return None


def connect_bluestacks():
    """Kết nối BlueStacks qua ADB"""
    print("Đang kết nối BlueStacks...")
    adb_command("adb connect 127.0.0.1:5555")
    devices = adb_command("adb devices")
    if "127.0.0.1:5555" in devices:
        print("Kết nối BlueStacks thành công!")
    else:
        print("Kết nối thất bại. Hãy kiểm tra ADB và BlueStacks.")


def pull_cookies():
    """Trích xuất file cookie từ BlueStacks"""
    print("Đang sao chép file cookie từ BlueStacks...")
    command = f"adb pull {REMOTE_COOKIE_PATH} {LOCAL_COOKIE_PATH}"
    output = adb_command(command)
    print(f"Kết quả adb pull: {output}")
    if output and "pulled" in output or os.path.exists(LOCAL_COOKIE_PATH):
        print("File cookie đã được sao chép về máy.")
    else:
        print("Không thể sao chép file cookie. Kiểm tra đường dẫn hoặc quyền truy cập.")


def read_cookies():
    """Đọc nội dung file cookie"""
    if not os.path.exists(LOCAL_COOKIE_PATH):
        print(
            "File cookie không tồn tại. Hãy chắc chắn rằng bạn đã sao chép file thành công."
        )
        return []

    print("Đang đọc nội dung cookie...")
    try:
        conn = sqlite3.connect(LOCAL_COOKIE_PATH)
        cursor = conn.cursor()

        # Kiểm tra xem các bảng có tồn tại không
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Các bảng trong cơ sở dữ liệu:", tables)

        # Kiểm tra xem bảng cookies có tồn tại không
        if not any("cookies" in table for table in tables):
            print("Bảng cookies không tồn tại trong cơ sở dữ liệu.")
            conn.close()
            return []

        # Lấy các cột liên quan đến cookie
        cursor.execute("SELECT host_key, name, value FROM cookies")
        cookies = cursor.fetchall()

        conn.close()
        return cookies
    except sqlite3.DatabaseError as e:
        print(f"Lỗi khi đọc file cookie: {e}")
        return []
    except Exception as e:
        print(f"Lỗi không xác định khi đọc cookie: {e}")
        return []


def main():
    """Chương trình chính"""
    # Kết nối BlueStacks
    connect_bluestacks()

    # Sao chép file cookie từ BlueStacks
    pull_cookies()

    # Đọc nội dung cookie
    cookies = read_cookies()

    # Hiển thị cookie liên quan đến Facebook (lọc theo host chứa 'facebook.com')
    if cookies:
        fb_cookies = [cookie for cookie in cookies if "facebook" in cookie[0]]
        print("\nCookie liên quan đến Facebook:")
        for cookie in fb_cookies:
            print(cookie)
    else:
        print("Không có cookie nào được đọc từ file.")


if __name__ == "__main__":
    main()
