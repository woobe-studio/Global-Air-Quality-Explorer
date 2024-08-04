import dash
from dash import dcc
from dash import html
import plotly.express as px
from app import create_app

server = create_app()

app = dash.Dash(server=server, routes_pathname_prefix='/dash/')

app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure=px.line(x=[1, 2, 3], y=[4, 5, 6], title='Example Chart')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
