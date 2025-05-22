import pandas as pd
from dash import html
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dashboard import update_max_val_div, PM2_5, PM10, NO2

import dashboard  

#Tests the normal ("good") case of update_max_val
def test_max_val_div_normal_case():
    data = pd.DataFrame({
        'Country': ['Switzerland', 'Switzerland', 'Switzerland'],
        'Year': [2018, 2019, 2020],
        PM2_5: [10, 20, 15],
        PM10: [30, 25, 35],
        NO2: [5, 10, 7]
    })
    result = update_max_val_div(data, [PM2_5, PM10, NO2], 'Switzerland', [2018, 2020])
    assert isinstance(result, html.Div)
    assert len(result.children) == 3
    assert "Max PM2.5" in result.children[0].children

#tests the "bad" case where there is no Data available
def test_max_val_div_nan_pollutant():
    data = pd.DataFrame({
        'Country': ['Switzerland', 'Switzerland'],
        'Year': [2019, 2020],
        PM2_5: [None, None],
        PM10: [22, 28],
        NO2: [11, 14]
    })
    result = update_max_val_div(data, [PM2_5, PM10], 'Switzerland', [2019, 2020])
    texts = [p.children for p in result.children]
    assert any("No data available for PM2.5" in t for t in texts)
    assert any("Max PM10" in t for t in texts)

def test_max_val_div_empty_country_filter():
    data = pd.DataFrame({
        'Country': ['Germany', 'Germany'],
        'Year': [2019, 2020],
        PM2_5: [12, 18],
        PM10: [25, 30],
        NO2: [7, 10]
    })
    result = update_max_val_div(data, [PM2_5], 'Switzerland', [2018, 2021])
    assert isinstance(result, html.Div)
    assert "No data available" in result.children[0].children

#Tests udate_plot with valid input
def test_update_pollution_plot_valid_input():
    data = pd.DataFrame({
        'City': ['Bern', 'Bern', 'Luzern'],
        'Year': [2019, 2020, 2019],
        dashboard.PM2_5: [12, 15, 18],
  
        dashboard.PM10: [25, 30, 20],
        dashboard.NO2: [5, 8, 6]
    })
    fig = dashboard.update_pollution_plot(data, [dashboard.PM2_5], ['Bern'])

    assert isinstance(fig, dashboard.go.Figure)
    assert len(fig.data) > 0
    assert fig.layout.title.text == 'Air Pollution Trends Over Time'

#tests update_pollution with invalid input
def test_update_pollution_plot_no_cities():
    data = pd.DataFrame({
        'City': ['A'],
        'Year': [2020],
        dashboard.PM2_5: [10]
    })
    fig = dashboard.update_pollution_plot(data, [dashboard.PM2_5], [])

    assert isinstance(fig, dashboard.go.Figure)
    assert 'select at least one city' in fig.layout.title.text
    