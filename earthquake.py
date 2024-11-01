import pandas as pd
import requests
from datetime import datetime, timedelta, timezone

def get_data(startdate, enddate):
    """Fetch earthquake data from USGS API."""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        'format': 'geojson',
        'starttime': startdate,
        'endtime': enddate
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")
        return None

def extract_data(raw_data):
    """Extract relevant data from raw USGS response."""
    clean_data = []
    features = raw_data.get('features', [])
    for feature in features:
        earthquake = {
            'Magnitude': feature['properties'].get('mag'),
            'Location': feature['properties'].get('place'),
            'Latitude': feature['geometry']['coordinates'][1],
            'Longitude': feature['geometry']['coordinates'][0]
        }
        clean_data.append(earthquake)
    return clean_data

def save_to_csv(data, path):
    """Save extracted data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"Data saved to {path}")

# Calculate yesterday's date
yesterday = datetime.now(timezone.utc) - timedelta(days=1)
startdate = yesterday.strftime('%Y-%m-%d')
enddate = (yesterday + timedelta(days=1)).strftime('%Y-%m-%d')

# Fetch, process, and save earthquake data for yesterday
raw_data = get_data(startdate, enddate)
if raw_data:
    clean_data = extract_data(raw_data)
    save_to_csv(clean_data, 'earthquakes_yesterday.csv')
    print("Cleaned earthquake data:")
    print(clean_data)
else:
    print("No data available to process.")