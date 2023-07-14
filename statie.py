import os
import time
from threading import Thread
from datetime import datetime
from whatsapp import send_whatsapp_msg
import file_logger
class Statie():
    def __init__(self,denumire,ip_panou,ip_tvm,ip_camera,ip_switch) -> None:
        self.denumire=str(denumire)
        self.ip_panou=str(ip_panou)
        self.ip_tvm=str(ip_tvm)
        self.ip_camera=str(ip_camera)
        self.ip_switch=str(ip_switch)

    def check_ip_station(self,ip,ip_source_text,wait_time):
        while(True):
            self.check_ip(ip,ip_source_text)
            time.sleep(wait_time)
        

    def check_station(self):
        Thread(target=self.check_ip_station,args=(self.ip_panou,"Panou",3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_tvm,"TVM",600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_camera,"Camera",3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_switch,"Switch",3600)).start()
        
        
    def check_ip(self,ip,ip_source_text):
        if(ip!='None'):
            response = os.popen(f"ping -n 4 {ip}").read()
            if "Received = 0" in response:
                now=datetime.now()
                if(now.hour>4 and now.hour<23):
                    data=now.strftime('%d.%m.%Y %H:%M:%S')
                    message=f"Lipsa conexiune {ip_source_text} {self.denumire}\n{data}"
                    file_logger.log("\n"+message)
                    send_whatsapp_msg("Echipa racheta",message,"lipsa conexiune")
    
    def __str__(self):
        return self.denumire+" "+self.ip_panou+" "+self.ip_tvm+" "+self.ip_camera+" "+self.ip_switch