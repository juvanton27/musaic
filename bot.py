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
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--enable-logging")
  options.add_argument("--v=1")
  options.add_argument(f"user-data-dir={os.getenv('USER_DATA_DIR')}")
  if platform.system() == 'Darwin':
    options.binary_location = os.getenv('BINARY_LOCATION')

  chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
  os.environ["PATH"] += os.pathsep + chromedriver_path

  return webdriver.Chrome(options)

def upload_video(bot: webdriver.Chrome, video_path: str, title: str):
  bot.get("https://studio.youtube.com")

  try:
    upload_button = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located((By.XPATH, '//*[@id="upload-icon"]'))
    )
    upload_button.click()
    time.sleep(2)
  except:
    print('Not logged')
    bot.quit()
    return

  try:
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), video_path))
    print(abs_path)
    bot.find_element(By.NAME, 'Filedata').send_keys(abs_path)
  except:
    print('Uploading video failed')
    bot.quit()
    return

  try:
    title_input = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located(
        (
          By.CSS_SELECTOR,
          "div.input-container.title.style-scope.ytcp-video-metadata-editor-basics div#textbox",
        )
      )
    )
    title_input.clear()
    title_input.send_keys(title)
    time.sleep(2)
  except:
    print('Changing title failed')
    bot.quit()
    return 

  try:
    visibility_button = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located(
        (
          By.XPATH,
          '//button[@id="step-badge-3"]'
        )
      )
    )
    visibility_button.click()
    time.sleep(1)
  except:
    print('Finding visibility button failed')
    bot.quit()
    return 

  try:
    done_button = WebDriverWait(bot, 120).until(
      EC.visibility_of_element_located(
        (
          By.XPATH,
          '//ytcp-button[@id="done-button"]'
        )
      )
    )
    done_button.click()
    print('Waiting 1 minute for file from being uploaded ...')
    time.sleep(60)
  except:
    print('Finding done button failed')
    bot.quit()
    return
  bot.quit()

def upload_tiktok(bot: webdriver.Chrome, video_path: str, title: str):
  bot.get('https://www.tiktok.com/upload?lang=fr')
  print('site joined')
  time.sleep(40)

  try:
    abs_path = os.path.abspath(video_path)
    print(abs_path)
    bot.find_element(By.XPATH, '//input[@type="file"]').send_keys(abs_path)
    print('input found')
  except Exception as e:
    print(e)
    print('Uploading video failed')
    bot.quit()
    return
  
  try:
    title_input = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located((By.XPATH, '//*[@data-text="true"]'))
    )
    print('title input found')
    title_input.clear()
    print('title cleared')
    title_input.send_keys(title)
    print('title changed')
    time.sleep(2)
    print('slept 2 sec')
  except Exception as e:
    print(e)
    print('Changing title failed')
    bot.quit()
    return
  
