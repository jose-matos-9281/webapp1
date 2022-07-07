
from dash import Dash, html,dcc,Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt


serie = [ 'Confirmados', 'Fallecidos', 'Muestras', 'Recuperados']
provincias = ['Azua', 'Baoruco', 'Barahona', 'Dajabón', 'Distrito Nacional', 'Duarte',
       'El Seibo', 'Elías Piña', 'Espaillat', 'Hato Mayor', 'Hermanas Mirabal',
       'Independencia', 'La Altagracia', 'La Romana', 'La Vega',
       'María Trinidad Sánchez', 'Monseñor Nouel', 'Monte Cristi',
       'Monte Plata', 'Pedernales', 'Peravia', 'Puerto Plata', 'RD', 'Samaná',
       'San Cristóbal', 'San José de Ocoa', 'San Juan', 'San Pedro de Macorís',
       'Santiago', 'Santiago Rodríguez', 'Santo Domingo', 'Sánchez Ramírez',
       'Valverde']

app = Dash(__name__)
server = app.server
app.layout = html.Div( children=[
    html.H1(children='hello Dash'),
    html.H4(children='US Agriculture Exports (2011)'),
    html.Div([
        html.Label('Serie'),
        dcc.RadioItems( serie, 'Confirmados',id='serie',style={'padding': 10, 'flex': 1}),
        html.Br(),
        html.Label('Provincias'),
        dcc.Dropdown( provincias, 'RD', id ='provincia', multi = True)
         ]),
    
    html.Div(id='tabla')
    
])

if __name__ == '__main__':
    app.run()