import os
import time
from threading import Thread
from datetime import datetime
from whatsapp import send_whatsapp_msg
import file_logger
import network
class Statie():
    def __init__(self,nume_statie,ip_panou,ip_tvm,ip_camera,ip_switch) -> None:
        self.nume_statie=str(nume_statie)
        self.ip_panou=str(ip_panou)
        self.ip_tvm=str(ip_tvm)
        self.ip_camera=str(ip_camera)
        self.ip_switch=str(ip_switch)

    def check_ip_station(self,ip,tip_echipament,wait_time):
        while(True):
            while(network.check_local_network_conn()==False):
                time.sleep(600)
            sleep_time=wait_time
            result=self.check_ip(ip)
            inspect_min=9.1
            inspect_sec=inspect_min*60
            iterations=inspect_sec/10
            total_exceed_sec= iterations*10 + iterations*12 #12 sec aprox dureaza requestul de ping cu 4 interogari
            total_exceed_min= int(total_exceed_sec/60)
            if(result==False):
                file_logger.log(f"IP-ul {ip} ({tip_echipament} {self.nume_statie}) nu raspunde la ping. Inspecteaza {total_exceed_min} min...")
                remaining_sec=inspect_sec
                while(remaining_sec>=0 and result==False):
                    result=self.check_ip(ip)
                    remaining_sec-=10
                    time.sleep(10)
                if(result==True):
                    file_logger.log(f"IP-ul {ip} ({tip_echipament} {self.nume_statie}) a raspuns cu succes la ping dupa intrerupere.")
                elif(result==False):
                    file_logger.log(f"IP-ul {ip} ({tip_echipament} {self.nume_statie}) nu a raspuns la ping timp de {total_exceed_min} min.")
                    now=datetime.now()
                    sleep_time=wait_time-total_exceed_sec
                    if(now.hour>=5 and now.hour<=21):
                        data=now.strftime('%d.%m.%Y %H:%M:%S')
                        message=f"Lipsa conexiune {tip_echipament} {self.nume_statie}\n{data}"
                        file_logger.log("\n"+message)
                        send_whatsapp_msg("Echipa racheta",message,"lipsa conexiune")
            time.sleep(sleep_time)
        

    def check_station(self):
        Thread(target=self.check_ip_station,args=(self.ip_panou,"Panou",3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_tvm,"TVM",1800)).start()
        Thread(target=self.check_ip_station,args=(self.ip_camera,"Camera",3600)).start()
        Thread(target=self.check_ip_station,args=(self.ip_switch,"Switch",3600)).start()
        
        
    def check_ip(self,ip):
        result=True
        if(ip!=None and ip!='None' and ip!='' and ip[0].upper()!='X'):
            response = os.popen(f"ping -n 4 {ip}").read()
            if ("Received = 0" in response) or ('unreachable' in response):
                result=False
        return result
    
    def __str__(self):
        return self.nume_statie+" "+self.ip_panou+" "+self.ip_tvm+" "+self.ip_camera+" "+self.ip_switch