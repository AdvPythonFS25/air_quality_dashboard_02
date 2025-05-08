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
