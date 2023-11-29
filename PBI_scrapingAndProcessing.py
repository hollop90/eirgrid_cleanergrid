import requests
import json
import pandas as pd
import datetime

#region dashboard queries
def query_dashbaord(area, date_range, date_from, date_to):
    range_start = None
    range_end = None
    endpoint = "https://www.smartgriddashboard.com/DashboardService.svc/data"

    # If a specific date range is not provided, use the date 3 days ago and the
    # date 2 days from now as the range
    if date_from is None and date_to is None:
        date_to = datetime.date.today() + datetime.timedelta(days=2)
        date_from = date_to - datetime.timedelta(days=date_range)
    else:
        date_to = datetime.date.fromisoformat(date_to)
        date_from = datetime.date.fromisoformat(date_from)

    # Format the date to work with the dashboard's API
    range_start = date_from.strftime("%d-%b-%Y")
    range_end = date_to.strftime("%d-%b-%Y")

    # The query parameters for the dashboard
    payload = [
        ("area", f"{area}"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]

    return requests.get(endpoint, params=payload)

def dashboard_data(*, data_field, date_range=None, date_from=None, date_to=None):
    # Get the data from the dashboard
    response = query_dashbaord(data_field, date_range, date_from, date_to)

    # If the response was OK return something, else return nothing
    if response:
        # Unpack the JSON data from the dashboard and pack it into a Pandas DataFram
        data = response.json()
        # Every response contains a timestamp and a value
        return pd.DataFrame({
            "DateTime" : pd.to_datetime([field["EffectiveTime"] for field in data["Rows"]]),
            data_field : [[field]["Value"] for field in data["Rows"]],
        })
    else:
        return None

def mixture(*, date_range=None, date_from=None, date_to=None):
    # Get the data from the dashboard
    response = query_dashbaord("fuelmix", date_range, date_from, date_to)

    # If the response was OK return something, else return nothing
    if response:
        # Pack the JSON data into a Pandas DataFrame
        data = response.json()
        # This dataframe contains the timestamp, the source of the energy and the amount of energy from that source
        return  pd.DataFrame({
            "Time" : [field["EffectiveTime"] for field in data["Rows"]],
            "Source" : [field["FieldName"] for field in data["Rows"]],
            "Mixture" : [field["Value"] for field in data["Rows"]],
        })
    else:
        return None
#endregion

#region functions and calculations
def calculate_max_min_value_days(_data, data_field): # determine minimum and maximum value for the day
    grouped_data = _data.groupby(_data['DateTime'].dt.date) # group data by days
    _max = grouped_data[data_field].max().rename('Max' + data_field) # find max value for each day
    _min = grouped_data[data_field].min().rename('Min' + data_field) # find minimum value for each day
    return pd.merge(_min, _max, on='DateTime', how='left').merge(_data['DateTime'].dt.date, on="DateTime", how='left') # merge max values, min values and dates into a dataframe

def calculate_max_min_value_hours(_data, data_field, _date): # determine minimum and maximum value for each hour of the day
    grouped_date = _data[_data['DateTime'].dt.date == _date] # filter data by date (today or tomorrow)
    grouped_data = grouped_date.groupby(grouped_date['DateTime'].dt.hour) # group data by hour
    _max = grouped_data[data_field].max().rename('Max' + data_field) # find max value for each hour
    _min = grouped_data[data_field].min().rename('Min' + data_field) # find min value for each hour
    result_df = pd.merge(_min, _max, on='DateTime', how='left').merge(_data['DateTime'].dt.hour, on="DateTime", how='left') # merge max values, min values and date and time into dataframe
    # convert DateTime field (currently stored as int) into datetime fields with requested date and corresponding time
    result_df['RequestedDateTime'] = pd.to_datetime(_date) + pd.to_timedelta(result_df['DateTime'], unit='h')
    result_df = result_df.drop(columns=['DateTime'])
    result_df = result_df.dropna(subset=['Min' + data_field]) # drop empty values
    result_df.rename(columns={'RequestedDateTime': 'DateTime'}, inplace=True)
    return result_df

def calculate_moving_average(demand_maxmin, data_field, window_size): # determine moving average
    moving_average_data = demand_maxmin.copy() # create a copy of data
    moving_average_data['MaxMovingAverage' + data_field] = moving_average_data['Max' + data_field].rolling(window_size).mean() # calculate moving average for max values
    moving_average_data['MinMovingAverage' + data_field] = moving_average_data['Min' + data_field].rolling(window_size).mean() # calculate moving average for min values
    return moving_average_data
#endregion

#region forming dataframes for demand, wind and fuel mix (actual and forecast data)
dem_act = dashboard_data(data_field = "demandactual", date_range=30, date_from=None, date_to=None) # actual demand for the last 28 days dataframe
dem_for = dashboard_data(data_field = "demandforecast", date_range=30, date_from=None, date_to=None) # forecast demand dataframe for last 28 days
wind_act = dashboard_data(data_field = "windactual", date_range=30, date_from=None, date_to=None) # actual wind dataframe for last 28 days
wind_for = dashboard_data(data_field = "windforecast", date_range=30, date_from=None, date_to=None) # forecast wind dataframe for last 28 days
PBImix = mixture(date_range=1, date_from=None, date_to=None) # fuel mix dataframe for now
#endregion

#region calulate maximum and minimum values for each day for demand and wind
dem_maxmin_act_days = calculate_max_min_value_days(dem_act, 'demandactual').drop_duplicates(subset='DateTime') # max and min values for actual demand
dem_maxmin_for_days = calculate_max_min_value_days(dem_for, 'demandforecast').drop_duplicates(subset='DateTime')  # max and min values for forecast demand
wind_maxmin_act_days = calculate_max_min_value_days(wind_act, 'windactual').drop_duplicates(subset='DateTime') # max and min values for actual wind
wind_maxmin_for_days = calculate_max_min_value_days(wind_for, 'windforecast').drop_duplicates(subset='DateTime') # max and min values for forecast wind
#endregion

#region calculate maximum and minimum values for each hour of the day (today or tomorrow) for demand and wind
dem_maxmin_act_hours = calculate_max_min_value_hours(dem_act, 'demandactual', datetime.date.today()).drop_duplicates(subset='DateTime') # max and min values for actual demand for hours of today
dem_maxmin_for_hours = calculate_max_min_value_hours(dem_for, 'demandforecast', datetime.date.today()).drop_duplicates(subset='DateTime')  # max and min values for forecast demand for hours of today
wind_maxmin_act_hours = calculate_max_min_value_hours(wind_act, 'windactual', datetime.date.today()).drop_duplicates(subset='DateTime') # max and min values for actual wind for hours of today
wind_maxmin_for_hours = calculate_max_min_value_hours(wind_for, 'windforecast', datetime.date.today()).drop_duplicates(subset='DateTime') # max and min values for forecast wind for hours of today

dem_maxmin_for_hours_tomorrow = calculate_max_min_value_hours(dem_for, 'demandforecast', datetime.date.today() + datetime.timedelta(days=1)).drop_duplicates(subset='DateTime') # max and min values for forecast demand for hours of tomorrow
wind_maxmin_for_hours_tomorrow = calculate_max_min_value_hours(wind_for, 'windforecast', datetime.date.today() + datetime.timedelta(days=1)).drop_duplicates(subset='DateTime') # max and min values for forecast wind for hours of tomorrow
#endregion

#region calculate moving averages for 7 days for actual data and 1 day for forecast data
dem_maxmin_movavg_act_days = calculate_moving_average(dem_maxmin_act_days, 'demandactual', 7) # calculate 7 day moving average for actual demand
dem_maxmin_movavg_for_days = calculate_moving_average(dem_maxmin_for_days, 'demandforecast', 1) # calculate 1 day moving average for forecast demand
wind_maxmin_movavg_act_days = calculate_moving_average(wind_maxmin_act_days, 'windactual', 7) # calculate 7 day moving average for actual wind
wind_maxmin_movavg_for_days = calculate_moving_average(wind_maxmin_for_days, 'windforecast', 1) # calculate 1 day moving average for forecast wind
#endregion

#region calculate moving averages for 5 hours for actual data and 2 hours for forecast data
dem_maxmin_movavg_act_hours = calculate_moving_average(dem_maxmin_act_hours, 'demandactual', 5) # calculate 5 hour moving average for actual demand for today
dem_maxmin_movavg_for_hours = calculate_moving_average(dem_maxmin_for_hours, 'demandforecast', 2) # calculate 2 hour moving average for forecast demand for today
wind_maxmin_movavg_act_hours = calculate_moving_average(wind_maxmin_act_hours, 'windactual', 5) # calculate 5 hour moving average for actual wind for today
wind_maxmin_movavg_for_hours = calculate_moving_average(wind_maxmin_for_hours, 'windforecast', 2) # calculate 2 hour moving average for forecast wind for today

wind_maxmin_movavg_for_hours_tomorrow = calculate_moving_average(wind_maxmin_for_hours_tomorrow, 'windforecast', 3) # calculate 3 hour moving average for forecast demand for tomorrow
dem_maxmin_movavg_for_hours_tomorrow = calculate_moving_average(dem_maxmin_for_hours_tomorrow, 'demandforecast', 3) # calculate 3 hour moving average for forecast wind for tomorrow
#endregion

#region form PBI tables for demand, wind, actual and forecast data for days
PBIdemand = pd.merge(dem_act, dem_for, on="DateTime", how="outer") # create a demand table for power BI
PBIwind = pd.merge(wind_act, wind_for, on="DateTime", how="outer") # create a wind generation table for power BI
PBIactual_days = pd.merge(dem_maxmin_movavg_act_days, wind_maxmin_movavg_act_days, on="DateTime", how="outer") # create table with actual values for days for wind and demand
PBIactual_days = PBIactual_days[pd.to_datetime(PBIactual_days['DateTime']).dt.date < datetime.date.today()] # filter by today
PBIforecast_days = pd.merge(dem_maxmin_movavg_for_days, wind_maxmin_movavg_for_days, on="DateTime", how="outer") # create table with forecast values for days for wind and demand
PBIforecast_days = PBIforecast_days[pd.to_datetime(PBIforecast_days['DateTime']).dt.date >= datetime.date.today()] # filter by days after today
#endregion

#region find hours data for today and tomorrow
PBIdemand_today = PBIdemand[PBIdemand['DateTime'].dt.date == datetime.date.today()] # filter demand by today's date
PBIwind_today =  PBIwind[PBIwind['DateTime'].dt.date == datetime.date.today()] # filter wind gen by today's date
PBIdemand_tomorrow = PBIdemand[PBIdemand['DateTime'].dt.date == datetime.date.today() + datetime.timedelta(days=1)] # filter demand by tomorrow's date
PBIwind_tomorrow =  PBIwind[PBIwind['DateTime'].dt.date == datetime.date.today() + datetime.timedelta(days=1)] # filter wind by tomorrow's date
#endregion

#region manipulate PBIactual_hours to get data for today
PBIactual_hours = pd.merge(dem_maxmin_movavg_act_hours, wind_maxmin_movavg_act_hours, on="DateTime", how="outer") # create a table for actual data for demand and wind gen for hours
PBIactual_hours = pd.merge(PBIdemand_today, PBIactual_hours, on="DateTime", how="outer") # add demand for today
PBIactual_hours = pd.merge(PBIwind_today, PBIactual_hours, on="DateTime", how="outer") # add wind for today
#endregion

#region manipulate PBIforecast_hours to get data for today
PBIforecast_hours = pd.merge(dem_maxmin_movavg_for_hours, wind_maxmin_movavg_for_hours, on="DateTime", how="outer") # create a table for forecast data for demand and wind gen for hours
PBIforecast_hours = PBIforecast_hours[PBIforecast_hours['DateTime'].dt.hour >= datetime.datetime.now().hour] # filter to have hours after current hour
PBIforecast_hours = pd.merge(PBIdemand_today, PBIforecast_hours, on="DateTime", how="outer") # add demand values
PBIforecast_hours = pd.merge(PBIwind_today, PBIforecast_hours, on="DateTime", how="outer") # add wind values
#endregion

#region manipulate PBIforecast_hours to get data for tomorrow
PBIforecast_hours_tomorrow = pd.merge(wind_maxmin_movavg_for_hours_tomorrow, dem_maxmin_movavg_for_hours_tomorrow, on="DateTime", how="outer") # create dataframe for forecast for each hour for tomorrow
PBIforecast_hours_tomorrow = PBIforecast_hours_tomorrow[PBIforecast_hours_tomorrow['DateTime'].dt.date > datetime.datetime.today().date()] # filter by tomorrow
PBIforecast_hours_tomorrow = pd.merge(PBIdemand_tomorrow, PBIforecast_hours_tomorrow, on="DateTime", how="outer") # add demand values
PBIforecast_hours_tomorrow = pd.merge(PBIwind_tomorrow, PBIforecast_hours_tomorrow, on="DateTime", how="outer") # add wind values
#endregion

#region fill empty cells to eliminate null values for each field
PBIactual_hours = PBIactual_hours[PBIactual_hours['DateTime'].dt.hour <= datetime.datetime.now().hour]
PBIactual_hours['Mindemandactual'] = PBIactual_hours['Mindemandactual'].ffill()
PBIactual_hours['Minwindactual'] = PBIactual_hours['Minwindactual'].ffill()
PBIactual_hours['Maxwindactual'] = PBIactual_hours['Maxwindactual'].ffill()
PBIactual_hours['Maxdemandactual'] = PBIactual_hours['Maxdemandactual'].ffill()
PBIactual_hours['MaxMovingAveragewindactual'] = PBIactual_hours['MaxMovingAveragewindactual'].ffill()
PBIactual_hours['MinMovingAveragewindactual'] = PBIactual_hours['MinMovingAveragewindactual'].ffill()
PBIactual_hours['MaxMovingAveragedemandactual'] = PBIactual_hours['MaxMovingAveragedemandactual'].ffill()
PBIactual_hours['MinMovingAveragedemandactual'] = PBIactual_hours['MinMovingAveragedemandactual'].ffill()

PBIforecast_hours = PBIforecast_hours[PBIforecast_hours['DateTime'].dt.hour >= datetime.datetime.now().hour]
PBIforecast_hours_15min = PBIforecast_hours['DateTime'] + datetime.timedelta(minutes=15) # add 15 minutes increments to datetime
PBIforecast_hours= pd.concat([PBIforecast_hours, PBIforecast_hours_15min], axis=0)
PBIforecast_hours['demandforecast'] = PBIforecast_hours['demandforecast'].ffill()
PBIforecast_hours['Mindemandforecast'] = PBIforecast_hours['Mindemandforecast'].ffill()
PBIforecast_hours['Minwindforecast'] = PBIforecast_hours['Minwindforecast'].ffill()
PBIforecast_hours['Maxwindforecast'] = PBIforecast_hours['Maxwindforecast'].ffill()
PBIforecast_hours['Maxdemandforecast'] = PBIforecast_hours['Maxdemandforecast'].ffill()
PBIforecast_hours['MaxMovingAveragewindforecast'] = PBIforecast_hours['MaxMovingAveragewindforecast'].ffill()
PBIforecast_hours['MinMovingAveragewindforecast'] = PBIforecast_hours['MinMovingAveragewindforecast'].ffill()
PBIforecast_hours['MaxMovingAveragedemandforecast'] = PBIforecast_hours['MaxMovingAveragedemandforecast'].ffill()
PBIforecast_hours['MinMovingAveragedemandforecast'] = PBIforecast_hours['MinMovingAveragedemandforecast'].ffill()

PBIforecast_hours_tomorrow['Mindemandforecast'] = PBIforecast_hours_tomorrow['Mindemandforecast'].ffill()
PBIforecast_hours_tomorrow['Minwindforecast'] = PBIforecast_hours_tomorrow['Minwindforecast'].ffill()
PBIforecast_hours_tomorrow['Maxwindforecast'] = PBIforecast_hours_tomorrow['Maxwindforecast'].ffill()
PBIforecast_hours_tomorrow['Maxdemandforecast'] = PBIforecast_hours_tomorrow['Maxdemandforecast'].ffill()
PBIforecast_hours_tomorrow['MaxMovingAveragewindforecast'] = PBIforecast_hours_tomorrow['MaxMovingAveragewindforecast'].ffill()
PBIforecast_hours_tomorrow['MinMovingAveragewindforecast'] = PBIforecast_hours_tomorrow['MinMovingAveragewindforecast'].ffill()
PBIforecast_hours_tomorrow['MaxMovingAveragedemandforecast'] = PBIforecast_hours_tomorrow['MaxMovingAveragedemandforecast'].ffill()
PBIforecast_hours_tomorrow['MinMovingAveragedemandforecast'] = PBIforecast_hours_tomorrow['MinMovingAveragedemandforecast'].ffill()
#endregion
