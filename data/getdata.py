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

def openBrave():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        # Tìm thẻ a có title="1 month" và click vào nó
        one_month_link = driver.find_element(By.XPATH, '//a[@title="1 month"]')
        one_month_link.click()
        time.sleep(5)
        email_element = driver.find_element(By.ID, "email")
        email_text = email_element.text
        local_part = email_text.split("@")[0]
        firstName, lastName = local_part.split(".")
        # Lấy cookie MI
        mi_cookie = driver.get_cookie("MI")
        mi_value = mi_cookie["value"] if mi_cookie else "Không tìm thấy cookie MI"

        # Lấy cookie PHPSESSID
        phpsessid_cookie = driver.get_cookie("PHPSESSID")
        phpsessid_value = phpsessid_cookie["value"] if phpsessid_cookie else "Không tìm thấy cookie PHPSESSID"
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
    finally:
        driver.quit()
        return {
            "email": email_text,
            "passWord": firstName + '.' + lastName + '123456',
            "firstName": firstName,
            "lastName": lastName,
            "mi": mi_value,
            "phpsessid": phpsessid_value
        }

def open_excel_file(file_path):
  try:
    df = pd.read_excel(file_path)
    return df
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

def input_data(file_path, email, passWord, firstName, lastName, mi, phpsessid):
  data = open_excel_file(file_path)
  if data is not None:
    print(data.head())
    # Create a new DataFrame with the specified columns
    if 'Email' not in data.columns:
      new_data = pd.DataFrame(columns=['Email', 'Pass Word', 'FirstName', 'LastName', 'MI', 'PHPSESSID'])
    else:
      new_data = data
    
    # Append the new data to the DataFrame
    new_row = pd.DataFrame({
      'Email': [email],
      'Pass Word': [passWord],
      'FirstName': [firstName],
      'LastName': [lastName],
      'MI': [mi],
      'PHPSESSID': [phpsessid]
    })
    new_data = pd.concat([new_data, new_row], ignore_index=True)

    # Save the new DataFrame to the Excel file
    new_data.to_excel(file_path, index=False)
    # main()
  else:
    print("Failed to load data from the Excel file.")

def main():
  data = openBrave()
  print(data)
  email = data['email']
  passWord = data['passWord']
  firstName = data['firstName']
  lastName = data['lastName']
  mi = data['mi']
  phpsessid = data['phpsessid']

  input_data(file_path, email, passWord, firstName, lastName, mi, phpsessid)

main()