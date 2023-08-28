import requests
import file_logger


def check_local_network_conn():
    try:
        res = requests.get("http://192.168.95.93/Skayo_CFM/")
        return True
    except Exception as e:
        return False
    
def check_internet_conn():
    try:
        res = requests.get("https://www.google.com/")
        return True
    except Exception as e:
        return False