from data_processing import process_data
from air_quality_dashboard import create_dashboard

from pathlib import Path


def main():
    
    main_dir = Path(__file__).resolve().parent.parent
    who_data_file = main_dir / 'data' / 'who_ambient_air_quality_database_version_2024_(v6.1).xlsx'
    
    if not who_data_file.exists():
        raise FileNotFoundError(f"WHO data file not found at: {who_data_file}")
    
    data = process_data(who_data_file)
    app = create_dashboard(data)
    app.run(debug = True)


if __name__ == '__main__':
    main()