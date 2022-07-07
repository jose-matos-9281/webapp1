# importar librerias

from distutils.log import debug
from itertools import count
from msilib.schema import Component
from dash import Dash, html,dcc,Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt

# funciones definidas
def num(data,col):
    '''
    limpia la data numerica que tiene un caracter extra '-1
    '''
    for i in col:
        data[i]= data[i].str.replace("'","").astype("int32")
    return data

def data_pivot(data,serie):
    '''
    dado un dataframe crea la serie de tiempo por provincias, segun el parametro solicitado
    '''
    Frame = data.pivot_table(
        index = "fecha",
        columns = 'Provincia',
        values = serie
    )
    return Frame

#Filtra cuales provincias seran usadas
filtro_P = lambda data,prov: data[data.Provincia.isin(prov)]

#Filtra la data por un periodo especifico de tiempo
def filtro_F (data,inicio = dt.datetime(2020,3,19), fin = dt.datetime(2022,7,3)): 
    return data[[data['fecha']>= inicio] and [data['fecha'] <= fin][0]]



def diferencia(serie):
    '''
    dada una serie de tiempo obtiene la serie con la diferencia de valore entre cada periodo
    '''
    a = [serie[0]]
    for i in range(1,len(serie)):
        a.append(serie[i]-serie[i-1])
    return a

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# lectura de los datos

hosp = pd.read_csv('data/hospitalizacion.csv')
data = pd.read_csv('data/data.csv')

# limpieza de los datos
data['fecha']= pd.to_datetime(data['fecha'])
data = num(data,['Confirmados', 'Fallecidos', 'Muestras','Recuperados'])
hosp['fecha']= pd.to_datetime(hosp['fecha'])

#lista de series
serie = [ 'Confirmados', 'Fallecidos', 'Muestras', 'Recuperados']
provincias = ['Azua', 'Baoruco', 'Barahona', 'Dajabón', 'Distrito Nacional', 'Duarte',
       'El Seibo', 'Elías Piña', 'Espaillat', 'Hato Mayor', 'Hermanas Mirabal',
       'Independencia', 'La Altagracia', 'La Romana', 'La Vega',
       'María Trinidad Sánchez', 'Monseñor Nouel', 'Monte Cristi',
       'Monte Plata', 'Pedernales', 'Peravia', 'Puerto Plata', 'RD', 'Samaná',
       'San Cristóbal', 'San José de Ocoa', 'San Juan', 'San Pedro de Macorís',
       'Santiago', 'Santiago Rodríguez', 'Santo Domingo', 'Sánchez Ramírez',
       'Valverde']

# aplicacion Dash
app = Dash(__name__)


#Creacion de la estructura de la pagina 
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

#Creacion de callbacks, o llamadas
@app.callback(
    Output('tabla','children'),
    Input('serie','value'),
    Input('provincia','value')
)
def update_table(serie, provincia):
    provincia = [provincia] if type(provincia) == str else provincia
    frame = filtro_P(data,provincia)
    frame = data_pivot(frame,serie).cumsum()
    frame.insert(0,'fechas', frame.index)
    frame['fechas'] = frame.fechas.dt.strftime('%d/%m/%Y')
    return generate_table(frame,20)

# correr servidor
if __name__ == '__main__':
    app.run_server(debug= True)