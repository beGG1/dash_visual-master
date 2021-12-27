from pandas import read_excel, to_numeric


class MyData:
    def __init__(self):
        self.lab_data = read_excel('./lab.xlsx')[:-1]
        self.model_data = read_excel('./model.xlsx')
        pass