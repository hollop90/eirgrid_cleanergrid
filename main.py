import matplotlib.pyplot as plt
import time
import soup

x = soup.demand(range=30)

# print(x["Rows"])

vals = [x["Rows"][i]["Value"] for i in range(len(x["Rows"]))]
fig, ax = plt.subplots()
ax.plot(vals)
plt.show()
# DATA WE ARE INTERESTED IN
# - Demand for the month
# - Fuel mix for the:
#   - day
#   - week
#   - month
# - Wind generation for the month
# - Wind generation forecast
