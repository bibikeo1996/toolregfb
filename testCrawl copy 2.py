from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
#96053157820b4746e3e621bba69c1c776c14ecbbe42329c70612156cfdb9b18772bf95798a1b17cdf7250a237928977dd27d7b8dd86bcbbe7931971c14e852bef5590416301ba05aae6db1fa0cefaa1e
# API proxy từ Smartproxy, với username và password
proxy = "http://U0000223196:PW_10afa0a3432e4a996252be7a6437d3a36@proxy.smartproxy.com:10000"  # Thay 'your-username' và 'your-password' bằng thông tin thật

# Cấu hình ChromeOptions với proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy}')  # Đặt proxy server cho tất cả các yêu cầu

# Cấu hình User-Agent để giả lập trình duyệt thực sự
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")

# Khởi tạo WebDriver với proxy
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Kiểm tra proxy hoạt động qua httpbin
    print("Kiểm tra IP qua proxy...")
    driver.get("http://httpbin.org/ip")
    time.sleep(3)  # Kiểm tra địa chỉ IP từ proxy
    print("Kiểm tra proxy thành công!")

    # 2. Truy cập trang đăng ký Facebook qua proxy
    print("Truy cập Facebook qua proxy...")
    driver.get("https://www.facebook.com/r.php")
    time.sleep(5)  # Chờ trang tải

    # 3. Điền thông tin vào form đăng ký
    driver.find_element(By.NAME, "firstname").send_keys("Henry")
    driver.find_element(By.NAME, "lastname").send_keys("Pham")
    driver.find_element(By.NAME, "reg_email__").send_keys("matinec102@kelenson.com")
    driver.find_element(By.NAME, "reg_passwd__").send_keys("9qwenqk@!@31")
    driver.find_element(By.XPATH, "//input[@name='sex' and @value='1']").click()  # Nam

    # 4. Chọn ngày, tháng, năm sinh
    driver.find_element(By.NAME, "birthday_day").send_keys("28")
    driver.find_element(By.NAME, "birthday_month").send_keys("10")
    driver.find_element(By.NAME, "birthday_year").send_keys("1996")

    # 5. Nhấn nút "Đăng ký"
    # driver.find_element(By.NAME, "websubmit").click()
    time.sleep(10)  # Chờ phản hồi từ Facebook

finally:
    time.sleep(3)
    driver.quit()  # Đóng trình duyệt
