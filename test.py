import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Crear la aplicación de Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1("Ejemplo de Dash"),
    dcc.Input(id="input-text", type="text", value=""),
    html.Div(id="output-text"),
    dcc.Graph(id="bar-chart")
])

# Definir una función de actualización para el gráfico
@app.callback(
    Output("bar-chart", "figure"),
    [Input("input-text", "value")]
)
def update_chart(input_text):
    # Aquí podrías realizar algún procesamiento con input_text y obtener los datos para el gráfico
    # En este ejemplo, simplemente generaremos un gráfico de barras con datos ficticios
    data = {
        "x": ["A", "B", "C", "D"],
        "y": [10, 5, 8, 12],
        "type": "bar",
        "name": "Ejemplo"
    }
    return {"data": [data], "layout": {"title": "Gráfico de Barras"}}

# Definir una función de actualización para el texto
@app.callback(
    Output("output-text", "children"),
    [Input("input-text", "value")]
)
def update_text(input_text):
    return f"Texto ingresado: {input_text}"

if __name__ == "__main__":
    app.run_server(debug=True)