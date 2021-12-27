from numpy import sqrt
import plotly.express as px
from dash import Dash
import copy
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as pd

from scipy.interpolate import interp1d
from datetime import date, timedelta

from plot_of_dash import get_trend_fig, calculate_korel, calculate_determ, calculate_rms, change_labels



app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = 'МКС: Аналитика'

app.layout = html.Div([
    html.H1("МКС: Аналитика", className='app-head-title'),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Инструмент для визуализации работы моделей", className='text-properties'),
                html.Label('Выберите модель', className='label-dropdown'),
                html.Div(
                    dcc.Dropdown(
                        options=[
                            {'label': 'Модель 1', 'value': '1'},
                            {'label': 'Модель 2', 'value': '2'},
                            {'label': 'Модель 3', 'value': '3'},
                            {'label': 'Модель 4', 'value': '4'},
                            {'label': 'Модель 5', 'value': '5'},
                            {'label': 'Модель 6', 'value': '6'}
                        ],
                        value='1',
                        id = 'my-dropdown-model'
                    ), className='dropdown-model'),
                html.Div([
                    html.Label('Выбор даты для анализа', className='slider-label'),
                    html.Div(
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(2021, 9, 1),
                            max_date_allowed=date(2022, 1, 1),
                            initial_visible_month=date(2022, 1, 1),
                            end_date=date(2022, 1, 1)
                        ),
                        style = {'margin-left': '85px'}
                    ),

                    html.Div(id='output-container-date-picker-range', style={'font-family' : 'Arial', 'text-align': 'center', 'font-size': '20px'})
                ]),
            ]),
            width=3,
            className='model-analyst',
        ),
        dbc.Col([
            html.Div([
                dcc.Graph(
                    id='models-lines',
                    #figure=get_trend_fig(n = 5)
                    figure = get_trend_fig(start_date=date(2021, 9, 1), end_date=date(2021, 10, 21), id_model=1)
                    # style={'display': 'none'}
                ),
            ], style={'margin-left': '0vw', 'margin-top': '10px'}),
        ],
            width=8,
            style={"height": "920px", "background-color": "#153F4C", 'margin-left': '50px'},

        ),

    ], style={"height": "310px", 'width': '1900px'}),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1(className='metric-value-style', id='R'),
                html.H6("Корреляция", className='metric-correlation-style'),
            ]),
            width={"size": 2, 'order': 2},
            className='metric-value-col-style'
        ),
        dbc.Col(
            html.P("R", className='metric-style'),
            width={"size": 1, 'order': 1},
            className="metric-col-style"
        ),
    ], style={"height": "160px", 'width': '1920px'}),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1(className='metric-value-style', id = 'S'),
                html.H6("Среднеквадратическое отклонение", className='metric-sred-style'),
            ]),
            width={"size": 2, 'order': 2},
            className='metric-value-col-style'
        ),
        dbc.Col(
            html.P("S", className='metric-style'),
            width={"size": 1, 'order': 1},
            className="metric-col-style",
        ),
    ], style={"height": "160px", 'margin-top': '20px', 'width': '1920px'}),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1(className='metric-value-style', id = 'D'),
                html.H6("Детерминация", className='metric-correlation-style'),
            ]),
            width={"size": 2, 'order': 2},
            className='metric-value-col-style'
        ),
        dbc.Col(
            html.P("D", className='metric-style'),
            width={"size": 1, 'order': 1},
            className="metric-col-style",
        ),
    ], style={"height": "160px", 'margin-top': '20px', 'width': '1920px'}),

    
])


@app.callback(
    Output("models-lines", "figure"), Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date'), Input('my-dropdown-model', 'value')
)
def change_active_page(start_date, end_date, value):

    return get_trend_fig(start_date, end_date, value)

@app.callback(
    Output("R", "children"), Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date'), Input('my-dropdown-model', 'value')
)
def change_corr_value(start_date, end_date, value):
    koef_korel = calculate_korel(start_date, end_date, value)
    return koef_korel

@app.callback(
    Output("S", "children"), Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date'), Input('my-dropdown-model', 'value')
)
def change_rms_value(start_date, end_date, value):
    rms = calculate_rms(start_date, end_date, value)
    return rms

@app.callback(
    Output("D", "children"), Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date'), Input('my-dropdown-model', 'value')
)
def change_deter_value(start_date, end_date, value):
    determ = calculate_determ(start_date, end_date, value)
    return determ

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'Даты анализа: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Начальная дата: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Конечная дата: ' + end_date_string
    if len(string_prefix) == len('Даты анализа: '):
        return 'Выберете дату'
    else:
        return string_prefix

@app.callback(
    Output("my-dropdown-model", "options"), Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date')
    )
def change_labels_value(start_date, end_date):

    return change_labels()

# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.run_server(debug=True)

