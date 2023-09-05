import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Dash, Input, Output

# Cargar datos
df1 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(1)+'_ctrl2.csv', na_values=[999, -999, -888, 888,-880])
umb_s1 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(1)+'.csv')
umb_s1a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(1)+'.csv')

df2 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(2)+'_ctrl2.csv', na_values=[999, -999, -888, 888,-880])
umb_s2 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(2)+'.csv')
umb_s2a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(2)+'.csv')

df3 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(3)+'_ctrl2.csv', na_values=[999, -999, -888, 880,-880])
umb_s3 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(3)+'.csv')
umb_s3a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(3)+'.csv')

df4 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(4)+'_ctrl2.csv', na_values=[999, -999, -888, 880,-880])
umb_s4 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(4)+'.csv')
umb_s4a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(4)+'.csv')

df5 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(5)+'_ctrl2.csv', na_values=[999, -999, -888, 880,-880])
umb_s5 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(5)+'.csv')
umb_s5a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(5)+'.csv')

df6 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(6)+'_ctrl2.csv', na_values=[999, -999, -888, 880,-880])
umb_s6 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(6)+'.csv')
umb_s6a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(6)+'.csv')

df7 = pd.read_csv(r'C:\\Users\\Andy\\Downloads\\DATOS/dt_zn_'+str(7)+'_ctrl2.csv', na_values=[999, -999, -888, 880,-880])
umb_s7 = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs2_zn'+str(7)+'.csv')
umb_s7a = pd.read_csv(r'C:\Users\Andy\Downloads\DATOS/umbs3_zn'+str(7)+'.csv')

# Definir nombres de variables
variables = ['P_TMAX', 'P_TMIN', 'P_TS7', 'P_TS13', 'P_TS19', 'P_TH7', 'P_TH13',  'P_TH19', 'P_PP7',  'P_PP19']
variables2 = ['Nacional_TMAX', 'Nacional_TMIN', 'Nacional_TS7', 'Nacional_TS13', 'Nacional_TS19', 'Nacional_TH7',
              'Nacional_TH13', 'Nacional_TH19', 'Nacional_PP7', 'Nacional_PP19']
var = ['N_TM102', 'N_TM103', 'N_TM104', 'N_TM105', 'N_TM106', 'N_TM107', 'N_TM108', 'N_TM109', 'N_PT102', 'N_PT103']

# Procesar datos
def process_data(df, variable, variables2, var):
    vacio = []
    for j in range(10):
        df_b = df[(df[variable[j]] == 'B') & (df[variables2[j]] == 'B')]
        df_b = df_b.dropna(subset=[var[j]])
        vacio.append([df_b[df_b['V_MES'] == i][var[j]] for i in range(1, 13)])
    return vacio

sector_data = {
    'Sector1': process_data(df1, variables, variables2, var),
    'Sector2': process_data(df2, variables, variables2, var),
    'Sector3': process_data(df3, variables, variables2, var),
    'Sector4': process_data(df4, variables, variables2, var),
    'Sector5': process_data(df5, variables, variables2, var),
    'Sector6': process_data(df6, variables, variables2, var),
    'Sector7': process_data(df7, variables, variables2, var)
    # Agregar más sectores si es necesario
}

# Datos de umbrales para varios sectores
thresholds = {
    'Sector1': umb_s1,
    'Sector2': umb_s2,
    'Sector3': umb_s3,
    'Sector4': umb_s4,
    'Sector5': umb_s5,
    'Sector6': umb_s6,
    'Sector7': umb_s7
    # Agregar más sectores si es necesario
}

thresholds2 = {
    'Sector1': umb_s1a,
    'Sector2': umb_s2a,
    'Sector3': umb_s3a,
    'Sector4': umb_s4a,
    'Sector5': umb_s5a,
    'Sector6': umb_s6a,
    'Sector7': umb_s7a
    # Agregar más sectores si es necesario
}
def generate_figures(sector, variables, vacio, thresholds,thresholds2):
    figures = []
    for i, variable in enumerate(variables):
        fig_month = go.Figure()
        xticks = [f'Mes {j + 1}' for j in range(12)]
        for j in range(12):
            b = 0 + 12 * i
            c = 12 + 12 * i
            fig_month.add_trace(go.Box(y=vacio[i][j], name=f'Mes {j + 1}'))

            # Agregar líneas de umbrales
            fig_month.add_trace(go.Scatter(x=xticks, y=thresholds['lb_kme_inf'][b:c], mode='lines', name='LB - K-Means',
                                           legendgroup='kmeans', line=dict(color='#17202A')))
            fig_month.add_trace(go.Scatter(x=xticks, y=thresholds['lb_kme_sup'][b:c], mode='lines', name='LB - K-Means',
                                           legendgroup='kmeans', line=dict(color='#17202A')))

            fig_month.add_trace(
                go.Scatter(x=xticks, y=thresholds2['ld_new_i'][b:c], mode='lines', name='LD - Nuevo', legendgroup='New',
                           line=dict(color='#631302')))
            fig_month.add_trace(
                go.Scatter(x=xticks, y=thresholds2['ld_new_s'][b:c], mode='lines', name='LD - Nuevo', legendgroup='New',
                           line=dict(color='#631302')))

        fig_month.update_layout(
            title=f'Diagrama de Cajas - {variable} por Mes',
            xaxis=dict(title='Mes'),
            yaxis=dict(title='Valor'),
            showlegend=True
        )

        figures.append(fig_month)

    return figures

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Diagramas de Cajas por Mes y por Año'),

    html.Div(children=[
        dcc.Dropdown(
            id='sector-dropdown',
            options=[{'label': sector, 'value': sector} for sector in sector_data.keys()],
            value='Sector1'
        ),
        dcc.Dropdown(
            id='variable-dropdown',
            options=[{'label': variable, 'value': i} for i, variable in enumerate(variables)],
            value=0
        )
    ]),

    html.Div(children=[
        dcc.Graph(id='graph-month', config={'displayModeBar': False}),
    ])
])

@app.callback(
    Output('graph-month', 'figure'),
    [Input('sector-dropdown', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_graph_month(selected_sector, selected_variable):
    return sector_figures[selected_sector][selected_variable]

if __name__ == '__main__':
    # Generar gráficos para varios sectores
    sector_figures = {}
    for sector, data in sector_data.items():
        sector_figures[sector] = generate_figures(sector, variables, data, thresholds[sector],thresholds2[sector])

    # Ejecutar la aplicación
    app.run_server(debug=True)
