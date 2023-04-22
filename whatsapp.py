from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import os
from threading import Thread
import psutil
import random
import file_logger

def pkill (process_name):
      try:
         killed = os.system('taskkill /f /im ' + process_name).read()
      except Exception:
         killed = 0
      return killed

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def send_msg(chat_name,message,message_type):

   def send():
      wait_time=0
      while(checkIfProcessRunning('msedge.exe')==True):
         wait=10+random.randint(0,5)
         file_logger.log(f"Se asteapta finisarea trimiterii unui mesaj mai vechi...({wait} sec)")
         time.sleep(wait) #wait for finishing prev process
         wait_time+=wait
         if(wait_time>200):
            pkill('msedge.exe')
            wait_time=0
      time.sleep(1)  
      file_logger.log(f"Se trimite mesaj {message_type} catre Whatsap...") 
      profile_path='C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Edge\\User Data'
      opts=webdriver.EdgeOptions()
      # opts.add_argument("--headless")
      # opts.add_argument("--disable-gpu")
      opts.add_argument('--log-level=3')
      opts.add_argument(f"--user-data-dir={profile_path}")
      driver = webdriver.Edge(options=opts)
      time.sleep(5)
      driver.get(f'https://web.whatsapp.com/')
      search_box = WebDriverWait(driver, 50).until(
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
      time.sleep(3)
      driver.quit()
      file_logger.log(f"Mesaj {message_type} trimis cu succes.")
   try:
      send()
   except Exception as e:
      file_logger.log(f"Eroare trimitere mesaj Whatsapp.Se incearca din nou dupa...5 sec")
      # print(e)
      #try to resend after 5 sec
      pkill("msedge.exe")
      time.sleep(5)
      send()
     
def send_whatsapp_msg(chat_name,message,message_type):
      
      time.sleep(3)
      Thread(target=send_msg,args=(chat_name,message,message_type)).start()
      