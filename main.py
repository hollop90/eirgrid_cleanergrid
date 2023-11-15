import matplotlib.pyplot as plt
import time
import soup

"""
Uncomment for demand plot
"""
x = soup.demand(date_range=3)
fig, ax = plt.subplots()
print(x)
ax.plot(x["Demand"])
plt.show()

"""
Uncomment for mixture plot
"""
x = soup.mixture(date_range=3)
fig, ax = plt.subplots()
print(x)
ax.pie(x["Mixture"])
plt.show()

"""
Uncomment for wind gen plot
"""
x = soup.wind(date_range=3)
fig, ax = plt.subplots()
print(x)
ax.plot(x["Wind"])
plt.show()

"""
Uncomment for wind forecast plot
"""
x = soup.wind_forecast(date_range=3)
fig, ax = plt.subplots()
print(x)
ax.plot(x["Forecast"])
plt.show()

# DATA WE ARE INTERESTED IN
# - Demand for the month
# - Fuel mix for the:
#   - day
#   - week
#   - month
# - Wind generation for the month
# - Wind generation forecast
