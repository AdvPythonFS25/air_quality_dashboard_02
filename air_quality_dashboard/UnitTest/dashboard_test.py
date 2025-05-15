import pandas as pd
from dash import html
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dashboard  

#Tests the normal ("good") case of update_max_val
def test_update_max_val_div_normal_case():
    data = pd.DataFrame({
        'City': ['A', 'A', 'B', 'B'],
        'Year': [2020, 2021, 2020, 2021],
        dashboard.PM2_5: [10, 20, 30, 40],
        dashboard.PM10: [15, 25, 35, 45],
        dashboard.NO2: [5, 15, 25, 35]
    })
    result = dashboard.update_max_val_div(data, [dashboard.PM2_5, dashboard.PM10, dashboard.NO2])
    
    
    assert isinstance(result, html.Div)
    assert len(result.children) == 3
    assert any("Max PM2.5" in p.children for p in result.children)

#tests the "bad" case where there is no Data available
def test_update_max_val_div_all_nan():
    data = pd.DataFrame({
        'City': ['A', 'B'],
        'Year': [2020, 2021],
        dashboard.PM2_5: [None, None],
        dashboard.PM10: [None, None],
        dashboard.NO2: [None, None]
    })
    result = dashboard.update_max_val_div(data, [dashboard.PM2_5, dashboard.PM10, dashboard.NO2])
    
   
    assert all("No data available" in p.children for p in result.children)

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
    