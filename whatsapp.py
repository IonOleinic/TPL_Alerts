from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from threading import Thread
import random
import file_logger
import processes
import network

def send_msg(chat_name, message, message_type):

   def send():
      try:
         wait_time = 0
         while (processes.checkIfProcessRunning('msedge.exe') == True):
               wait = 5+random.randint(0, 10)
               file_logger.log(
                  f"Se asteapta finisarea trimiterii unui mesaj mai vechi...({wait} sec)")
               time.sleep(wait)  # wait for finishing prev process
               wait_time += wait
               if (wait_time > 200):
                  processes.pkill('msedge.exe')
                  wait_time = 0
         file_logger.log(
               f"Se trimite mesaj {message_type} catre Whatsap...")
         profile_path = 'C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Edge\\User Data'
         opts = webdriver.EdgeOptions()
         # opts.add_argument("--headless")
         opts.add_argument('--log-level=3')
         opts.add_argument(f"--user-data-dir={profile_path}")
         driver = webdriver.Edge(options=opts)
         time.sleep(4)
         driver.get(f'https://web.whatsapp.com/')
         search_box = WebDriverWait(driver, 50).until(
               EC.presence_of_element_located(
                  (By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'))
         )
         search_box.send_keys(chat_name)
         search_box.send_keys(Keys.ENTER)
         time.sleep(1)
         text_box = WebDriverWait(driver, 10).until(
               EC.presence_of_element_located(
                  (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'))
         )
         message_lines = message.split("\n")
         for line in message_lines:
               text_box.send_keys(Keys.SHIFT + Keys.ENTER)
               text_box.send_keys(line)
         text_box.send_keys(Keys.ENTER)
         time.sleep(3)
         driver.quit()
         file_logger.log(f"Mesaj {message_type} trimis cu succes.")
         return True
      except Exception as e:
         file_logger.log(e)
         return False

   while (send() == False):
      file_logger.log(
         f"Eroare trimitere mesaj Whatsapp.Se incearca din nou dupa...5 sec")
      # try to resend after 5 sec
      processes.pkill("msedge.exe")
      time.sleep(5)


def send_whatsapp_msg(chat_name, message, message_type):
   if(network.check_internet_conn()==True):
      time.sleep(3)
      Thread(target=send_msg, args=(chat_name, message, message_type)).start()
   else:
       file_logger.log(f"Nu exista conexiune la internet. Mesajul {message_type} nu va fi trimis pe whatsapp.")