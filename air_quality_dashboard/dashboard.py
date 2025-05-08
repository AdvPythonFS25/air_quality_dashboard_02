"""
This module creates a Dash-based dashboard for visualizing air quality data.
"""
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors

PM2_5 = 'PM2.5 (µg/m³)'
PM10 = 'PM10 (µg/m³)'
NO2 = 'NO₂ (µg/m³)'



def create_city_dropdown(data):
    cities = sorted(data['City'].unique())
    return dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': c, 'value': c} for c in cities],
        multi=True,
        placeholder="Select cities"
    )


def create_pollutant_dropdown():
    return dcc.Dropdown(
        id='pollutant-dropdown',
        options=[
            {'label': PM2_5, 'value': PM2_5},
            {'label': PM10,  'value': PM10},
            {'label': NO2,   'value': NO2}
        ],
        multi=True,
        value=[PM2_5],
        placeholder="Select pollutants"
    )

def create_time_range(min_year,max_year):
    
    return dcc.RangeSlider(
        id='year-slider',
        min=min_year,
            max=max_year,
            step=1,
            value=[min_year, max_year],
            marks={str(year): str(year) for year in range(min_year, max_year + 1, 5)}
    )


def create_dashboard(data : pd.DataFrame) -> Dash:
    """
    Creates a dashboard app from the given data.
    The data is expected to be a pandas DataFrame, formatted as per the WHO air quality database.
    The dashboard will be created using the Dash framework.
    """
    app = Dash()
    app.layout = html.Div([
        html.H1('Air Quality Dashboard'),
        html.Div('Select one or more countries to see PM2.5 trends over time:'),
        create_city_dropdown(data),
        html.Div('Select one or more pollutants to display:'),
        create_pollutant_dropdown(),
        html.Div('Select a year-range to display:'),
        create_time_range(data['Year'].min(), data['Year'].max()),
        dcc.Graph(id='pm25-trend'),
        html.Hr(),
        html.Div('Raw data preview:'),
        dash_table.DataTable(data.to_dict('records'), page_size=10)
    ])

    @app.callback(
        dash.Output('pm25-trend', 'figure'),
        dash.Input('city-dropdown', 'value'),
        dash.Input('pollutant-dropdown', 'value'),
        dash.Input('year-slider', 'value')
    )
    def update_pollution_plot(selected_cities, selected_pollutants, year_range):
        if not selected_cities or not selected_pollutants:
            return px.line(title="Please select at least one city and one pollutant")
        
        start_year, end_year = year_range
        filtered_df = data[(data['City'].isin(selected_cities)) & (data['Year'] >= start_year) & (data['Year'] <= end_year)]
        fig = go.Figure()

        dashes = {
            PM2_5: 'dot',
            PM10: 'dash',
            NO2: 'solid'
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
                    line={'dash': dashes[pollutant], 'color': color}
                ))

        for pollutant in selected_pollutants:
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='lines',
                name=f'Pollutant : {pollutant}',
                line={'dash': dashes[pollutant], 'color': 'gray'},
            ))

        for city, color in zip(selected_cities, colors):
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
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
