from pandas.core import series
import plotly.graph_objects as go
from numpy import array, sqrt, corrcoef
from pandas import read_excel, to_numeric, Series, Timestamp
from scipy.interpolate import interp1d
from plotly.subplots import make_subplots
from datetime import date, timedelta
from sklearn.metrics import r2_score, mean_squared_error\

from database import DataBase


def get_trend_fig(start_date, end_date, id_model):
    
    d = DataBase()
    d.change_lab(id_model)
    d.change_model(id_model)
    lab = d.lab_data
    model = d.model_data

    lab = lab[to_numeric(lab.d) >= Timestamp(start_date).value]
    lab = lab[to_numeric(lab.d) <= Timestamp(end_date).value]
    model = model[to_numeric(model.d) >= Timestamp(start_date).value]
    model = model[to_numeric(model.d) <= Timestamp(end_date).value]

    n = lab.shape[0]
    if n < 15:
        circle_size = 20
    elif n < 25:
        circle_size = 10
    else: 
        circle_size = 0

    
    model = model[model.d >= lab.d.iloc[-1] - timedelta(hours=10)]


    liner_interp = interp1d(to_numeric(model.d), model.v, kind='linear', fill_value="extrapolate")

    lab_time, model_vale_by_lab_time = lab.d,  liner_interp(to_numeric(lab.d))

    data = model_vale_by_lab_time - lab.v

    colors = array(['#1F5869', ] * len(lab_time))
    colors_model = array(["#33ffe6", ] * len(lab_time))
    colors_lab = array(["#ffd348", ] * len(lab_time))

    colors_lab[abs(data) > 3] = '#ff6e2e'
    colors_model[abs(data) > 3] = '#33ffe6'
    colors[abs(data) > 3] = '#ff2c6d'

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.11,
        row_heights=[0.7, 0.3]
    )

    fig.add_trace(go.Scatter(x=lab.d.iloc[:n],
                             y=lab.v.iloc[:n],
                             mode='lines+markers',
                             name='ЛИМС',
                             marker=dict(symbol='circle',
                                         line_color=colors_lab,
                                         color=colors_lab,
                                         line_width=1,
                                         size=circle_size),

                             line=dict(color='#ffd348', width=5)), row=1, col=1)

    fig.add_trace(go.Scatter(x=model.d,
                             y=model.v,
                             mode='lines',
                             name='Модель',
                             line=dict(color='#33ffe6', width=3)), row=1, col=1)

    fig.add_trace(go.Scatter(x=lab_time,
                             y=model_vale_by_lab_time,
                             showlegend=False,
                             name='Модель, ЛИМС',
                             mode='markers',
                             marker=dict(symbol='circle',
                                         line_color=colors_model,
                                         color=colors_model,
                                         line_width=1,
                                         opacity=1,
                                         size=circle_size),
                             ), row=1, col=1)

    fig.add_trace(go.Bar(x=lab_time[:n], y=data,
                         name='Ошибка',
                         marker_color=colors,
                         ), row=2, col=1)

    fig.update_layout(
        legend_orientation="h",
        legend_yanchor="top",
        legend_y=1.12,
        legend=dict(traceorder='normal', bgcolor='#153F4C'),
        font_family="Arial",
        font_color="#63A8A6",
        font_size=22,
        autosize=False,
        width=1190,
        height=875,
        margin=dict(r=0, l=0, t=10, b=0)
    )
    # #153F4C
    fig.update_xaxes(visible=True, gridcolor='#63A8A6', rangeslider_visible=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#63A8A6')
    fig.update_layout({'plot_bgcolor': '#153F4C', 'paper_bgcolor': '#153F4C'},
                      modebar_add=['togglespikelines', 'togglehover', 'v1hovermode'])

    return fig


def calculate_korel(start_date, end_date, id_model):
        d = DataBase()
        d.change_lab(id_model)
        d.change_model(id_model)
        lab = d.lab_data
        model = d.model_data
        lab = lab[to_numeric(lab.d) >= Timestamp(start_date).value]
        lab = lab[to_numeric(lab.d) <= Timestamp(end_date).value]
        model = model[to_numeric(model.d) >= Timestamp(start_date).value]
        model = model[to_numeric(model.d) <= Timestamp(end_date).value]
        value = lab.shape[0]
    
        if value == 0:
            return str('Значений нет')

        lab = lab[:value]
        model = model[model.d >= lab.d.iloc[-1] - timedelta(hours=10)]
        liner_interp = interp1d(to_numeric(model.d), model.v, kind='linear', fill_value="extrapolate")
        model_vale_by_lab_time = Series(liner_interp(to_numeric(lab.d)))
    
        l = []
        for i in lab.v:
            l.append(int(i))

        koef_korel =  corrcoef(l, model_vale_by_lab_time)

        return str(float('{:.3f}'.format(koef_korel[0][1])))



def calculate_determ(start_date, end_date, id_model):
    d = DataBase()
    d.change_lab(id_model)
    d.change_model(id_model)
    lab = d.lab_data
    model = d.model_data
    
    lab = lab[to_numeric(lab.d) >= Timestamp(start_date).value]
    lab = lab[to_numeric(lab.d) <= Timestamp(end_date).value]
    model = model[to_numeric(model.d) >= Timestamp(start_date).value]
    model = model[to_numeric(model.d) <= Timestamp(end_date).value]
    value = lab.shape[0]
    
    if value == 0:
        return str('Значений нет')

    lab = lab[:value]
    model = model[model.d >= lab.d.iloc[-1] - timedelta(hours=10)]
    liner_interp = interp1d(to_numeric(model.d), model.v, kind='linear', fill_value="extrapolate")
    model_vale_by_lab_time = Series(liner_interp(to_numeric(lab.d)))
    
    l = []
    for i in lab.v:
        l.append(int(i))

    #https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
    r2 = r2_score(l, model_vale_by_lab_time)
    return str(float('{:.3f}'.format(r2)))
    
    
def calculate_rms(start_date, end_date, id_model):
    d = DataBase()
    d.change_lab(id_model)
    d.change_model(id_model)
    lab = d.lab_data
    model = d.model_data
    lab = lab[to_numeric(lab.d) >= Timestamp(start_date).value]
    lab = lab[to_numeric(lab.d) <= Timestamp(end_date).value]
    model = model[to_numeric(model.d) >= Timestamp(start_date).value]
    model = model[to_numeric(model.d) <= Timestamp(end_date).value]
    value = lab.shape[0]
    
    if value == 0:
        return str('Значений нет')

    lab = lab[:value]
    model = model[model.d >= lab.d.iloc[-1] - timedelta(hours=10)]
    liner_interp = interp1d(to_numeric(model.d), model.v, kind='linear', fill_value="extrapolate")
    model_vale_by_lab_time = Series(liner_interp(to_numeric(lab.d)))
    
    l = []
    for i in lab.v:
        l.append(int(i))

    rms = mean_squared_error(l, model_vale_by_lab_time, squared=False)
    return str(float('{:.3f}'.format(rms)))

def change_labels():
        d = DataBase()
        d.select_model()
        data = d.model_name
        options = []
        for i in data:
            options.append({'label': i[1], 'value':str(i[0])})
        return options