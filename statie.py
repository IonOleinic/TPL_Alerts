import os
import time
from pythonping import ping
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from threading import Thread
import pywhatkit
from datetime import datetime

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
            print(f"Next ping for {ip_source_text} {self.denumire} will be after {wait_time} sec...")
            time.sleep(wait_time)
        

    def check_station(self,whatsap_group_id='HR4sPdnEGnI1vNGGehBmr4')-> None:
        Thread(target=self.check_ip_station,args=(self.ip_panou,"Panou",whatsap_group_id,3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_tvm,"TVM",whatsap_group_id,600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_camera,"Camera",whatsap_group_id,3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_switch,"Switch",whatsap_group_id,3600)).start()
        
        
    def check_ip(self,ip,ip_source_text,whatsap_group_id)-> None:
        if(ip!='None'):
            response = os.popen(f"ping -n 4 {ip}").read()
            if "Received = 3" in response or "Received = 4" in response or "Received = 2" in response:
                # print(f"UP IP {ip_source_text} {self.denumire} Ping Successful, Host is UP!")
                pass
            else:
                data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pywhatkit.sendwhatmsg_to_group_instantly(whatsap_group_id,f"(TEST)\nLipsa conexiune {ip_source_text} {self.denumire}\n{data}")
                print(f"(TEST)\nLipsa conexiune {ip_source_text} {self.denumire}\n{data}")
                print(f"Trimis mesaj alerta ip catre Whatsap\n")
    
    def __str__(self):
        return self.denumire+" "+self.ip_panou+" "+self.ip_tvm+" "+self.ip_camera+" "+self.ip_switch