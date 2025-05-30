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
        value=['Bern/CHE'],
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
        value=[PM2_5, PM10, NO2],
        placeholder="Select pollutants"
    )

def create_country_dropdown(data):
    countries = sorted(data['Country'].unique())
    return dcc.Dropdown(
        id = 'country-dropdown',
        options=[{'label': c, 'value': c} for c in countries],
        placeholder="Select Country:"
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

def create_time_range_forMax(min_year,max_year):
    return dcc.RangeSlider(
        id='year-slider_max',
        min=min_year,
            max=max_year,
            step=1,
            value=[min_year, max_year],
            marks={str(year): str(year) for year in range(min_year, max_year + 1, 5)}
    )

def update_pollution_plot(filtered_df : pd.DataFrame, selected_pollutants, selected_cities):
    if not selected_cities or not selected_pollutants:
        return px.line(title="Please select at least one city and one pollutant")
        
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

def update_max_val_div(filtered_df : pd.DataFrame, selected_pollutants, selected_country, year_range_max):
    #calculate Max-Values in given Country/Years
    max_value_descriptions = []
    start_year, end_year = year_range_max
    country_filtered_df = filtered_df[
        (filtered_df['Country'] == selected_country) &
        (filtered_df['Year'] >= start_year) &
        (filtered_df['Year'] <= end_year)
    ]
    for pollutant in selected_pollutants:
        if country_filtered_df[pollutant].isna().all():
            max_value_descriptions.append(f'No data available for {pollutant} in the selected filters')
        else:
            max_val = country_filtered_df[pollutant].max()
            #max_city = country_filtered_df['City'][filtered_df[pollutant].idxmax()]
            max_year = filtered_df['Year'][filtered_df[pollutant].idxmax()]
            max_value_descriptions.append(f'Max {pollutant}: {max_val} µg/m³ in ({max_year})')
    
    if not max_value_descriptions:
        return html.Div("No data available for the selected filters")
    return html.Div([html.P(val) for val in max_value_descriptions]) 


def update_country_pollution_plot(filtered_df: pd.DataFrame, selected_pollutants, selected_country, year_range):
    if not selected_country or not selected_pollutants:
        return px.line(title="Please select a country and pollutants")

    fig = go.Figure()
    dashes = {
        PM2_5: 'dot',
        PM10: 'dash',
        NO2: 'solid'
    }

    colors = plotly.colors.qualitative.Plotly
    start_year, end_year = year_range
    country_df = filtered_df[(filtered_df['Country'] == selected_country) & (filtered_df['Year'] >= start_year) & (filtered_df['Year'] <= end_year)]

    # Durchschnitt je Jahr berechnen
    avg_df = country_df.groupby('Year')[selected_pollutants].mean().reset_index()

    for pollutant, color in zip(selected_pollutants, colors):
        fig.add_trace(go.Scatter(
            x=avg_df['Year'],
            y=avg_df[pollutant],
            mode='lines+markers',
            name=pollutant,
            line={'dash': dashes[pollutant], 'color': color}
        ))

    fig.update_layout(
        title=f'Average Air Pollution in {selected_country}',
        xaxis_title='Year',
        yaxis_title='Average Concentration (µg/m³)',
        legend_title='Pollutants',
        transition_duration=500
    )
    return fig

def create_dashboard(data : pd.DataFrame) -> Dash:
    """
    Creates a dashboard app from the given data.
    The data is expected to be a pandas DataFrame, formatted as per the WHO air quality database.
    The dashboard will be created using the Dash framework.
    """
    app = Dash()
    app.layout = html.Div([
        html.H1('Air Quality Dashboard'),
        html.Div('Select one or more cities to see PM2.5 trends over time:'),
        create_city_dropdown(data),
        html.Div('Select one or more pollutants to display:'),
        create_pollutant_dropdown(),
        html.Div('Select a year-range to display:'),
        create_time_range(data['Year'].min(), data['Year'].max()),
        dcc.Graph(id='pm25-trend'),
        html.Hr(),
        html.Div('Select a country for which to display the max-values'),
        create_country_dropdown(data),
        html.Div('Select years for Max Values: '),
        create_time_range_forMax(data['Year'].min(), data['Year'].max()),
        dcc.Graph(id='country-trend'),
        html.Div(id='max-values'),
        html.Hr(),
        html.Div('Raw data preview:'),
        dash_table.DataTable(data.to_dict('records'), page_size=10)
    ])

    @app.callback(
        [dash.Output('pm25-trend', 'figure'), dash.Output('max-values', 'children'),dash.Output('country-trend', 'figure')],
        dash.Input('city-dropdown', 'value'),
        dash.Input('pollutant-dropdown', 'value'),
        dash.Input('year-slider', 'value'),
        dash.Input('year-slider_max', 'value'),
        dash.Input('country-dropdown', 'value')
    )
    def update_filters(selected_cities, selected_pollutants, year_range,year_range_max, selected_country):
        """
        Update the graph and max value display based on selected filters.
        """
        
        start_year, end_year = year_range
        filtered_df = data[(data['City'].isin(selected_cities)) & (data['Year'] >= start_year) & (data['Year'] <= end_year)]

        country_filtered_df = data[data['Country']==(selected_country)]
        
        fig = update_pollution_plot(filtered_df, selected_pollutants, selected_cities)
        max_val_div = update_max_val_div(country_filtered_df, selected_pollutants, selected_country, year_range_max)
        country_fig = update_country_pollution_plot(data, selected_pollutants, selected_country, year_range_max)

        return fig, max_val_div, country_fig
    
    return app
