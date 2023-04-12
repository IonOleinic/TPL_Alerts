
class Alerta:
    
    def __init__(self,id_alerta,nume_alerta,data_ora,tip_alerta,time_to_live) -> None:
        self.id=id_alerta
        self.nume=nume_alerta
        self.data=data_ora
        self.tip=tip_alerta
        self.ttl=time_to_live
    