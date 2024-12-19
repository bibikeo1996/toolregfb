import requests
# import json

def KiemTraProxy(adb_path, scraperapi_key):
    print(f"Đang kiểm tra kết nối với proxy( scraperapi_key:{scraperapi_key}, adb_path: {adb_path} ) từ ứng dụng di động...")
    payload = {
        'apiKey': scraperapi_key,
        'url': 'https://m.facebook.com'
    }

    # Gửi yêu cầu POST tới ScraperAPI
    response = requests.post('https://async.scraperapi.com/jobs', json=payload)

    # Kiểm tra kết quả trả về
    if response.status_code == 200:
        result = response.json()
        print("IP trả về từ ScraperAPI: ", result)
        return True
    else:
        print(f"Có lỗi xảy ra: {response.status_code} - {response.text}")