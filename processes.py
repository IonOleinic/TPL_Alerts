import psutil
import os

def check_if_process_run(process_name):
   for proc in psutil.process_iter():
      try:
         # Check if process name contains the given name string.
         if process_name.lower() in proc.name().lower():
               return True
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
         pass
   return False

def pkill(process_name):
    try:
        if(check_if_process_run(process_name)==True):
            killed = os.system('taskkill /f /im ' + process_name).read()
    except Exception as e:
        killed = 0
    return killed
