import matplotlib.pyplot as plt
import time
import soup

"""
Uncomment for demand plot
"""
# x = soup.demand(range=30)
# vals = [x["Rows"][i]["Value"] for i in range(len(x["Rows"]))] # List comprehension
# fig, ax = plt.subplots()
# ax.plot(vals)
# plt.show()

"""
Uncomment for mixture plot
"""
# x = soup.mixture(range=1)
# vals = [x["Rows"][i]["Value"] for i in range(len(x["Rows"]))] # List comprehension
# fig, ax = plt.subplots()
# ax.pie(vals)
# plt.show()

"""
Uncomment for wind gen plot
"""
# x = soup.wind(range=30)
# vals = [x["Rows"][i]["Value"] for i in range(len(x["Rows"]))] # List comprehension
# fig, ax = plt.subplots()
# ax.plot(vals)
# plt.show()

# DATA WE ARE INTERESTED IN
# - Demand for the month
# - Fuel mix for the:
#   - day
#   - week
#   - month
# - Wind generation for the month
# - Wind generation forecast
