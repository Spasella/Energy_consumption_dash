import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import pandasql as ps
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc
from plotly.offline import plot
from dash import Dash, dcc, html, Input, Output, dash_table
from plotly.subplots import make_subplots
from datetime import date
import json

import requests

import random
import numpy as np
from datetime import datetime


df_final = pd.read_csv('https://raw.githubusercontent.com/Spasella/cer/main/df_final.csv')


#CREATE ADOBE DATASET
regex = 'AA_M.*'
df_AA = df_final[df_final['source'].str.match(regex)]



#BING - GA - FB - GADS - - - SUMMARY
q_summary = '''select dataset_name, _BATCH_LAST_RUN_, _COUNT_ROWS_, link from df_final where dataset_name not regexp 'CW_AA' '''
df_summary = ps.sqldf(q_summary)







#APP SPACE
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.VAPOR])
server = app.server
LUXOTTICA_LOGO = "https://www.jest.it/wp-content/uploads/2018/10/Logo-Luxottica.jpg"
button = dbc.Row([
        dbc.Col(
            dbc.Button(
                "GO TO DOMO", color="primary", className="btn btn-outline-light", n_clicks=0,
                href='https://luxottica.domo.com/datacenter/datasources',
            ),
            width="auto",
        ),
    ], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", align="right",)
controls = dcc.DatePickerRange(
            id="_date_picker_range_",
            start_date=datetime(2022, 11, 18).strftime('%Y-%m-%d'),
            end_date=datetime.today().strftime('%Y-%m-%d'),
            style={'background-color': 'black'})


navbar = dbc.Navbar(dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LUXOTTICA_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("CYBERWEEK DATA-TEAM CONTROLLER", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://luxottica.domo.com/datacenter/datasources",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                controls,
                id="navbar-collapse_1",
                is_open=False,
                navbar=True,
            ),
            dbc.Collapse(
                button,
                id="navbar-collapse_2",
                is_open=False,
                navbar=True,
            ),]), color="#111111", dark=True,)

#LAYOUT SPACE
app.layout = dbc.Container([
    html.Div(id = 'parent', children = [navbar]),
    html.Nav(id='nav', className='menu'),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card(dcc.Graph(id='linebar_chart'), class_name="card border-light mb-3")
                ], xl= 9, xxl= 9, xs=9),
    ]
    ),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                        dash_table.DataTable(
                            data= df_summary.to_dict('records'),
                            columns= [{"name": i, "id": i} for i in df_summary.columns],
                            style_header={'border': 'Secondary',
                                          'backgroundColor': 'Warning',
                                          'color': 'black',
                                          'fontWeight': 'bold'},
                            style_cell={'border': '1px solid grey',
                                        'backgroundColor': 'dark'},
                            style_data={
                                'color': 'Primary',
                                'backgroundColor': 'black'
                            },
                            style_table={'overflowY':'scroll',
                                         'height':500,
                                         'width':1500,
                                         'border': '1px Primary'},
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            row_selectable="multi",
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=15,

                        ),



                ], xl= 6, xxl= 6, xs=6),
                    ]),
            html.Br(),

            ],xl= 3, xxl= 3, xs=3, style={'border-color':'light'})

])

], fluid=True)




#========================
#    CALLBACK SPACE
#========================
@app.callback(
    Output("linebar_chart", "figure"),
    [Input("_date_picker_range_", "start_date"), Input("_date_picker_range_", "end_date")]
)

def update_linebar_chart(start_date, end_date):
    df_filter_data_1 = df_AA[(df_AA['_BATCH_LAST_RUN_DATE']>=start_date) & (df_AA['_BATCH_LAST_RUN_DATE']<=end_date)]
    q = '''select* FROM df_filter_data_1 GROUP BY _BATCH_LAST_RUN_HOUR, dataset_name
    '''
    df_filter_data_2 = ps.sqldf(q)
    print('DF FINAL',df_AA[['_BATCH_LAST_RUN_DATE', '_BATCH_LAST_RUN_HOUR','dataset_name']])
    print('DF FILTRATO',df_filter_data_2)
    fig = px.line(df_filter_data_2, x='_BATCH_LAST_RUN_HOUR', y='_COUNT_ROWS_',
                 hover_data=['_COUNT_ROWS_', 'dataset_name', 'link', '_BATCH_LAST_RUN_'], color='dataset_name',
                 #color_discrete_sequence=['#0d47a1', '#2962ff', '#e3f2fd'],
                 custom_data=['dataset_name', 'link', '_BATCH_LAST_RUN_HOUR', '_BATCH_LAST_RUN_DATE', '_BATCH_LAST_RUN_'],
                 labels={'_COUNT_ROWS_': 'Count Rows',
                         'dataset_name': 'dataset_name'},

                 height=400)
    fig.update_layout(template='plotly_dark')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig







#========================
#RUNNING SPACE
#========================
#========================
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)

