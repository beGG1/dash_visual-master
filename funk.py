import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from datetime import timedelta


def calculate_korel(value):
        lab = pd.read_excel('./lab.xlsx')[:-1]
        model = pd.read_excel('./model.xlsx')
        lab = lab[:value]
        model = model[model.d >= lab.d.iloc[-1] - timedelta(hours=10)]
        liner_interp = interp1d(pd.to_numeric(model.d), model.v, kind='linear')

        model_vale_by_lab_time = liner_interp(pd.to_numeric(lab.d))
        lab_avg = 0

        for index, row in lab.iterrows():
            lab_avg = lab_avg + row['v']
        lab_avg = lab_avg/len(lab)

        model_avg = 0
        for i in model_vale_by_lab_time:
            model_avg = model_avg + float(i)
        model_avg = model_avg/len(model_vale_by_lab_time)

        chisl = 0
        s_x = 0
        s_y = 0
        for i in range(value):
            chisl = chisl + ((lab.v[i] - lab_avg) * (model_vale_by_lab_time[i] - model_avg))
            s_x = (lab.v[i] - lab_avg) * (lab.v[i] - lab_avg)
            s_y = (model_vale_by_lab_time[i] - model_avg) * (model_vale_by_lab_time[i] - model_avg)

        koef_korel = chisl/np.sqrt(s_x * s_y)

        return str(koef_korel)