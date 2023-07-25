import os
import time
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_bot() -> webdriver.Chrome:
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument(
    f"user-data-dir={os.getenv('USER_DATA_DIR')}"
  )
  if platform.system() == 'Darwin':
    options.binary_location = os.getenv('BINARY_LOCATION')

  chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
  os.environ["PATH"] += os.pathsep + chromedriver_path

  # return webdriver.Chrome(options) if platform.system() == 'Darwin' else webdriver.Chrome() if platform.system() == 'Linux' else webdriver.Chrome()
  return webdriver.Chrome(options)

def upload_video(bot: webdriver.Chrome, video_path: str, title: str):
  bot.get("https://studio.youtube.com")

  upload_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="upload-icon"]'))
  )
  upload_button.click()

  time.sleep(2)
  abs_path = os.path.abspath(video_path)
  print(abs_path)
  bot.find_element(By.NAME, 'Filedata').send_keys(abs_path)

  title_input = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located(
      (
        By.CSS_SELECTOR,
        "div.input-container.title.style-scope.ytcp-video-metadata-editor-basics ytcp-social-suggestions-textbox#title-textarea div#child-input div#textbox",
      )
    )
  )
  title_input.clear()
  title_input.send_keys(title)

  next_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="next-button"]'))
  )
  for i in range(3):
      next_button.click()
      time.sleep(1)

  done_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="done-button"]'))
  )
  done_button.click()
  time.sleep(5)

  bot.quit()
