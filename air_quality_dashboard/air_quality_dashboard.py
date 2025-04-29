import pandas as pd


# we will neeed to decise if we want to only create an application object here and then return it
# or if we want to create the dashboard here and also run it here
# what framework we will use to create the dashboard ?
def create_dashboard(data : pd.DataFrame) -> None: #TODO
    """
    Entry point to the dashboard after data processing.
    """
    
    
    # at the moment we will just print the data to the console
    print(data.head())