import pandas as pd
from dash import Dash, html, dash_table
import plotly.express as px
from dash import dcc, Input, Output


PM2_5 = 'PM2.5 (µg/m³)'
PM10 = 'PM10 (µg/m³)'
NO2 = 'NO₂ (µg/m³)'

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
                {'label': PM2_5, 'value': PM2_5},
                {'label': PM10,  'value': PM10},
                {'label': NO2,   'value': NO2}
            ],
            multi=True,
            value=[PM2_5],  # default selection
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
        import plotly.colors
        
        fig = go.Figure()
        
        # Use a dictionary for consistent mapping of pollutants to line styles
        dashes = {
            PM2_5 : 'dot',
            PM10  : 'dash',
            NO2   : 'solid'
        }
        colors = plotly.colors.qualitative.Plotly

        for pollutant in selected_pollutants:
            for city, color in zip(selected_cities, colors):
                city_data = filtered_df[filtered_df['City'] == city]
                fig.add_trace(go.Scatter(
                    x=city_data['Year'],
                    y=city_data[pollutant],
                    mode='lines+markers',
                    showlegend=False,
                    line={'dash' : dashes[pollutant], 'color' : color}
                ))
        
        # Add one trace per pollutant for legend (dash only)
        for pollutant in selected_pollutants:
            fig.add_trace(go.Scatter(
                x=[None], y = [None], # Placeholder for legend
                mode='lines',
                name=f'Pollutant : {pollutant}',
                line={'dash': dashes[pollutant], 'color': 'gray'},
            ))

        # Add one trace per city for legend (color only)
        for city, color in zip(selected_cities, colors):
            fig.add_trace(go.Scatter(
                x=[None], y = [None], # Placeholder for legend
                mode='lines',
                name=f'City : {city}',
                line={'dash': 'solid', 'color': color},
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

