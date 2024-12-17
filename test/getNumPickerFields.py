import os
import subprocess
import time
import requests
from include.detectNumPicker import swipe_all_fields
from dotenv import load_dotenv

# Load biến môi trường từ tệp .env nếu có
load_dotenv()

bluestacks_path = os.getenv('BLUESTACKS_PATH')
adb_path = os.getenv('ADB_PATH')
package_name = os.getenv('PACKAGE_NAME')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')
apk_path = os.getenv('APK_PATH')

# Chọn giá trị cho NumberPicker
resource_id = "android:id/numberpicker_input"  # Replace with actual resource ID
target_values = ["Jul", "17", "1996"]  # Target values: Month, Day, Year
swipe_coords_list = [
    ((100, 1000), (100, 800)),  # Month picker swipe coordinates
    ((300, 1000), (300, 800)),  # Day picker swipe coordinates
    ((500, 1000), (500, 800)),  # Year picker swipe coordinates
]

swipe_all_fields(adb_path, resource_id, target_values, swipe_coords_list)