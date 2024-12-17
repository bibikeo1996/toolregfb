import subprocess

def KiemTraProxy(adb_path):
    print("Đang kiểm tra kết nối proxy từ ứng dụng di động...")
    check_proxy_command = [adb_path, "shell", "curl", "http://httpbin.org/ip"]
    result = subprocess.run(check_proxy_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"IP trả về từ proxy: {result.stdout}")
    else:
        print(f"Lỗi khi kiểm tra proxy: {result.stderr}")