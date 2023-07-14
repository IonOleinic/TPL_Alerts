from datetime import datetime


def init_logs():
   try:
      f = open("logs.txt", "w")
      f.write("START\n")
      f.close()
   except Exception as e:
      print(e)  

def log(message):
   try:
      print(message)
      f = open("logs.txt", "a")
      now=datetime.now()
      data=now.strftime('%d.%m.%Y %H:%M:%S')
      f.write(f"[{data}] :  {str(message)}\n")
      f.close()
   except Exception as e:
      print(e)