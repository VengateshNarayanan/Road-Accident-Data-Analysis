# Road Accident Data Analysis System

A Python-based desktop application for analysing road accident statistics through an interactive dashboard. The system presents accident cases, injuries, fatalities, and location-wise comparisons using data visualisation.

## Overview

The Road Accident Data Analysis System helps users explore accident statistics through an interactive graphical interface. It processes a CSV dataset, calculates summary statistics, and displays visualisations to make accident data easier to understand.

Users can switch between overall and state-wise analysis, select different metrics, compare accident categories, and control how many locations appear in ranking charts.

## Features

- **Interactive Dashboard:** View accident statistics in a graphical interface.
- **Summary Cards:** Display accident cases, people injured, and deaths.
- **Overall Analysis:** Explore statistics across the records included in the dataset.
- **State-wise Analysis:** Examine accident statistics for a selected state or union territory.
- **Metric Selection:** Analyse different measures, such as accident cases, injuries, and deaths.
- **Top Locations:** Rank locations and display a configurable number of results, such as Top 10 or Top 15.
- **Data Visualisation:** Present comparisons and patterns using charts and heatmaps.
- **CSV Data Processing:** Load, clean, and process accident statistics for analysis.

## Technologies Used

- **Python** — Core programming language
- **Tkinter and ttk** — Graphical user interface
- **Pandas** — Data loading, processing, filtering, and aggregation
- **Matplotlib** — Charts and data visualisation
- **CSV** — Dataset storage and input

## Project Structure

```text
Road_Accident_Analysis/
│
├── main.py                  # Application entry point
├── config.py                # Shared configuration and constants
├── data_loader.py           # Loads and prepares CSV data
├── calculations.py          # Filtering, summaries, and calculations
├── plots.py                 # Chart and heatmap generation
├── dashboard.py             # Dashboard interface and interactions
├── requirements.txt         # Python dependencies
└── ADSI_Table_1A.2_2.csv    # Accident statistics dataset
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Road_Accident_Analysis
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

Make sure the CSV dataset is available at the location expected by the application.

## How It Works

1. **Data Loading:** The application reads accident statistics from the CSV dataset.
2. **Data Preparation:** The data loader prepares the records for analysis.
3. **Data Analysis:** The calculations module filters records and computes relevant statistics.
4. **Dashboard Display:** Summary cards present accident cases, injuries, and deaths.
5. **Visualisation:** Matplotlib generates charts to compare locations and accident categories.
6. **Interactive Exploration:** Users can change analysis modes, metrics, geographical selections, and the number of locations displayed.

## Understanding the Dashboard

The summary cards represent totals for the selected analysis scope. The Top Locations setting controls how many locations appear in the ranking chart; it does not automatically change the summary totals.

The figures shown depend on the supplied dataset and the application's calculation logic. They should not be interpreted as current national statistics without verifying the dataset's reporting period and coverage.

## Limitations

- Analysis depends on the completeness and accuracy of the supplied dataset.
- The application analyses the available recorded statistics; it does not independently verify accident reports.
- The system does not perform real-time accident monitoring or predict future accidents.
- The available analysis is limited to the fields present in the dataset.

## Future Enhancements

- Add more interactive filters and visualisations.
- Support additional datasets and reporting periods.
- Introduce export options for charts and analytical summaries.
- Improve data validation and handling of missing values.

## Conclusion

The Road Accident Data Analysis System demonstrates how Python, Pandas, Tkinter, and Matplotlib can be combined to build a desktop-based data analysis application. It provides an accessible way to explore accident statistics, compare locations, and understand patterns in the available data.

## License

This project is intended for educational and academic purposes. Add a suitable open-source license if you plan to distribute it publicly.
