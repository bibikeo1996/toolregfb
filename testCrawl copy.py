from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# API proxy từ ScraperAPI
proxy = "http://api.scraperapi.com?api_key=ef1401855702dc5c5d36849de0c39909&url="

# Cấu hình ChromeOptions với proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy}')  # Đặt proxy server cho tất cả các yêu cầu

# Khởi tạo WebDriver với proxy
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Kiểm tra proxy hoạt động qua httpbin
    print("Kiểm tra IP qua proxy...")
    driver.get("http://httpbin.org/ip")
    time.sleep(10)
    print("Kiểm tra proxy thành công!")

    # 2. Truy cập trang đăng ký Facebook qua proxy
    print("Truy cập Facebook qua proxy...")
    driver.get("https://www.facebook.com/r.php")
    time.sleep(3)  # Chờ trang tải

    # 3. Điền thông tin vào form đăng ký
    driver.find_element(By.NAME, "firstname").send_keys("Joe")
    driver.find_element(By.NAME, "lastname").send_keys("Cao")
    driver.find_element(By.NAME, "reg_email__").send_keys("rodel54174@rabitex.com")
    driver.find_element(By.NAME, "reg_passwd__").send_keys("alululi")
    driver.find_element(By.XPATH, "//input[@name='sex' and @value='1']").click()  # Nam

    # 4. Chọn ngày, tháng, năm sinh
    driver.find_element(By.NAME, "birthday_day").send_keys("28")
    driver.find_element(By.NAME, "birthday_month").send_keys("10")
    driver.find_element(By.NAME, "birthday_year").send_keys("1995")

    # 5. Nhấn nút "Đăng ký"
    driver.find_element(By.NAME, "websubmit").click()
    time.sleep(60)  # Chờ phản hồi từ Facebook

finally:
    time.sleep(3600)
    # driver.quit()  # Đóng trình duyệt
