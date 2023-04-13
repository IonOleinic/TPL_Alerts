import os
import time
from threading import Thread
import pywhatkit
from datetime import datetime
from whatsapp import send_whatsapp_msg

class Statie():
    def __init__(self,denumire,ip_panou,ip_tvm,ip_camera,ip_switch) -> None:
        self.denumire=str(denumire)
        self.ip_panou=str(ip_panou)
        self.ip_tvm=str(ip_tvm)
        self.ip_camera=str(ip_camera)
        self.ip_switch=str(ip_switch)

    def check_ip_station(self,ip,ip_source_text,whatsap_group_id,wait_time):
        while(True):
            self.check_ip(ip,ip_source_text,whatsap_group_id)
            # print(f"Next ping for {ip_source_text} {self.denumire} will be after {wait_time} sec...")
            time.sleep(wait_time)
        

    def check_station(self,whatsap_group_id='HR4sPdnEGnI1vNGGehBmr4')-> None:
        Thread(target=self.check_ip_station,args=(self.ip_panou,"Panou",whatsap_group_id,3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_tvm,"TVM",whatsap_group_id,600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_camera,"Camera",whatsap_group_id,3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_switch,"Switch",whatsap_group_id,3600)).start()
        
        
    def check_ip(self,ip,ip_source_text,whatsap_group_id)-> None:
        if(ip!='None'):
            response = os.popen(f"ping -n 4 {ip}").read()
            if "Received = 0" in response :
                data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # pywhatkit.sendwhatmsg_to_group_instantly(whatsap_group_id,f"(TEST)\nLipsa conexiune {ip_source_text} {self.denumire}\n{data}")
                send_whatsapp_msg("Echipa racheta",f"(TEST)\nLipsa conexiune {ip_source_text} {self.denumire}\n{data}")
                print(f"(TEST)\nLipsa conexiune {ip_source_text} {self.denumire}\n{data}")
                print(f"Trimis mesaj alerta ip catre Whatsap\n")
                
    
    def __str__(self):
        return self.denumire+" "+self.ip_panou+" "+self.ip_tvm+" "+self.ip_camera+" "+self.ip_switch