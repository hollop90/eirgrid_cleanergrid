# import matplotlib
import requests
import json


print("EIRGRID CLEANERGRID")

# response = requests.get("https://www.smartgriddashboard.com/DashboardService.svc/data?area=demandactual&region=ALL&datefrom=11-Nov-2023+00%3A00&dateto=11-Nov-2023+23%3A59")

payload = [("area", "demandactual"), ("region", "ALL"), ("datefrom", "11-Nov-2023 00:00"), ("dateto", "11-Nov-2023 23:59")]
response = requests.get(
        "https://www.smartgriddashboard.com/DashboardService.svc/data",
        params=payload
    )

print(response.url)

if response:
    print(response)
    print(response.json())
    with open("temp.json", "w+") as file:
        file.write(json.dumps(response.json()))
else:
    print("REQUEST FAILED")

# DATA WE ARE INTERESTED IN
# - Demand for the month
# - Fuel mix for the:
#   - day
#   - week
#   - month
# - Wind generation for the month
# - Wind generation forecast
