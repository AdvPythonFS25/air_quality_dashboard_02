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
    app.run(debug = True)

if __name__ == '__main__':
    main()
