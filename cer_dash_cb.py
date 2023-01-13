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
from dash import Dash, dcc, html, Input, Output
from datetime import date
import json
import requests
import sys
import certifi


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.CYBORG])
server = app.server


ca = certifi.where()
df_hourly = pd.read_csv('https://raw.githubusercontent.com/LudovicoLanzo92/CER_DB/main/hourly_database_ID202206.csv',
                        low_memory=False)


#0 - NUMBER CARDS DATASET
#---------------
cards_query = '''
              SELECT fascia_oraria, stabilimento, ROUND(SUM(consumi_kw_h), 2) as consumi_kw_h
              FROM df_hourly
              GROUP BY stabilimento, fascia_oraria
'''
cards_df = ps.sqldf(cards_query, locals())



#1 - LINEBAR CHART DATASET
#---------------
linebar_query = '''
SELECT date, anno, mese, fascia_oraria, stabilimento, ROUND(SUM(consumi_kw_h), 2) as consumi_kw_h
FROM df_hourly
GROUP BY date, anno, mese, fascia_oraria, stabilimento
'''
linebar_df = ps.sqldf(linebar_query, locals())






#2 - RADAR WEEKDAYS CHART DATASET
#---------------
#radar_chart_1_df = df_hourly = df_hourly.loc[df_hourly['stabilimento'] == "Frigo"]
#radar_chart_1_df['hour'] = radar_chart_1_df['hour'].astype(str)
radar_chart_stab_query = """
    SELECT stabilimento, ID_Utente, giorno_sett,  SUM(consumi_kw_h) as consumi_kw_h,
    CASE 
        WHEN hour like '0' or hour like '1' THEN '0-1'
        WHEN hour like '2' or hour like '3' THEN '2-3'
        WHEN hour like '4' or hour like '5' THEN '4-5'
        WHEN hour like '6' or hour like '7' THEN '6-7'
        WHEN hour like '8' or hour like '9' THEN '8-9'
        WHEN hour like '10' or hour like '11' THEN '10-11'
        WHEN hour like '12' or hour like '13' THEN '12-13'
        WHEN hour like '14' or hour like '15' THEN '14-15'
        WHEN hour like '16' or hour like '17' THEN '16-17'
        WHEN hour like '18' or hour like '19' THEN '18-19'
        WHEN hour like '20' or hour like '21' THEN '20-21'
        WHEN hour like '22' or hour like '23' THEN '22-23'

    END AS hour_group

    FROM df_hourly
    WHERE ID_Utente like 'ID202206'
    GROUP BY  hour_group, ID_Utente, stabilimento, giorno_sett
    """
radar_chart_stab_df = ps.sqldf(radar_chart_stab_query, locals())
radar_chart_stab_dropdown_options = radar_chart_stab_df['stabilimento'].unique()
#print(radar_chart_stab_df['hour_group'].unique())




#3 - RADAR MONTHS CHART DATASET
#---------------
radar_chart_2_query = """
    SELECT stabilimento, ID_Utente, mese,  SUM(consumi_kw_h) as consumi_kw_h,
    CASE 
        WHEN hour like '0' or hour like '1' THEN '0-1'
        WHEN hour like '2' or hour like '3' THEN '2-3'
        WHEN hour like '4' or hour like '5' THEN '4-5'
        WHEN hour like '6' or hour like '7' THEN '6-7'
        WHEN hour like '8' or hour like '9' THEN '8-9'
        WHEN hour like '10' or hour like '11' THEN '10-11'
        WHEN hour like '12' or hour like '13' THEN '12-13'
        WHEN hour like '14' or hour like '15' THEN '14-15'
        WHEN hour like '16' or hour like '17' THEN '16-17'
        WHEN hour like '18' or hour like '19' THEN '18-19'
        WHEN hour like '20' or hour like '21' THEN '20-21'
        WHEN hour like '22' or hour like '23' THEN '22-23'

    END AS hour_group


    FROM df_hourly
    WHERE ID_Utente like 'ID202206'
    GROUP BY  hour_group, ID_Utente, stabilimento, mese
    """
radar_chart_2_df = ps.sqldf(radar_chart_2_query, locals())





#2 - LINEBAR MONTHLY DATASE
#---------------
linebar_monthly_query = '''
SELECT anno, mese, fascia_oraria, stabilimento, ROUND(SUM(consumi_kw_h), 2) as consumi_kw_h
FROM df_hourly
GROUP BY mese, anno, fascia_oraria, stabilimento
'''
linebar_monthly_df = ps.sqldf(linebar_monthly_query, locals())





PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
button = dbc.Row([
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0,
                href='https://dashcheatsheet.pythonanywhere.com/',
            ),
            width="auto",
        ),
    ], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", align="center",)
navbar = dbc.Navbar(dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand("CER Profilo 2", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                button,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),]), color="#111111", dark=True,)
range_slider = dcc.RangeSlider(id='_RangeSlider_months_',
                                min=1,
                                max=12,
                                step=None,
                                marks={1: 'gen', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'mag', 6: 'giu', 7: 'lug', 8: 'ago',
                                       9: 'set', 10: 'ott', 11: 'nov', 12: 'dic'},
                                value=[1, 2, 3],
                                className='form-label'
                                )


#               !!!LAYOUT SPACE!!!
app.layout = dbc.Container([
    html.Div(id = 'parent', children = [navbar]),
    html.Nav(id='nav', className='menu'),
    html.Br(),
    dbc.Col([
        dbc.Row([
            dbc.Col([
                html.Br(),
                dcc.Dropdown(
                        id='_dropdown_stabilimento_',
                        multi=True,
                        options=[{'label': stabilimento, 'value': stabilimento} for stabilimento in radar_chart_stab_dropdown_options],
                        value=['Frigo', 'Pozzo Conte', 'Pozzo di casa'],
                        placeholder='Select Profile',
                        style={'color':'blue',
                               'background-color':'#111111',
                               'background':'#111111'}),
                html.Br(),
                dcc.Dropdown(
                    id='_dropdown_anno_',
                    multi=True,
                    options=[2021, 2022],
                    value=[2021, 2022],
                    placeholder='Select Year',
                    style={'color': 'blue',
                           'background-color': '#111111',
                           'background': '#111111'}),

                html.Br(),
                dcc.Dropdown(
                    id='_dropdown_fascia_oraria_',
                    multi=True,
                    options=['F1', 'F2', 'F3'],
                    value=['F1', 'F2', 'F3'],
                    placeholder='Select Hour Slot',
                    style={'color': 'blue',
                           'background-color': '#111111',
                           'background': '#111111'}),


            ],xl=3, lg=3, md=3, sm=3, xs=3, style={'background-color':'#111111'}),

            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card(id='summary_f1', children=[], body=True, style={'background-color': '#111111',
                                                                                 'text-align':'center'})],
                        xl=4, lg=4, md=4, sm=4, xs=4),
                    dbc.Col([
                        dbc.Card(id='summary_f2', children=[], body=True, style={'background-color': '#111111',
                                                                                 'text-align':'center'})],
                        xl=4, lg=4, md=4, sm=4, xs=4),
                    dbc.Col([
                        dbc.Card(id='summary_f3', children=[], body=True, style={'background-color': '#111111',
                                                                                 'text-align':'center'})],
                        xl=4, lg=4, md=4, sm=4, xs=4),
                    dbc.Row([
                        dbc.Col([dcc.Graph(id='linebar_chart')])
                            ], style={'margin-top':'10px'})
                        ])
                    ])
        ],),
    ]),
    #dbc.Row([
     #   dbc.Col([dcc.Graph(id='graph_radar_weekdays')], xl=6, lg=6, md=6, sm=6, xs=6),
      #  dbc.Col([dcc.Graph(id='graph_radar_month')], xl=6, lg=6, md=6, sm=6, xs=6),
    #], style= {'margin-top':'20px', 'margin-bot':'10px', 'height':'auto'}),
    #dbc.Row([
     #   dbc.Col([dcc.Graph(id='linebar_monthly')], xl=12, lg=12, md=12, sm=12, xs=12)
    #],style= {'margin-top':'20px', 'margin-bot':'10px', 'margin-right':'3px'})


], fluid=True)


#                                    !!!CALLBACK SPACE!!!
#_____________________________________________________________________________________________
#0- NUMBER CARDS CALLBACK
@app.callback([Output('summary_f1', 'children'),
               Output('summary_f2', 'children'),
               Output('summary_f3', 'children')],
              Input('_dropdown_stabilimento_', 'value'))

def update_number_cards(value):
    filtered_data = cards_df[cards_df["stabilimento"].isin(value)]

    f1_list = ['F1']
    f1_ds = filtered_data[filtered_data["fascia_oraria"].isin(f1_list)]
    f1_sum = f1_ds['consumi_kw_h'].sum()

    f2_list = ['F2']
    f2_ds = filtered_data[filtered_data["fascia_oraria"].isin(f2_list)]
    f2_sum = f2_ds['consumi_kw_h'].sum()

    f3_list = ['F3']
    f3_ds = filtered_data[filtered_data["fascia_oraria"].isin(f3_list)]
    f3_sum = f3_ds['consumi_kw_h'].sum()

    output_f1 = html.H5([f'🔵      CONSUMI F1', html.Br(),f'{f1_sum}'])
    output_f2 = html.H5([f'🔵      CONSUMI F2', html.Br(), f'{f2_sum}'])
    output_f3 = html.H5([f'🔵      CONSUMI F3', html.Br(), f'{f3_sum}'])
    return output_f1, output_f2, output_f3

#1- LINE CALLBACK
@app.callback(
Output('linebar_chart', 'figure'),
    [Input('_dropdown_stabilimento_', 'value'),
     Input('_dropdown_fascia_oraria_', 'value'),
     Input('_dropdown_anno_', 'value')
     #Input('_RangeSlider_months_', 'value')
     ]
)
def update_linebar_chart(value_1, value_2, value_3):
    filtered_data_1 = linebar_df[linebar_df["stabilimento"].isin(value_1)]
    filtered_data_2 = filtered_data_1[filtered_data_1['fascia_oraria'].isin(value_2)]
    filtered_data_3 = filtered_data_2[filtered_data_2['anno'].isin(value_3)]
    #filtered_data_4 = filtered_data_3[filtered_data_3['mese'].isin(value_4)]

    fig = px.bar(filtered_data_3, x='date', y='consumi_kw_h',
                 hover_data=['consumi_kw_h', 'fascia_oraria'], color='stabilimento',
                 color_discrete_sequence=['#0d47a1', '#2962ff', '#e3f2fd'],
                 custom_data=['stabilimento', 'fascia_oraria', 'anno'],
                 labels={'consumi_kw_h': 'Consumi in KW/h',
                         'fascia_oraria': 'Fascia Oraria'},

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

#----------------------------------------------------


#----------------------------------------------------



#----------------------------------------------------





#                 !!!RUNNING!!!
#========================
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)
