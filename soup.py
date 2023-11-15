import requests
import json
import pandas as pd
import datetime

endpoint = "https://www.smartgriddashboard.com/DashboardService.svc/data"
def demand(*, date_range=None, date_from=None, date_to=None):
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
        ("area", "demandactual"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]
    response = requests.get(endpoint, params=payload)
    if response:
        data = response.json()
        rows = [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))]
        dict = {
            "Demand" : rows
        }
        demand = pd.DataFrame(dict)
        return demand
    else:
        return None

def mixture(*, date_range=None, date_from=None, date_to=None):
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
        ("area", "fuelmix"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_start} 23:59")
    ]

    response = requests.get(endpoint, params=payload)
    if response:
        # List comprehension
        data = response.json()
        rows = [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))]
        dict = {
            "Mixture" : rows
        }
        return pd.DataFrame(dict)
    else:
        return None

def wind(*, date_range=None, date_from=None, date_to=None):
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
        ("area", "windactual"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]
    response = requests.get(endpoint, params=payload)
    if response:
        data = response.json()
        rows = [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))]
        dict = {
            "Wind" : rows
        }
        return pd.DataFrame(dict)
    else:
        return None

def wind_forecast(*, date_range=None, date_from=None, date_to=None):
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
        ("area", "windforecast"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]
    response = requests.get(endpoint, params=payload)
    if response:
        data = response.json()
        rows = [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))]
        dict = {
            "Forecast" : rows
        }
        return pd.DataFrame(dict)
    else:
        return None
