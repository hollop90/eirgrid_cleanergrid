import matplotlib.pyplot as plt
import time
import soup

demand_data = soup.demand(date_range=3)
mix_data = soup.mixture(date_range=3)
wind = soup.wind(date_range=3)
wind_forecast = soup.wind_forecast(date_range=3)

print(demand_data)
print(mix_data)
print(wind)
print(wind_forecast)
