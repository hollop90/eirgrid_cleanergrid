import requests
import json
import pandas as pd
import datetime

#region functions and calculations
def query_dashbaord(area, date_range, date_from, date_to):
    range_start = None
    range_end = None

    if date_from is None and date_to is None:
        date_to = datetime.date.today() + datetime.timedelta(days=2)
        date_from = date_to - datetime.timedelta(days=date_range)
    else:
        date_to = datetime.date.fromisoformat(date_to)
        date_from = datetime.date.fromisoformat(date_from)

    range_start = date_from.strftime("%d-%b-%Y")
    range_end = date_to.strftime("%d-%b-%Y")

    payload = [
        ("area", f"{area}"),
        ("region", "ALL"),
        ("datefrom", f"{range_start} 00:00"),
        ("dateto", f"{range_end} 23:59")
    ]

    endpoint = "https://www.smartgriddashboard.com/DashboardService.svc/data"
    return requests.get(endpoint, params=payload)

def dashboard_data(*, data_field, date_range=None, date_from=None, date_to=None):
    response = query_dashbaord(data_field, date_range, date_from, date_to)

    if response:
        data = response.json()
        return pd.DataFrame({
            "DateTime" : pd.to_datetime([data["Rows"][i]["EffectiveTime"] for i in range(len(data["Rows"]))]),
            data_field : [data["Rows"][i]["Value"] for i in range(len(data["Rows"]))],
        })
    else:
        return None
    
def calculate_max_min_value_days(_data, data_field):
    grouped_data = _data.groupby(_data['DateTime'].dt.date)
    _max = grouped_data[data_field].max().rename('Max' + data_field)
    _min = grouped_data[data_field].min().rename('Min' + data_field)

    return pd.merge(_min, _max, on='DateTime', how='left').merge(_data['DateTime'].dt.date, on="DateTime", how='left')

def calculate_max_min_value_hours(_data, data_field, _date):
    grouped_date = _data[_data['DateTime'].dt.date == _date]
    grouped_data = grouped_date.groupby(grouped_date['DateTime'].dt.hour)
    
    _max = grouped_data[data_field].max().rename('Max' + data_field)
    _min = grouped_data[data_field].min().rename('Min' + data_field)

    result_df = pd.merge(_min, _max, on='DateTime', how='left').merge(_data['DateTime'].dt.hour, on="DateTime", how='left')
    
    result_df['TodayDateTime'] = pd.to_datetime(_date) + pd.to_timedelta(result_df['DateTime'], unit='h')
    
    result_df = result_df.drop(columns=['DateTime'])
    
    result_df = result_df.dropna(subset=['Min' + data_field])
    
    result_df.rename(columns={'TodayDateTime': 'DateTime'}, inplace=True)
    
    return result_df

def calculate_moving_average(demand_maxmin, data_field, window_size):
    moving_average_data = demand_maxmin.copy()

    moving_average_data['MaxMovingAverage' + data_field] = moving_average_data['Max' + data_field].rolling(window_size).mean()

    moving_average_data['MinMovingAverage' + data_field] = moving_average_data['Min' + data_field].rolling(window_size).mean()

    return moving_average_data
#endregion
#region Scrape demand and wind generation data
dem_act = dashboard_data(data_field = "demandactual", date_range=30, date_from=None, date_to=None)
dem_for = dashboard_data(data_field = "demandforecast", date_range=30, date_from=None, date_to=None) 
wind_act = dashboard_data(data_field = "windactual", date_range=30, date_from=None, date_to=None)
wind_for = dashboard_data(data_field = "windforecast", date_range=30, date_from=None, date_to=None)
#endregion
#region calulate maxmin values for days
dem_maxmin_act_days = calculate_max_min_value_days(dem_act, 'demandactual').drop_duplicates(subset='DateTime')
dem_maxmin_for_days = calculate_max_min_value_days(dem_for, 'demandforecast').drop_duplicates(subset='DateTime')  
wind_maxmin_act_days = calculate_max_min_value_days(wind_act, 'windactual').drop_duplicates(subset='DateTime') 
wind_maxmin_for_days = calculate_max_min_value_days(wind_for, 'windforecast').drop_duplicates(subset='DateTime') 
#endregion
#region calculate maxmin values for hours
dem_maxmin_act_hours = calculate_max_min_value_hours(dem_act, 'demandactual', datetime.date.today()).drop_duplicates(subset='DateTime')
dem_maxmin_for_hours = calculate_max_min_value_hours(dem_for, 'demandforecast', datetime.date.today()).drop_duplicates(subset='DateTime')  
wind_maxmin_act_hours = calculate_max_min_value_hours(wind_act, 'windactual', datetime.date.today()).drop_duplicates(subset='DateTime') 
wind_maxmin_for_hours = calculate_max_min_value_hours(wind_for, 'windforecast', datetime.date.today()).drop_duplicates(subset='DateTime') 

dem_maxmin_for_hours_tomorrow = calculate_max_min_value_hours(dem_for, 'demandforecast', datetime.date.today() + datetime.timedelta(days=1)).drop_duplicates(subset='DateTime') 
wind_maxmin_for_hours_tomorrow = calculate_max_min_value_hours(wind_for, 'windforecast', datetime.date.today() + datetime.timedelta(days=1)).drop_duplicates(subset='DateTime')
#endregion
#region calculate moving average for days
dem_maxmin_movavg_act_days = calculate_moving_average(dem_maxmin_act_days, 'demandactual', 7) 
dem_maxmin_movavg_for_days = calculate_moving_average(dem_maxmin_for_days, 'demandforecast', 1) 
wind_maxmin_movavg_act_days = calculate_moving_average(wind_maxmin_act_days, 'windactual', 7)
wind_maxmin_movavg_for_days = calculate_moving_average(wind_maxmin_for_days, 'windforecast', 1)
#endregion
#region calculate moving average for hours
dem_maxmin_movavg_act_hours = calculate_moving_average(dem_maxmin_act_hours, 'demandactual', 5) 
dem_maxmin_movavg_for_hours = calculate_moving_average(dem_maxmin_for_hours, 'demandforecast', 2) 
wind_maxmin_movavg_act_hours = calculate_moving_average(wind_maxmin_act_hours, 'windactual', 5)
wind_maxmin_movavg_for_hours = calculate_moving_average(wind_maxmin_for_hours, 'windforecast', 2)

wind_maxmin_movavg_for_hours_tomorrow = calculate_moving_average(wind_maxmin_for_hours_tomorrow, 'windforecast', 2)
dem_maxmin_movavg_for_hours_tomorrow = calculate_moving_average(dem_maxmin_for_hours_tomorrow, 'demandforecast', 2) 
#endregion
#region form PBI tables for demand, wind and days
PBIdemand = pd.merge(dem_act, dem_for, on="DateTime", how="outer")
PBIwind = pd.merge(wind_act, wind_for, on="DateTime", how="outer")
PBIactual_days = pd.merge(dem_maxmin_movavg_act_days, wind_maxmin_movavg_act_days, on="DateTime", how="outer")
PBIactual_days = PBIactual_days[pd.to_datetime(PBIactual_days['DateTime']).dt.date < datetime.date.today()]
PBIforecast_days = pd.merge(dem_maxmin_movavg_for_days, wind_maxmin_movavg_for_days, on="DateTime", how="outer")
PBIforecast_days = PBIforecast_days[pd.to_datetime(PBIforecast_days['DateTime']).dt.date >= datetime.date.today()]
#endregion
#region find hours data for today and tomorrow 
PBIdemand_today = PBIdemand[PBIdemand['DateTime'].dt.date == datetime.date.today()]
PBIwind_today =  PBIwind[PBIwind['DateTime'].dt.date == datetime.date.today()]

PBIdemand_tomorrow = PBIdemand[PBIdemand['DateTime'].dt.date == datetime.date.today() + datetime.timedelta(days=1)]
PBIwind_tomorrow =  PBIwind[PBIwind['DateTime'].dt.date == datetime.date.today() + datetime.timedelta(days=1)]
#endregion
#region manipulate PBIactual_hours
PBIactual_hours = pd.merge(dem_maxmin_movavg_act_hours, wind_maxmin_movavg_act_hours, on="DateTime", how="outer")
PBIactual_hours = pd.merge(PBIdemand_today, PBIactual_hours, on="DateTime", how="outer")
PBIactual_hours = pd.merge(PBIwind_today, PBIactual_hours, on="DateTime", how="outer")
#endregion
#region manipulate PBIforecast_hours for today
PBIforecast_hours = pd.merge(dem_maxmin_movavg_for_hours, wind_maxmin_movavg_for_hours, on="DateTime", how="outer")
PBIforecast_hours = PBIforecast_hours[PBIforecast_hours['DateTime'].dt.hour >= datetime.datetime.now().hour]
PBIforecast_hours = pd.merge(PBIdemand_today, PBIforecast_hours, on="DateTime", how="outer")
PBIforecast_hours = pd.merge(PBIwind_today, PBIforecast_hours, on="DateTime", how="outer")
#endregion
#region manipulate PBIforecast_hours for tomorrow
PBIforecast_hours_tomorrow = pd.merge(wind_maxmin_movavg_for_hours_tomorrow, dem_maxmin_movavg_for_hours_tomorrow, on="DateTime", how="outer")
PBIforecast_hours_tomorrow = PBIforecast_hours_tomorrow[PBIforecast_hours_tomorrow['DateTime'].dt.date > datetime.datetime.today().date()]
PBIforecast_hours_tomorrow = pd.merge(PBIdemand_tomorrow, PBIforecast_hours_tomorrow, on="DateTime", how="outer")
PBIforecast_hours_tomorrow = pd.merge(PBIwind_tomorrow, PBIforecast_hours_tomorrow, on="DateTime", how="outer")
#endregion
#region fill empty cells
