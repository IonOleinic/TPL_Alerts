from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from threading import Thread
from threading import Event
import random
import file_logger
import processes
import network
import queue

message_queue = queue.Queue()
message_available_event = Event()

def process_messages():
    while True:
        # Wait for the message available event to be set
         message_available_event.wait()
         try:
            if(not message_queue.empty() and network.check_internet_conn()):
               chat_name, message, message_type = message_queue.get()
               send_msg(chat_name, message, message_type)
               message_queue.task_done()
         except Exception as e:
            file_logger.log(e)
         if(message_queue.empty()):
            message_available_event.clear()

message_processing_thread = Thread(target=process_messages)

def send_whatsapp_msg(chat_name, message, message_type):
    if network.check_internet_conn():
         message_queue.put((chat_name, message, message_type))
         if not message_processing_thread.is_alive():
            message_processing_thread.start()
         message_available_event.set()
    else:
        file_logger.log(f"No internet connection. Message {message_type} will not be sent on WhatsApp.")

def send_msg(chat_name, message, message_type):
    def send():
         try:
            total_wait_time = 0
            while(processes.checkIfProcessRunning('msedge.exe')):
               wait = 5 + random.randint(0, 10)
               file_logger.log(f"Se asteapta finisarea trimiterii unui mesaj mai vechi... ({wait} sec)")
               time.sleep(wait)
               total_wait_time += wait
               if total_wait_time > 200:
                  processes.pkill('msedge.exe')
                  total_wait_time = 0
            file_logger.log(f"Se trimite mesaj {message_type} catre WhatsApp...")
            profile_path = 'C:\\Users\\Administrator\\AppData\\Local\\Microsoft\\Edge\\User Data'
            opts = webdriver.EdgeOptions()
            #opts.add_argument("--headless")
            opts.add_argument('--log-level=3')
            opts.add_argument(f"--user-data-dir={profile_path}")
            driver = webdriver.Edge(options=opts)
            time.sleep(3)
            driver.get('https://web.whatsapp.com/')
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
            time.sleep(1)
            driver.quit()
            file_logger.log(f"Mesaj {message_type} trimis cu succes.")
            return True
         except Exception as e:
               file_logger.log("****Error: Exception in function send(). The sending has crashed.****")
               return False

    if not send():
        file_logger.log(f"Eroare trimitere mesaj pe WhatsApp. Se incearca din nou...")
        # Try to resend by putting the message back in the queue
        message_queue.put((chat_name, message, message_type))
        message_available_event.set()
