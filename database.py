import sqlite3
from pandas import DataFrame, to_datetime


class DataBase:
    def __init__(self) -> None:
        self.model_name = []
        self.lab_data = []
        self.model_data = []
        self.conn = sqlite3.connect("data.sqlite.db")
        self.c = self.conn.cursor()
        pass

    def select_model(self):
        
        self.model_name = self.c.execute("select * from model").fetchall()
    
    def change_lab(self, id_model):
        lab_data = self.c.execute(f'select date, value from data where lab_model = "lab" and data_id_model = {id_model}').fetchall()
        d = []
        for i in lab_data:
            d.append(to_datetime(i[0]))
        v = []
        for i in lab_data:
            v.append(float(i[1]))
        
        data_df = {'d': d, 'v':v}
        self.lab_data = DataFrame(data=data_df)
        

    def change_model(self, id_model):
        model_data = self.c.execute(f'select date, value from data where lab_model = "model" and data_id_model = {id_model}').fetchall()
        d = []
        for i in model_data:
            d.append(to_datetime(i[0]))
        v = []
        for i in model_data:
            v.append(float(i[1]))
        
        data_df = {'d': d, 'v':v}
        self.model_data = DataFrame(data=data_df)
