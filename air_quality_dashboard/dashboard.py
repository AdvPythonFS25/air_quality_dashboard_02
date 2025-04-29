import pandas as pd
from dash import Dash, html, dash_table


def create_dashboard(data : pd.DataFrame) -> Dash:
    """
    Creates a dashboard app from the given data.
    The data is expected to be a pandas DataFrame, formatted as per the WHO air quality database.
    The dashboard will be created using the Dash framework.
    """
    app = Dash()
    
    # simple app displaying the data
    app.layout = [
        html.H1('Air Quality Dashboard'),
        html.Div('This is a simple dashboard to display air quality data.'),
        dash_table.DataTable(data.to_dict('records'))
    ]
    
    return app