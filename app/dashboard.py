import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
from app import create_app

# Create the Flask server instance
server = create_app()

# Create Dash app instance
app = dash.Dash(
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
    ]
)

# Load GeoJSON data for U.S. states
with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    states = json.load(response)

# Use the 'name' property for state names as the 'id' in GeoJSON
for feature in states['features']:
    feature['id'] = feature['properties']['name']

# Create mock air pollution data (Replace this with real data)
data = {
    "State": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
    "PM2.5": [7.5, 5.4, 8.2, 6.1, 12.3, 6.5, 5.6, 7.1, 9.4, 8.9, 4.2, 6.7, 8.3, 7.8, 6.9, 7.2, 8.5, 7.3, 4.9, 7.6, 6.0, 8.1, 5.7, 7.9, 8.0, 4.8, 6.3, 5.9, 5.1, 7.0, 5.3, 6.8, 7.4, 5.5, 7.7, 8.6, 6.4, 8.8, 6.6, 7.7, 5.2, 8.4, 9.8, 4.7, 4.3, 7.1, 8.7, 7.2, 7.9, 5.0],
    "PM10": [12.5, 9.4, 11.2, 8.1, 15.3, 10.5, 7.6, 11.1, 14.4, 10.9, 6.2, 9.7, 12.3, 11.8, 9.9, 10.2, 11.5, 10.3, 7.9, 11.6, 9.0, 11.1, 8.7, 10.9, 11.0, 7.8, 9.3, 7.9, 8.1, 10.0, 7.3, 10.8, 10.4, 8.5, 10.7, 12.6, 10.4, 12.8, 10.6, 11.7, 8.2, 10.4, 12.8, 7.7, 6.3, 11.1, 12.7, 10.2, 11.9, 7.0],
    "O3": [35.5, 28.4, 32.2, 29.1, 40.3, 30.5, 27.6, 31.1, 34.4, 31.9, 23.2, 30.7, 32.3, 33.8, 31.9, 30.2, 33.5, 30.3, 24.9, 31.6, 28.0, 30.1, 29.7, 30.9, 32.0, 25.8, 28.3, 26.9, 25.1, 31.0, 27.3, 29.8, 32.4, 25.5, 33.7, 34.6, 30.4, 34.8, 29.6, 31.7, 26.2, 31.4, 34.8, 25.7, 23.3, 30.1, 34.7, 31.2, 32.9, 26.0]
}
df = pd.DataFrame(data)

# Function to create choropleth map
def create_map(pollutant='PM2.5'):
    fig = px.choropleth(
        df,
        geojson=states,
        locations='State',
        color=pollutant,
        color_continuous_scale="Blues",
        scope="usa",  # Limits the map to the United States
        labels={pollutant: f'{pollutant} Levels'},
        title=f'{pollutant} Levels by State in the USA'
    )

    # Update layout for a cleaner look
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='#f5f5f5',  # Light background color
        plot_bgcolor='#ffffff',
        font_color='#333333',  # Dark text color for contrast
        title_font_size=24,
        coloraxis_colorbar=dict(
            title=f'{pollutant} Levels',
            tickvals=[df[pollutant].min(), df[pollutant].max()],
            ticktext=[f'{df[pollutant].min()}', f'{df[pollutant].max()}']
        )
    )

    return fig

# Define app layout
app.layout = html.Div(
    style={'backgroundColor': '#f5f5f5', 'color': '#333333', 'padding': '20px'},
    children=[
        html.H1('Global Air Quality Dashboard', style={'textAlign': 'center', 'marginBottom': '20px'}),
        html.Div([
            html.Label('Select Pollutant', style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='pollutant-dropdown',
                options=[
                    {'label': 'PM2.5', 'value': 'PM2.5'},
                    {'label': 'PM10', 'value': 'PM10'},
                    {'label': 'O3', 'value': 'O3'}
                ],
                value='PM2.5',
                style={'width': '250px', 'display': 'inline-block'}
            )
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
        dcc.Graph(
            id='us-air-pollution-map'
        )
    ]
)

# Update the graph based on user selection
@app.callback(
    Output('us-air-pollution-map', 'figure'),
    [Input('pollutant-dropdown', 'value')]
)
def update_map(selected_pollutant):
    return create_map(selected_pollutant)

if __name__ == '__main__':
    app.run_server(debug=True)
