import requests
import csv
import json
import pandas as pd

def query_semopx(resource_name):
    """
    Query the SEMOpx API for a specific resource

    :param resource_name: The name of the resource to query for
    :return: A dictionary containing the json response or None if the request failed
    :rtype: dict
    """
    payload = {
        "DPuG_ID": "EA-001",
        "order_by":	"DESC",
        "sort_by": "Date",
        "ExcludeDelayedPublication": "0",
        "ResourceName": resource_name,
    }
    response = requests.get("https://reports.sem-o.com/api/v1/documents/static-reports", params=payload)

    if response:
        return response.json()
    else:
        return None

def day_ahead():
    """
    Returns a datafram containing the day ahead prices

    :return: DataFrame containing the day ahead prices
    :rtype: pandas.DataFrame
    """
    data = query_semopx("MarketResult_SEM-DA_PWR-MRC-D")
    if data is not None:
        id = data["items"][0]["_id"]

        payload = {"IST": "1"}
        document = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload).json()

        return pd.DataFrame({
            "Timestamp" : pd.to_datetime(document["rows"][0][2]),
            "Prices" : document["rows"][0][3],
        })
    else:
        return []

def interday_auction(auction_number):
    """
    Returns a datafram containing the interday auction 1, 2, or 3

    :param auction_number: The desired interday auction
    :type auction_number: int
    :return: A datafram containing the interday auction prices
    :rtype: pandas.DataFrame
    """
    ida = ["MarketResult_SEM-IDA1_PWR-SEM-GB-D", "MarketResult_SEM-IDA2_PWR-SEM-GB-D", "MarketResult_SEM-IDA3_PWR-SEM-D_"]

    data = query_semopx(ida[auction_number - 1])
    if data is not None:
        id = data["items"][0]["_id"]

        payload = {"IST": "1"}
        document = requests.get(f"https://reports.sem-o.com/api/v1/documents/{id}", params=payload).json()

        return pd.DataFrame({
            "Timestamp" : pd.to_datetime(document["rows"][0][2]),
            "Prices" : document["rows"][0][3],
        })
    else:
        return []

if __name__ == "__main__":
    print(day_ahead())
    print(interday_auction(1))
    print(interday_auction(2))
    print(interday_auction(3))
