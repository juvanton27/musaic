import platform
import os
import time

from dotenv import load_dotenv
from selenium.webdriver import Chrome, ChromeOptions

load_dotenv()
options = ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--enable-logging")
options.add_argument("--v=1")
options.add_argument(f"user-data-dir={os.getenv('USER_DATA_DIR')}")
chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
os.environ["PATH"] += os.pathsep + chromedriver_path

bot = Chrome(options)
try:
  bot.get("https://studio.youtube.com")
  print('Wainting 1 minute to let user logging in')
  time.sleep(60)
  bot.quit()
except:
  print('Error while logging in')
  bot.quit()