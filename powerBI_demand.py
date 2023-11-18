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

def demand(*, date_range=None, date_from=None, date_to=None):
    response = query_dashbaord("demandactual", date_range, date_from, date_to)

    if response:
        data = response.json()
        return pd.DataFrame({
            "Time" : [data["Rows"][i]["EffectiveTime"] for i in range(len(data["Rows"]))],
            "Demand Actual" : [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))],
        })
    else:
        return None
    
    def demand_forecast(*, date_range=None, date_from=None, date_to=None):
    response = query_dashbaord("demandforecast", date_range, date_from, date_to)

    if response:
        data = response.json()
        return pd.DataFrame({
            "Time" : [data["Rows"][i]["EffectiveTime"] for i in range(len(data["Rows"]))],
            "Demand Forecast" : [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))],
        })
    else:
        return None
    
    demand_act = demand(date_range=30, date_from=None, date_to=None)
    demand_for = demand_forecast(date_range=3, date_from=None, date_to=None)
    
    data_frame = pd.merge(dem_act, dem_for, on="Time", how="outer")
    print(data_frame)
