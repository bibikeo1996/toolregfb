from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Cấu hình proxy (không cần username và password nữa)
proxy = 'vn.smartproxy.com:46000'

# Tạo Chrome options để thêm proxy và user-agent
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server=https://{proxy}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Ẩn Selenium automation
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")  # User-Agent

# Tạo trình duyệt với proxy
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Truy cập vào httpbin.org/ip để kiểm tra proxy IP
print("Truy cập vào httpbin.org/ip để kiểm tra IP proxy...")
driver.get("https://httpbin.org/ip")
time.sleep(3)  # Đợi trang tải

# Lấy địa chỉ IP và in ra
proxy_ip = driver.find_element(By.TAG_NAME, "pre").text
print(f"Proxy IP đang sử dụng: {proxy_ip}")

# 2. Truy cập trang đăng ký Facebook qua proxy
print("Truy cập Facebook qua proxy...")
driver.get("https://www.facebook.com/r.php")
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên

# 3. Điền thông tin vào form đăng ký
driver.find_element(By.NAME, "firstname").send_keys("Chirstan")
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.NAME, "lastname").send_keys("Lee")
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.NAME, "reg_email__").send_keys("serverfilm3@gmail.com")
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.NAME, "reg_passwd__").send_keys("lF94SaQqusv9ZXZ")
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.XPATH, "//input[@name='sex' and @value='2']").click()  # Nam
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên

# Chọn ngày, tháng, năm sinh với giá trị ngẫu nhiên
birthday_day = random.randint(1, 28)  # Ngày có thể từ 1 đến 28 để tránh lỗi
birthday_month = random.randint(1, 12)  # Tháng từ 1 đến 12
birthday_year = random.randint(1990, 2004)  # Năm từ 1990 đến 2004

driver.find_element(By.NAME, "birthday_day").send_keys(str(birthday_day))
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.NAME, "birthday_month").send_keys(str(birthday_month))
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên
driver.find_element(By.NAME, "birthday_year").send_keys(str(birthday_year))
time.sleep(random.uniform(5, 10))  # Delay ngẫu nhiên

# 5. Nhấn nút "Đăng ký"
driver.find_element(By.NAME, "websubmit").click()
time.sleep(random.uniform(3, 6))  # Delay ngẫu nhiên

time.sleep(3600)
# Đóng trình duyệt
driver.quit()
