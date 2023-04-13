from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import os


def pkill (process_name):
      try:
         killed = os.system('taskkill /f /im ' + process_name).read()
      except Exception:
         killed = 0
      return killed

def send_whatsapp_msg(chat_name,message):
      try:
         pkill('msedge.exe')
         time.sleep(5)
         profile_path='C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Edge\\User Data'
         opts=webdriver.EdgeOptions()
         opts.add_argument("--headless")
         opts.add_argument("--disable-gpu")
         opts.add_argument('--log-level=3')
         opts.add_argument(f"--user-data-dir={profile_path}")
         driver = webdriver.Edge(options=opts)
         time.sleep(5)
         driver.get(f'https://web.whatsapp.com/')
         search_box = WebDriverWait(driver, 30).until(
         EC.presence_of_element_located(('xpath','//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'))
         )
         search_box.send_keys(chat_name)
         search_box.send_keys(Keys.ENTER)
         time.sleep(2)
         text_box = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located(('xpath','//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'))
         )
         message_lines = message.split("\n")
         for line in message_lines:
            text_box.send_keys(Keys.SHIFT + Keys.ENTER)
            text_box.send_keys(line)
         text_box.send_keys(Keys.ENTER)
         time.sleep(2)
         driver.quit()
      except Exception as e:
         print("Failed with:", e.strerror) 
         print("Error code:", e.code)
         driver.quit()