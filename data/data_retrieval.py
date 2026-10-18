import pandas as pd
import requests
from config import macro_sett


def fred_getter(series_id: str) -> pd.DataFrame:

    '''
    FRED macroeconomic data series getter function
    series_id: economic series to be specified by the user. 
    '''
    
    url = "https://api.stlouisfed.org/fred/series/observations"

    api_key = macro_sett.FRED_API_KEY

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }

    response = requests.get(url, params=params)

    data = response.json()

    df = pd.DataFrame(data['observations'])

    return df

df = fred_getter("UNRATE")


df["date"] = pd.to_datetime(df["date"])
df["value"] = pd.to_numeric(df["value"], errors="coerce")

print(df.info())
print(df.head())
print(df.tail())