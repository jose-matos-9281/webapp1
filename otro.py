
from dash import Dash, html,dcc,Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt

app = Dash(__name__)
server = app.server
app.layout = html.H1("hola mundo")

if __name__ == '__main__':
    app.run()