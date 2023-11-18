import requests
import json
import pandas as pd
import datetime

def query_dashbaord(area, date_range, date_from, date_to):
    range_start = None
    range_end = None

    if date_from is None and date_to is None:
        date_to = datetime.date.today()
        date_from = date_to - datetime.timedelta(days=date_range)
    else:
        date_to = datetime.date.fromisoformat(date_to)
        date_from = datetime.date.fromisoformat(date_from)

    range_start = date_from.strftime("%d-%b-%Y")
    range_end = date_to.strftime("%d-%b-%Y")

    payload = [
        ("area", f"{area}"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]

    endpoint = "https://www.smartgriddashboard.com/DashboardService.svc/data"
    return requests.get(endpoint, params=payload)

def wind(*, date_range=None, date_from=None, date_to=None):
    response = query_dashbaord("windactual", date_range, date_from, date_to)

    if response:
        data = response.json()
        return  pd.DataFrame({
            "Time" : [data["Rows"][i]["EffectiveTime"] for i in range(len(data["Rows"]))],
            "Wind" : [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))],
        })
    else:
        return None
    
def wind_forecast(*, date_range=None, date_from=None, date_to=None):
    response = query_dashbaord("windforecast", date_range, date_from, date_to)

    if response:
        data = response.json()
        return pd.DataFrame({
            "Time" : [data["Rows"][i]["EffectiveTime"] for i in range(len(data["Rows"]))],
            "Forecast" : [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))],
        })
    else:
        return None

wind_act = wind(date_range=3, date_from=None, date_to=None)
wind_for = wind_forecast(date_range=3, date_from=None, date_to=None)

data_frame = pd.merge(wind_act, wind_for, on="Time", how="outer")
print(data_frame)
