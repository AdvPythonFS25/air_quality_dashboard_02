from pathlib import Path
import pandas as pd


def process_data(data : Path) -> pd.DataFrame:
    """
    Reads the WHO air quality data from an Excel file and processes it into a DataFrame.
    """
    df = pd.read_excel(data, sheet_name='Update 2024 (V6.1)')
    
    # Do some processing on the data
    # TODO
    
    return df