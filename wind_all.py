import soup
import pandas as pd

wind_act = soup.wind(date_range=3, date_from=None, date_to=None)
wind_for = soup.wind_forecast(date_range=3, date_from=None, date_to=None)

wind_all = pd.merge(wind_act, wind_for, on="Time", how="outer")
wind_all.fillna(0, inplace=True)

print(wind_all)

