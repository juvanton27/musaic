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

  # return webdriver.Chrome(options) if platform.system() == 'Darwin' else webdriver.Chrome() if platform.system() == 'Linux' else webdriver.Chrome()
  return webdriver.Chrome(options)

def upload_video(bot: webdriver.Chrome, video_path: str, title: str):
  bot.get("https://studio.youtube.com")
  print('Went to site')

  try:
    upload_button = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located((By.XPATH, '//*[@id="upload-icon"]'))
    )
    print('found upload button')
    upload_button.click()
    print('clicked on it')
    time.sleep(2)
    print('slept 2 sec')
  except:
    print('Not logged')
    bot.quit()
    return

  try:
    abs_path = os.path.abspath(video_path)
    print(abs_path)
    bot.find_element(By.NAME, 'Filedata').send_keys(abs_path)
    print('sent file')
  except:
    print('Uploading video failed')
    bot.quit()
    return

  try:
    title_input = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located(
        (
          By.CSS_SELECTOR,
          "div.input-container.title.style-scope.ytcp-video-metadata-editor-basics ytcp-social-suggestions-textbox#title-textarea div#child-input div#textbox",
        )
      )
    )
    print(title_input)
    title_input.clear()
    print('input cleared')
    title_input.send_keys(title)
    print('add input')
    time.sleep(2)
    print('slept 2 sec')
  except:
    print('Changing title failed')
    bot.quit()
    return 

  try:
    visibility_button = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located(
        (
          By.XPATH,
          '//button[@test-id=REVIEW]'
        )
      )
    )
    print('found visibility button')
    visibility_button.click()
    print('clicked on it')
    time.sleep(1)
    print('slept 1 sec')
  except:
    print('Finding visibility button failed')
    bot.quit()
    return 

  try:
    done_button = WebDriverWait(bot, 10).until(
      EC.visibility_of_element_located(
        (
          By.CSS_SELECTOR,
          "ytcp-animatable.button-area.metadata-fade-in-section.style-scope.ytcp-uploads-dialog div.inner-button-area.style-scope.ytcp-uploads-dialog div.right-button-area.style-scope.ytcp-uploads-dialog ytcp-button#done-button"
        )
      )
    )
    print('found done button')
    done_button.click()
    print('clicked on it')
    time.sleep(5)
    print('slept 5 sec')
  except:
    print('Finding done button failed')
    bot.quit()
    return

  bot.quit()
  print('quit')
