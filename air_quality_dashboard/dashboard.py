import pandas as pd
from dash import Dash, html, dash_table
import plotly.express as px
from dash import dcc, Input, Output


def create_dashboard(data : pd.DataFrame) -> Dash:
    """
    Creates a dashboard app from the given data.
    The data is expected to be a pandas DataFrame, formatted as per the WHO air quality database.
    The dashboard will be created using the Dash framework.
    """
    app = Dash()
    app.layout = html.Div([

        html.H1('Air Quality Dashboard'), # Title
        html.Div('Select one or more countries to see PM2.5 trends over time:'), # Instructions-Text

        # Dropdown for selecting one or more cities
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(data['City'].unique())],
            multi=True,
            placeholder="Select cities"
        ),

        # Dropdown for selecting pollutants
        html.Div('Select one or more pollutants to display:'),
        dcc.Dropdown(
            id='pollutant-dropdown',
            options=[
                {'label': 'PM2.5 (µg/m³)', 'value': 'PM2.5 (µg/m³)'},
                {'label': 'PM10 (µg/m³)',  'value': 'PM10 (µg/m³)'},
                {'label': 'NO₂ (µg/m³)',   'value': 'NO₂ (µg/m³)'}
            ],
            multi=True,
            value=['PM2.5 (µg/m³)'],  # default selection
            placeholder="Select pollutants"
        ),

        dcc.Graph(id='pm25-trend'),

        html.Hr(),

        # Data preview table for context
        html.Div('Raw data preview:'),
        dash_table.DataTable(data.to_dict('records'), page_size=10)
    ])

    @app.callback(
        Output('pm25-trend', 'figure'),
        Input('city-dropdown', 'value'),
        Input('pollutant-dropdown', 'value')
    )
    def update_pollution_plot(selected_cities, selected_pollutants):
        if not selected_cities or not selected_pollutants:
            return px.line(title="Please select at least one city and one pollutant")

        # Filter data to selected countries
        filtered_df = data[data['City'].isin(selected_cities)]

        # Create one plot with one trace per pollutant
        import plotly.graph_objects as go
        fig = go.Figure()

        for pollutant in selected_pollutants:
            for city in selected_cities:
                city_data = filtered_df[filtered_df['City'] == city]
                fig.add_trace(go.Scatter(
                    x=city_data['Year'],
                    y=city_data[pollutant],
                    mode='lines+markers',
                    name=f'{pollutant} - {city}'
                ))

        fig.update_layout(
            title='Air Pollution Trends Over Time',
            xaxis_title='Year',
            yaxis_title='Concentration (µg/m³)',
            legend_title='Pollutant & Country',
            transition_duration=500
        )

        return fig

    return app