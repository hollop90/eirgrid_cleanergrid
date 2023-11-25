import requests
import csv
import json
import pandas as pd

def day_ahead():
    payload = {
        "DPuG_ID": "EA-001",
        "order_by":	"DESC",
        "sort_by": "Date",
        "ExcludeDelayedPublication": "0",
        "ResourceName": "MarketResult_SEM-DA_PWR-MRC-D",
    }
    response = requests.get("https://reports.sem-o.com/api/v1/documents/static-reports", params=payload)

    if response:
        # print("OK")
        id = response.json()["items"][0]["_id"]
        # print(f"_id: {id}")

        payload = {
            "IST": "1",
        }
        response = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload)

        prices = response.json()["rows"][0][3]
        return pd.DataFrame({ "Prices" : prices })
    else:
        return []

def interday_auction_1():
    payload = {
    	"DPuG_ID": "EA-001",
    	"order_by": "DESC",
    	"sort_by": "Date",
    	"ExcludeDelayedPublication": "0",
    	"ResourceName": "MarketResult_SEM-IDA1_PWR-SEM-GB-D"
    }

    response = requests.get("https://reports.sem-o.com/api/v1/documents/static-reports", params=payload)

    if response:
        id = response.json()["items"][0]["_id"]

        payload = {
            "IST": "1",
        }
        response = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload)

        prices = response.json()["rows"][0][3]
        return pd.DataFrame({ "Prices" : prices })
    else:
        return []

def interday_auction_2():
    payload = {
    	"DPuG_ID": "EA-001",
    	"order_by": "DESC",
    	"sort_by": "Date",
    	"ExcludeDelayedPublication": "0",
    	"ResourceName": "MarketResult_SEM-IDA2_PWR-SEM-GB-D"
    }

    response = requests.get("https://reports.sem-o.com/api/v1/documents/static-reports", params=payload)

    if response:
        id = response.json()["items"][0]["_id"]

        payload = {
            "IST": "1",
        }
        response = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload)

        prices = response.json()["rows"][0][3]
        return pd.DataFrame({ "Prices" : prices })
    else:
        return []

def interday_auction_3():
    payload = {
    	"DPuG_ID": "EA-001",
    	"order_by": "DESC",
    	"sort_by": "Date",
    	"ExcludeDelayedPublication": "0",
    	"ResourceName": "MarketResult_SEM-IDA3_PWR-SEM-D_"
    }

    response = requests.get("https://reports.sem-o.com/api/v1/documents/static-reports", params=payload)

    if response:
        id = response.json()["items"][0]["_id"]

        payload = {
            "IST": "1",
        }
        response = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload)

        prices = response.json()["rows"][0][3]
        return pd.DataFrame({ "Prices" : prices })
    else:
        return []

print(interday_auction_1())
print(interday_auction_2())
print(interday_auction_3())
