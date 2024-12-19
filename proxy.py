import os
from dotenv import load_dotenv
#from include.isAppRunning import is_bluestacks_running, is_app_installed

from validate.proxy import KiemTraProxy
from app import OpenToolRegFaceBook
from include.isAppRunning import isBlueStackRunning
from include.deleteApp import xoa_app
import include.defined as defined

# Load biến môi trường từ tệp .env nếu có
load_dotenv()

adb_path = os.getenv('ADB_PATH')
scraperapi_key = os.getenv('SCRAPERAPI_KEY')
proxy_host = os.getenv('PROXY_HOST')
proxy_port = os.getenv('PROXY_PORT')

KiemTraProxy(adb_path, scraperapi_key, proxy_host, proxy_port)
