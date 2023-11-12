import requests
import json
import pandas
import datetime

"""
@brief Returns the demand for a specified time range
@param range Time range [day, week, month, custom]
"""
def demand(*, range=None, date_from=None, date_to=None):
    range_start = None
    range_end = None

    if date_from is None and date_to is None:
        date_to = datetime.date.today()
        date_from = date_to - datetime.timedelta(days=range)
    else:
        date_to = datetime.date.fromisoformat(date_to)
        date_from = datetime.date.fromisoformat(date_from)


    range_start = date_from.strftime("%d-%b-%Y")
    range_end = date_to.strftime("%d-%b-%Y")

    print(range_start)
    print(range_end)

    payload = [
        ("area", "demandactual"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]
    response = requests.get("https://www.smartgriddashboard.com/DashboardService.svc/data", params=payload)
    if response:
        return response.json()
    else:
        return None
