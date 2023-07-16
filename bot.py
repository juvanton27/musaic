import os
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_bot() -> webdriver.Chrome:
  options = webdriver.ChromeOptions()
  options.add_argument("--log-level=3")
  options.add_argument(
    "user-data-dir=/Users/julienvantongerloo/Library/Application\ Support/Google/Chrome\ Beta/Default"
  )
  options.binary_location = (
    "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"
  )

  chromedriver_path = "/opt/homebrew/bin/chromedriver"
  os.environ["PATH"] += os.pathsep + chromedriver_path

  return webdriver.Chrome(options=options)


def upload_video(bot: webdriver.Chrome, video_path: str, title: str):
  bot.get("https://studio.youtube.com")

  upload_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="upload-icon"]'))
  )
  upload_button.click()

  file_input = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="select-files-button"]'))
  )
  file_input.click()

  abs_path = os.path.abspath(video_path)
  pyautogui.hotkey("command", "shift", "g")
  pyautogui.write(abs_path)
  pyautogui.press("enter")

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

  public_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.NAME, "PUBLIC"))
  )
  public_button.click()
  time.sleep(1)

  done_button = WebDriverWait(bot, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="done-button"]'))
  )
  done_button.click()
  time.sleep(5)

  bot.quit()
