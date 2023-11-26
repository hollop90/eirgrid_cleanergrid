import requests
import json
import pandas as pd
import datetime

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
    
def calculate_max_min_value_days(demand_data, data_field):
    grouped_data = demand_data.groupby(demand_data['DateTime'].dt.date)
    _max = grouped_data[data_field].max().rename('Max' + data_field)
    _min = grouped_data[data_field].min().rename('Min' + data_field)

    return pd.merge(_min, _max, on='DateTime', how='left').merge(demand_data['DateTime'].dt.date, on="DateTime", how='left')


def calculate_max_min_value_hours(demand_data, data_field):
    today_date = datetime.date.today()
    
    grouped_date = demand_data[demand_data['DateTime'].dt.date == today_date]
    grouped_data = grouped_date.groupby(grouped_date['DateTime'].dt.hour)
    
    _max = grouped_data[data_field].max().rename('Max' + data_field)
    _min = grouped_data[data_field].min().rename('Min' + data_field)

    result_df = pd.merge(_min, _max, on='DateTime', how='left').merge(demand_data['DateTime'].dt.hour, on="DateTime", how='left')
    
    result_df['TodayDateTime'] = pd.to_datetime(today_date) + pd.to_timedelta(result_df['DateTime'], unit='h')
    
    result_df = result_df.drop(columns=['DateTime'])
    
    result_df = result_df.dropna(subset=['Min' + data_field])
    
    result_df.rename(columns={'TodayDateTime': 'DateTime'}, inplace=True)
    
    return result_df

def calculate_moving_average(demand_maxmin, data_field, window_size):
    moving_average_data = demand_maxmin.copy()

    moving_average_data['MaxMovingAverage' + data_field] = moving_average_data['Max' + data_field].rolling(window_size).mean()

    moving_average_data['MinMovingAverage' + data_field] = moving_average_data['Min' + data_field].rolling(window_size).mean()

    return moving_average_data

dem_act = dashboard_data(data_field = "demandactual", date_range=30, date_from=None, date_to=None)
dem_for = dashboard_data(data_field = "demandforecast", date_range=30, date_from=None, date_to=None) 
wind_act = dashboard_data(data_field = "windactual", date_range=30, date_from=None, date_to=None)
wind_for = dashboard_data(data_field = "windforecast", date_range=30, date_from=None, date_to=None)

dem_maxmin_act_days = calculate_max_min_value_days(dem_act, 'demandactual').drop_duplicates(subset='DateTime')
dem_maxmin_for_days = calculate_max_min_value_days(dem_for, 'demandforecast').drop_duplicates(subset='DateTime')  
wind_maxmin_act_days = calculate_max_min_value_days(wind_act, 'windactual').drop_duplicates(subset='DateTime') 
wind_maxmin_for_days = calculate_max_min_value_days(wind_for, 'windforecast').drop_duplicates(subset='DateTime') 

dem_maxmin_act_hours = calculate_max_min_value_hours(dem_act, 'demandactual').drop_duplicates(subset='DateTime')
dem_maxmin_for_hours = calculate_max_min_value_hours(dem_for, 'demandforecast').drop_duplicates(subset='DateTime')  
wind_maxmin_act_hours = calculate_max_min_value_hours(wind_act, 'windactual').drop_duplicates(subset='DateTime') 
wind_maxmin_for_hours = calculate_max_min_value_hours(wind_for, 'windforecast').drop_duplicates(subset='DateTime') 

dem_maxmin_movavg_act_days = calculate_moving_average(dem_maxmin_act_days, 'demandactual', 7) 
dem_maxmin_movavg_for_days = calculate_moving_average(dem_maxmin_for_days, 'demandforecast', 1) 
wind_maxmin_movavg_act_days = calculate_moving_average(wind_maxmin_act_days, 'windactual', 7)
wind_maxmin_movavg_for_days = calculate_moving_average(wind_maxmin_for_days, 'windforecast', 1)

dem_maxmin_movavg_act_hours = calculate_moving_average(dem_maxmin_act_hours, 'demandactual', 5) 
dem_maxmin_movavg_for_hours = calculate_moving_average(dem_maxmin_for_hours, 'demandforecast', 1) 
wind_maxmin_movavg_act_hours = calculate_moving_average(wind_maxmin_act_hours, 'windactual', 5)
wind_maxmin_movavg_for_hours = calculate_moving_average(wind_maxmin_for_hours, 'windforecast', 1)

PBIdemand = pd.merge(dem_act, dem_for, on="DateTime", how="outer")
PBIwind = pd.merge(wind_act, wind_for, on="DateTime", how="outer")
PBIactual_days = pd.merge(dem_maxmin_movavg_act_days, wind_maxmin_movavg_act_days, on="DateTime", how="outer")
PBIactual_days = PBIactual_days[pd.to_datetime(PBIactual_days['DateTime']).dt.date < datetime.date.today()]
PBIforecast_days = pd.merge(dem_maxmin_movavg_for_days, wind_maxmin_movavg_for_days, on="DateTime", how="outer")
PBIforecast_days = PBIforecast_days[pd.to_datetime(PBIforecast_days['DateTime']).dt.date >= datetime.date.today()]

PBIactual_hours = pd.merge(dem_maxmin_movavg_act_hours, wind_maxmin_movavg_act_hours, on="DateTime", how="outer")

PBIforecast_hours = pd.merge(dem_maxmin_movavg_for_hours, wind_maxmin_movavg_for_hours, on="DateTime", how="outer")
PBIforecast_hours = PBIforecast_hours[PBIforecast_hours['DateTime'].dt.hour >= datetime.datetime.now().hour]

today_date = datetime.date.today()
PBIdemand_today = PBIdemand[PBIdemand['DateTime'].dt.date == today_date]
PBIwind_today =  PBIwind[PBIwind['DateTime'].dt.date == today_date]

PBIactual_hours = pd.merge(PBIdemand_today, PBIactual_hours, on="DateTime", how="outer")
PBIactual_hours = pd.merge(PBIwind_today, PBIactual_hours, on="DateTime", how="outer")

PBIforecast_hours = pd.merge(PBIdemand_today, PBIforecast_hours, on="DateTime", how="outer")
PBIforecast_hours = pd.merge(PBIwind_today, PBIforecast_hours, on="DateTime", how="outer")

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
PBIforecast_hours['Mindemandforecast'] = PBIforecast_hours['Mindemandforecast'].ffill()
PBIforecast_hours['Minwindforecast'] = PBIforecast_hours['Minwindforecast'].ffill()
PBIforecast_hours['Maxwindforecast'] = PBIforecast_hours['Maxwindforecast'].ffill()
PBIforecast_hours['Maxdemandforecast'] = PBIforecast_hours['Maxdemandforecast'].ffill()
PBIforecast_hours['MaxMovingAveragewindforecast'] = PBIforecast_hours['MaxMovingAveragewindforecast'].ffill()
PBIforecast_hours['MinMovingAveragewindforecast'] = PBIforecast_hours['MinMovingAveragewindforecast'].ffill()
PBIforecast_hours['MaxMovingAveragedemandforecast'] = PBIforecast_hours['MaxMovingAveragedemandforecast'].ffill()
PBIforecast_hours['MinMovingAveragedemandforecast'] = PBIforecast_hours['MinMovingAveragedemandforecast'].ffill()

print(PBIforecast_hours)