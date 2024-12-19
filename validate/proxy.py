import requests
import subprocess
import time

def set_proxy_bluestacks(adb_path, proxy_host, proxy_port):
    """
    Thiết lập proxy cho BlueStacks thông qua ADB.
    """
    print(f"Đang cấu hình proxy cho BlueStacks với {proxy_host}:{proxy_port}")
    set_proxy_command = f"{adb_path} shell settings put global http_proxy {proxy_host}:{proxy_port}"
    subprocess.run(set_proxy_command, shell=True, check=True)
    print(f"Đã cấu hình proxy: {proxy_host}:{proxy_port}")

def get_current_ip(scraperapi_key):
    """
    Lấy IP hiện tại qua ScraperAPI Proxy.
    """
    proxy = {
        'http': f'http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001',
        'https': f'http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001'
    }

    url = 'http://httpbin.org/ip'

    try:
        # Gửi yêu cầu thông qua ScraperAPI proxy
        response = requests.get(url, proxies=proxy, verify=False)  # verify=False bỏ qua SSL certificate (nếu cần)
        response.raise_for_status()  # Kiểm tra nếu có lỗi từ yêu cầu

        # Trả về IP
        ip = response.json().get('origin')
        return ip
    except requests.RequestException as e:
        print(f"Lỗi khi gửi yêu cầu: {e}")
        return None

def KiemTraProxy(adb_path, scraperapi_key, proxy_host, proxy_port):
    print(f"Đang kiểm tra và thay đổi proxy (adb_path: {adb_path})...")

    while True:
        try:
            # Set proxy on BlueStacks
            set_proxy_bluestacks(adb_path, proxy_host, proxy_port)

            # Show current IP before setting proxy
            print("Đang lấy IP trước khi thay đổi proxy...")
            current_ip = get_current_ip(scraperapi_key)
            print(f"IP trước khi thay đổi proxy: {current_ip}")

            # Show new IP after setting proxy
            print("Đang lấy IP sau khi thay đổi proxy...")
            new_ip = get_current_ip(scraperapi_key)
            print(f"IP sau khi thay đổi proxy: {new_ip}")
            
            # Chờ một khoảng thời gian trước khi kiểm tra lại (giúp tránh việc gửi quá nhiều yêu cầu quá nhanh)
            time.sleep(120)  # 10 giây, bạn có thể điều chỉnh theo nhu cầu

        except KeyboardInterrupt:
            print("Đã dừng kiểm tra proxy!")
            break
