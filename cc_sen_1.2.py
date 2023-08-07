import dash
from dash import  dcc,  html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_table
import plotly.graph_objects as go

# Crear una instancia de la aplicación Dash
app = dash.Dash(__name__)

# Cargar los datos desde tu DataFrame (reemplaza 'data.csv' con la ubicación de tus datos)
df = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/cc_td_zn.csv')

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1('Visualizador de Datos'),

    # Filtros
    html.Label('Filtro por var:'),
    dcc.Dropdown(
        id='var-filter',
        options=[{'label': var, 'value': var} for var in df['var'].unique()],
        value=df['var'].unique()[0]
    ),

    html.Label('Filtro por Sector:'),
    dcc.Dropdown(
        id='sector-filter',
        options=[{'label': sector, 'value': sector} for sector in df['Sector'].unique()],
        value=df['Sector'].unique()[0]
    ),

    # Tabla
    html.H3('Tabla de Datos'),
    dash_table.DataTable(
        id='filtered-table',
        columns=[ {'name': col, 'id': col} for col in df.columns if col not in ['var', 'Sector']],
        style_table={'height': '300px', 'overflowY': 'auto'},
        page_size=10
    ),

    # Gráfica de barras
    dcc.Graph(id='bar-chart')
])


# Actualizar la tabla y la gráfica en función de los filtros
@app.callback(
    [Output('filtered-table', 'data'),
     Output('bar-chart', 'figure')],
    [Input('var-filter', 'value'),
     Input('sector-filter', 'value')]
)
def update_displayed_data(selected_var, selected_sector):
    filtered_df = df[(df['var'] == selected_var) & (df['Sector'] == selected_sector)]

    # Actualizar la gráfica de barras
    bar_chart = go.Figure(data=[go.Bar(x=filtered_df['BBDD'] + ' ' + filtered_df['Recontrol'], y=filtered_df['Porcentaje (%)'],
                                       hovertext=filtered_df['Porcentaje (%)'].apply(lambda x: f'{x:.2f}%'))])

    return filtered_df.to_dict('records'), bar_chart


if __name__ == '__main__':
    app.run_server(debug=True)