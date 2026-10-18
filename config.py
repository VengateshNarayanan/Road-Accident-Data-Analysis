
DATA_FILE = "ADSI_Table_1A.2_2.csv"

NAME_COLUMN = "State/UT/City"
SERIAL_COLUMN = "Sl. No."

METRICS = {
    "Accident Cases": "Total Traffic Accidents - Cases",
    "People Injured": "Total Traffic Accidents - Injured",
    "Deaths": "Total Traffic Accidents - Died",
    "Road Accident Cases": "Road Accidents - Cases",
    "Railway Accident Cases": "Railway Accidents - Cases",
    "Railway Crossing Cases": "Railway Crossing Accidents - Cases",
}

ACCIDENT_CATEGORIES = {
    "Road Accidents": {
        "cases": "Road Accidents - Cases",
        "injured": "Road Accidents - Injured",
        "deaths": "Road Accidents - Died",
    },
    "Railway Accidents": {
        "cases": "Railway Accidents - Cases",
        "injured": "Railway Accidents - Injured",
        "deaths": "Railway Accidents - Died",
    },
    "Railway Crossing Accidents": {
        "cases": "Railway Crossing Accidents - Cases",
        "injured": "Railway Crossing Accidents - Injured",
        "deaths": "Railway Crossing Accidents - Died",
    },
}
