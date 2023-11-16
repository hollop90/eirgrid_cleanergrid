import soup
import pandas as pd

dem_act = soup.demand(date_range=3, date_from=None, date_to=None)
dem_for = soup.demand_forecast(date_range=3, date_from=None, date_to=None)

dem_all = pd.merge(dem_act, dem_for, on="Time", how="outer")
dem_all.fillna(0, inplace=True)

print(dem_all)
