import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Path to the Excel file
file_path = r"D:\toolregfb\data\emails.xlsx"
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
url = "https://www.minuteinbox.com/"

def getDataInFileEmails(index):
    df = pd.read_excel(file_path)
    mi_values = df["MI"].tolist()[index]
    phpsessid_values = df["PHPSESSID"].tolist()[index]
    return {
        "mi": mi_values,
        "phpsessid": phpsessid_values
    }

def getMailCode(mi_value, phpsessid_value):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.add_cookie({"name": "MI", "value": mi_value})
        driver.add_cookie({"name": "PHPSESSID", "value": phpsessid_value})
        driver.refresh()
        #get mail code
        confirmation_code_element = driver.find_element(By.CLASS_NAME, "predmet")
        confirmation_code_text = confirmation_code_element.text
        confirmation_code = confirmation_code_text.split(" ")[0]
        return confirmation_code

        
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
    finally:
        # input("Nhấn Enter để đóng trình duyệt...")
        driver.quit()
def main():
    data = getDataInFileEmails(1)
    mi = data["mi"]
    phpsessid = data["phpsessid"]
    print("MI values:", mi)
    print("PHPSESSID values:", phpsessid)
    code = getMailCode(mi, phpsessid)
    print("Code:", code)

main()