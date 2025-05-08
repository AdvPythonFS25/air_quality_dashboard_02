# Code Formatting & Linting Report (Pylint Fixes)

## The original `pylint` output (before fixing any issues)

### `main.py`
- `[missing-module-docstring]` Missing module docstring

### `data_processing.py`
- `[line-too-long]` Line too long (128/100)
- `[trailing-whitespace]` Trailing whitespace
- `[missing-final-newline]` Final newline missing
- `[missing-module-docstring]` Missing module docstring

### `dashboard.py`
- `[missing-module-docstring]` Missing module docstring
- `[ungrouped-imports]` Imports from package `dash` are not grouped
- `[ungrouped-imports]` Imports from package `plotly` are not grouped

---

## Fixes applied

-  **Added module-level docstrings** in all files
-  **Grouped related imports** from the same package (especially `dash` and `plotly`)
-  **Wrapped long lines** to comply with 100-character line length limit
-  **Removed trailing whitespace**
-  **Added a final newline** to `data_processing.py`
-  **Reformatted multi-line lists** for readability

---

## Updated Code Versions (after fixing issues)

### `main.py`

```python
"""
Main entry point for the Air Quality Dashboard application.

This script loads and processes air quality data from the WHO dataset,
initializes the Dash dashboard, and starts the web application server.
"""
from pathlib import Path
from data_processing import process_data
from dashboard import create_dashboard

def main():
    """
    Loads the WHO air quality Excel file, processes the data, and launches the Dash dashboard.

    Raises:
        FileNotFoundError: If the WHO data file is not found in the expected directory.
    """
    main_dir = Path(__file__).resolve().parent.parent
    who_data_file = main_dir / 'data' / 'who_ambient_air_quality_database_version_2024_(v6.1).xlsx'
    if not who_data_file.exists():
        raise FileNotFoundError(f"WHO data file not found at: {who_data_file}")
    data = process_data(who_data_file)
    app = create_dashboard(data)
    app.run(debug=True)

if __name__ == '__main__':
    main()
```

### `data_processing.py`

```python
"""
Module for processing WHO air quality Excel data into a clean pandas DataFrame.
"""
from pathlib import Path
import pandas as pd

def process_data(data : Path) -> pd.DataFrame:
    """
    Reads the WHO air quality data from an Excel file and processes it into a DataFrame.
    """
    df = pd.read_excel(data, sheet_name='Update 2024 (V6.1)')

    # Choses the relevant columns from the dataframe
    df = df[[
        'country_name', 'city',
        'year', 'pm10_concentration',
        'pm25_concentration', 'no2_concentration',
        'pm10_tempcov', 'pm25_tempcov',
        'no2_tempcov', 'latitude',
        'longitude']
    ]

    # Deletes the rows with missing core values
    df = df.dropna(subset=['country_name', 'city', 'year'])

    # Unify dataframe
    df['year'] = df['year'].astype(int)
    for col in ['pm10_concentration', 'pm25_concentration',
                'no2_concentration', 'pm10_tempcov',
                'pm25_tempcov', 'no2_tempcov']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Renaming colums
    df = df.rename(columns={
        'country_name': 'Country',
        'city': 'City',
        'year': 'Year',
        'pm10_concentration': 'PM10 (µg/m³)',
        'pm25_concentration': 'PM2.5 (µg/m³)',
        'no2_concentration': 'NO₂ (µg/m³)',
        'pm10_tempcov': 'PM10 Coverage (%)',
        'pm25_tempcov': 'PM2.5 Coverage (%)',
        'no2_tempcov': 'NO₂ Coverage (%)',
        'latitude': 'Latitude',
        'longitude': 'Longitude'
    })
    return df

```
### `dashboard.py`

```python
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
        dash.Output('pm25-trend', 'figure'),
        dash.Input('city-dropdown', 'value'),
        dash.Input('pollutant-dropdown', 'value')
    )

    def update_pollution_plot(selected_cities, selected_pollutants):
        if not selected_cities or not selected_pollutants:
            return px.line(title="Please select at least one city and one pollutant")
        # Filter data to selected countries
        filtered_df = data[data['City'].isin(selected_cities)]

        # Create one plot with one trace per pollutant
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
```