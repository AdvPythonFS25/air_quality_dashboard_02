# WHO Air Quality Dashboard
This project was created as part of the course *Programming for Data Sciences* by students of the university of Bern.
We've worked on creating a simple interactive dashboard for exploring air quality data across countries and cities, 
using data from the **World Health Organization (WHO) Global Health Observatory**. 

---
# Data
The WHO Ambient Air Quality Database compiles data on ground measurements of annual mean concentrations of nitrogen 
dioxide (NO2), particulate matter of a diameter equal or smaller than 10 μm (PM10) or equal or smaller than 2.5 μm 
(PM2.5) which aim at representing an average for the city or town as a whole, rather than for individual stations. 
Both groups of pollutants originate mainly from human activities related to fossil fuel combustion. In order to present 
air quality data that represent human exposure, we used mainly urban measurements, comprising urban background, 
residential areas, commercial and mixed areas or rural areas and industrial areas close to urban settlements.

**Source:** [WHO Global Health Observatory – Air Pollution](https://www.who.int/data/gho/data/themes/air-pollution)

---
# Project Structure
```
project/
│
├── air_quality_dashboard/ 
│   ├── main.py                     # Main app
│   ├── dashboard.py                # Dashboard functionality
│   └── data_processing.py          # Data cleaning and processing functions
├── data/                           # Folder containing data files
├── notebooks/
│   └── playground.ipynb            # Experimental Jupyter notebook
├── requirements.txt                # Dependencies for the project
├── README.md                       # Documentation of the project - you're here right now!
└── Roadmap.md                      # Project roadmap

```
## Week 9: First Deliverable – What is implemented

### 1. Data Processing (`data_processing.py`)
- WHO Excel data is read from the official WHO database (version 2024 v6.1).
- Relevant columns are selected and renamed for readability:
  - Location: `Country`, `City`, `Latitude`, `Longitude`
  - Time: `Year`
  - Pollutants: `PM2.5 (µg/m³)`, `PM10 (µg/m³)`, `NO₂ (µg/m³)`
  - Temporal coverage (optional): `PM2.5 Coverage (%)`, `PM10 Coverage (%)`, `NO₂ Coverage (%)`
- Data types are converted to ensure numerical operations and plotting are possible.

### 2. Dashboard Interface (`dashboard.py`)
- Built using [Dash by Plotly](https://dash.plotly.com/).
- Layout includes:
  - Dropdown to select one or more **cities**
  - Dropdown to select one or more **pollutants** (PM2.5, PM10, NO₂)
  - A responsive **line chart** that updates based on user selections
  - A data table showing the raw filtered data

### 3. Application Entrypoint (`main.py`)
- Coordinates data loading and dashboard creation.

---
# Dependencies
Currently listed in requirements.txt.
You can simply load them with:

```pip install -r requirements.txt```

---
# Features
- Compare air pollution across cities and time
- Analyze PM2.5, PM10, and NO₂ individually or combined
- View underlying data in a clean table

---
# License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.

**Read the notes!**
