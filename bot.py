import os
import time
import platform

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def create_bot() -> Chrome:
  options = ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--window-size=1920,1080")
  options.add_argument("--enable-logging")
  options.add_argument("--v=1")
  options.add_argument(f"user-data-dir={os.getenv('USER_DATA_DIR')}")
  if platform.system() == 'Darwin':
    options.binary_location = os.getenv('BINARY_LOCATION')

  chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
  os.environ["PATH"] += os.pathsep + chromedriver_path

  return Chrome(options)

def upload_video(bot: Chrome, video_path: str, title: str):
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

# def check_exists_by_xpath(driver, xpath):
#   try:
#     driver.find_element_by_xpath(xpath)
#   except common.exceptions.NoSuchElementException:
#     return False

#   return True

def upload_tiktok(bot: Chrome, video_path: str, title: str):
  # bot.get('https://www.tiktok.com/upload?lang=fr')
  # print('site joined')
  # time.sleep(40)

  # try:
  #   abs_path = os.path.abspath(video_path)
  #   print(abs_path)
  #   bot.find_element(By.XPATH, '//input[@type="file"]').send_keys(abs_path)
  #   print('input found')
  # except Exception as e:
  #   print(e)
  #   print('Uploading video failed')
  #   bot.quit()
  #   return
  
  # try:
  #   title_input = WebDriverWait(bot, 10).until(
  #     EC.visibility_of_element_located((By.XPATH, '//*[@data-text="true"]'))
  #   )
  #   print('title input found')
  #   title_input.clear()
  #   print('title cleared')
  #   title_input.send_keys(title)
  #   print('title changed')
  #   time.sleep(2)
  #   print('slept 2 sec')
  # except Exception as e:
  #   print(e)
  #   print('Changing title failed')
  #   bot.quit()
  #   return

  # file_uploader = bot.find_element_by_xpath(
  #     '//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div/input')

  # file_uploader.send_keys(video_path)

  # caption = bot.find_element_by_xpath(
  #     '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')

  # bot.implicitly_wait(10)
  # webdriver.common.action_chains.ActionChains(bot).move_to_element(caption).click(
  #     caption).perform()
  # # webdriver.common.action_chains.ActionChains(bot).key_down(Keys.CONTROL).send_keys(
  # #     'v').key_up(Keys.CONTROL).perform()

  # tags = [title]

  # for tag in tags:
  #     webdriver.common.action_chains.ActionChains(bot).send_keys(tag).perform()
  #     time.sleep(2)
  #     webdriver.common.action_chains.ActionChains(bot).send_keys(webdriver.common.keys.Keys.RETURN).perform()
  #     time.sleep(1)

  # time.sleep(5)
  # bot.execute_script("window.scrollTo(150, 300);")
  # time.sleep(5)

  # post = WebDriverWait(bot, 100).until(
  #     EC.visibility_of_element_located(
  #         (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[5]/button[2]')))

  # post.click()
  # time.sleep(30)

  # if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
  #     reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
  #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

  #     reupload.click()
  # else:
  #     print('Unknown error cooldown')
  #     while True:
  #         time.sleep(600)
  #         post.click()
  #         time.sleep(15)
  #         if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
  #             break

  # if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
  #     reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
  #         (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
  #     reupload.click()

  # time.sleep(1)
  
  bot.quit()
