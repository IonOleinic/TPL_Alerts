import requests
from bs4 import BeautifulSoup
import time
import pywhatkit
import os
import openpyxl
from statie import Statie
from alerta import Alerta
from stoc import Stoc
from threading import Thread
from datetime import datetime
from pathlib import Path
from selenium import webdriver
import PyPDF2

downloads_path = str(Path.home() / "Downloads")
group_id='HR4sPdnEGnI1vNGGehBmr4'
session=requests.session()

def pkill (process_name):
      try:
         killed = os.system('taskkill /f /im ' + process_name).read()
      except Exception:
         killed = 0
      return killed

def check_ips():
   path = "IP echipamente statii.xlsx"
   wb_obj = openpyxl.load_workbook(path)
   sheet_obj = wb_obj.active
   max_col = sheet_obj.max_column
   max_row = sheet_obj.max_row
   stations_list=[]
   for i in range(2,max_row+1):
      cell_denumire=sheet_obj.cell(i,2).value
      cell_panou=sheet_obj.cell(i,3).value
      cell_tvm=sheet_obj.cell(i,4).value
      cell_camera=sheet_obj.cell(i,5).value
      cell_switch=sheet_obj.cell(i,6).value
      if(cell_denumire!=None):
         station=Statie(cell_denumire,cell_panou,cell_tvm,cell_camera,cell_switch)
         stations_list.append(station)
   for i in range(len(stations_list)):
      stations_list[i].check_station(group_id)
   

def check_alerts():
   def get_login_credentials():
      res=session.get("http://192.168.95.93/Skayo_CFM/Authentication.aspx?ReturnUrl=/Skayo_CFM/Default.aspx")
      soup=BeautifulSoup(res.content,'html.parser')
      ctl03_ctl00_TSM=soup.find('input',id="ctl03_ctl00_TSM").attrs["value"] 
      __VIEWSTATE=soup.find('input',id="__VIEWSTATE").attrs["value"] 
      __VIEWSTATEGENERATOR=soup.find('input',id="__VIEWSTATEGENERATOR").attrs["value"] 
      __VIEWSTATEENCRYPTED=soup.find('input',id="__VIEWSTATEENCRYPTED").attrs["value"] 
      __EVENTVALIDATION=soup.find('input',id="__EVENTVALIDATION").attrs["value"] 
      ctl03_cboCompany_ClientState=soup.find('input',id="__EVENTVALIDATION").attrs["value"] 
      txtUserName="admin"
      txtPassword='ticketing'
      tibAuthentication="Autentificare"
      payload={
         "ctl03_ctl00_TSM":ctl03_ctl00_TSM,
         "__VIEWSTATE":__VIEWSTATE,
         "__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,
         "__VIEWSTATEENCRYPTED":__VIEWSTATEENCRYPTED,
         "__EVENTVALIDATION":__EVENTVALIDATION,
         "ctl03_cboCompany_ClientState":ctl03_cboCompany_ClientState,
         "ctl03$txtUserName":txtUserName,
         "ctl03$txtPassword":txtPassword,
         "ctl03$tibAuthentication":tibAuthentication
      } 
      res=session.post("http://192.168.95.93/Skayo_CFM/Authentication.aspx?ReturnUrl=/Skayo_CFM/Default.aspx",data=payload)

   def check_if_alert_in(alert_id,alert_list):
      for i in range(len(alert_list)):
         if(alert_id==alert_list[i].id):
            return True
      return False

   def delete_expired_alerts(alert_list):
      result_list=[]
      for i in range(len(alert_list)):
         if(alert_list[i].ttl>0):
            result_list.append(alert_list[i])
         else:
            print('\n\x1b[1;36;43m' + f'A expirat timpul pentru alerta {alert_list[i].nume} {alert_list[i].data}' + '\x1b[0m\n')
      return result_list

   get_login_credentials()
   alert_list_already_send=[]
   rata_refresh=25
   wait_time=30*60
   default_alert_ttl=wait_time/rata_refresh
   sended_messages=0
   while True:
      try:
         response = session.get('http://192.168.95.93/Skayo_CFM/AVM/Manage/AlertListView.aspx')
         soup=BeautifulSoup(response.content,'html.parser')
         table_id='ctl00_cphContent_gridAlerts_ctl00'
         table_tag=soup.find('table',id=table_id)
         if(table_tag):
            alert_finded=False
            for i in range(10):
               row_tag=table_tag.find('tr',id=(table_id+"__"+str(i)))
               td_list=row_tag.find_all('td',class_='col-lg-1')
               tip_alerta=row_tag.find('td',class_='col-lg-3').text
               nume_TVM=td_list[0].text
               data_alerta=td_list[1].text
               alert_id=nume_TVM+data_alerta[0:10]
               if('Defect hardware' in tip_alerta):
                  alert_finded=True
                  print('\x1b[1;31;40m' + 'Defect Hardware detectat!!!' + '\x1b[0m')
                  print(nume_TVM)
                  print(data_alerta,end='')
                  print(tip_alerta)
                  if(check_if_alert_in(alert_id,alert_list_already_send)==False):
                     now=datetime.now()
                     if(now.hour<5):
                           alert_ttl=60*60/rata_refresh
                     else:
                        alert_ttl=default_alert_ttl
                     new_alert=Alerta(alert_id,nume_TVM,data_alerta,tip_alerta,alert_ttl)
                     pywhatkit.sendwhatmsg_to_group_instantly(group_id,f"TPL Suceava Skayo TVM Alert\n{nume_TVM}\n{data_alerta}\n{tip_alerta}")
                     print(f"Trimis mesaj alerta de la {new_alert.nume} catre Whatsap\n")
                     alert_list_already_send.append(new_alert)
                     sended_messages+=1
                  else:
                     print('\x1b[1;36;43m' + 'Mesaj deja trimis pe Whatsap' + '\x1b[0m\n')
            if(alert_finded==False):
               print("Nimic gasit.")
               if(sended_messages>2):
                  sended_messages=0
                  pkill('msedge.exe')
            alert_list_already_send=delete_expired_alerts(alert_list_already_send)
         else:
            print("Eroare logare.Se incearca din nou...")
            get_login_credentials()

         for i in range(len(alert_list_already_send)):
            alert_list_already_send[i].ttl-=1

         print(f"Refresh dupa {rata_refresh} sec...")
         print('-------------------------------------')
         time.sleep(rata_refresh) 
      except Exception as e:
        print("Failed with:", e.strerror) 
        print("Error code:", e.code)
        get_login_credentials()

def check_stocks():
  
  def list_to_str(list,delimiter):
      result=''
      for i in range(len(list)):
          result+=list[i]+delimiter
      return result

  def parse_pdf(pdf_name,sended_messages):
     if(pdf_name==None):
        print("[PARSE] File not exist or was removed.")
        return
     else:
      pdf_path=downloads_path+'/'+pdf_name
      if os.path.exists(pdf_path):
       with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        list_to_collect=[]
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            lines = text.splitlines()
            for i in range(10,len(lines)):
                line=lines[i].split(' ')
                if(len(line)>30):
                  nume_TVM=list_to_str(line[30:],' ')
                  if("Stefan" in nume_TVM):
                     nume_TVM="Colegiul Stefan cel Mare"
                  nr_bancnote=int(line[11])
                  if(nr_bancnote>399):
                     stoc=Stoc(nume_TVM,nr_bancnote)
                     list_to_collect.append(stoc)
        
        if(len(list_to_collect)==0):
           print("Nu sunt TVM-uri de colectat.")
           if(sended_messages>2):
               sended_messages=0
               pkill('msedge.exe')
        else:
            now=datetime.now()
            if(now.hour>5 and now.hour<22):    
               whatsapp_text=""
               for stoc in list_to_collect:
                     whatsapp_text+=stoc.nume_TVM+" "+str(stoc.nr_bancnote)+"\n"
               print("TVM-uri de colectat:")
               print(whatsapp_text)
               pywhatkit.sendwhatmsg_to_group_instantly(group_id,f"TPL Suceava Stocuri Bancnote:\n{whatsapp_text}")
               print(f"Trimis mesaj situatie stocuri catre Whatsap\n")
            else:
               print(f"Este ora {now.hour}, e tarziu deja...Nu mai trimitem mesaj pe whatsapp...")
      else:
         print("PDF File Not Found.")

  def download_pdf_stocuri():
      try:
         driver = webdriver.Firefox()
         time.sleep(1)
         driver.get("http://192.168.95.93/Skayo_CFM/Authentication.aspx?ReturnUrl=/Skayo_CFM/Default.aspx")
         username_field = driver.find_element('name','ctl03$txtUserName')
         username_field.send_keys('admin')
         time.sleep(1)
         password_field = driver.find_element('name','ctl03$txtPassword')
         password_field.send_keys('ticketing')
         time.sleep(1)
         login_form = driver.find_element('name','ctl03$tibAuthentication')
         login_form.click()
         time.sleep(1)
         driver.get("http://192.168.95.93/Skayo_CFM/Reporting/Local/ReportCreator.aspx?RID=428")
         time.sleep(2)
         generate_btn = driver.find_element('id','ctl00_cphContent_tibGenerate')
         generate_btn.click()
         time.sleep(15)
         driver.switch_to.frame("Situatie stocuri curenta")
         btn_export_pdf = driver.find_element('id','btnExportPdf')
         btn_export_pdf.click()
         time.sleep(10)
         driver.quit()
      except OSError as e:
         print("Failed with:", e.strerror)
         print("Error code:", e.code) 
         driver.quit()

  def find_pdf(partial_name):
     full_list = os.listdir(downloads_path)
     latest_date=0
     finded_file=None
     for file in full_list:
        if(partial_name in file):
           file_path=downloads_path+'/'+file
           file_name,file_extension=os.path.splitext(file_path)
           if(file_extension=='.pdf'):
              if(os.path.getctime(file_path)>latest_date):
                  latest_date=os.path.getctime(file_path)
                  finded_file=file
     return finded_file

  def delete_pdf(pdf_name):
   if(pdf_name==None):
      print("File not exist or was removed.")
      return
   pdf_path=downloads_path+'/'+pdf_name
   if os.path.exists(pdf_path):
      try:
        os.remove(pdf_path)
        print("FILE '",pdf_name,"' was deleted")
      except OSError as e: 
        print("Failed with:", e.strerror) 
        print("Error code:", e.code) 
   else:
     print("[DELETE] The file does not exist")
     
  refresh_stocuri=3600
  sended_messages=0
  while(True):
   try:
      download_pdf_stocuri()  
      time.sleep(1)
      print()
      pdf_name=find_pdf('Situatie stocuri curenta')
      parse_pdf(pdf_name,sended_messages)
      delete_pdf(pdf_name)
      print()
   except OSError as e:
      print("Failed with:", e.strerror)
      print("Error code:", e.code) 
   time.sleep(refresh_stocuri)
   

def main():
   
   Thread(target=check_ips).start()
   Thread(target=check_alerts).start()
   # Thread(target=check_stocks).start()

main()    