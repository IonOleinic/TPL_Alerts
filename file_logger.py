from datetime import datetime


def init_logs():
   try:
      f = open("logs.txt", "w")
      f.write("START\n")
      f.close()
   except Exception as e:
      print(e)  

def log(message,console_only=False):
   try:
      print(message)
      if(console_only==False):
         f = open("logs.txt", "a")
         now=datetime.now()
         data=now.strftime('%d.%m.%Y %H:%M:%S')
         f.write(f"[{data}] :  {str(message)}\n")
         f.close()
   except Exception as e:
      print(e)