"""Function to evaluate the time rating based on incremental interaction between resources"""

import pandas as pd
from dateutil.relativedelta import relativedelta


def time_df(data, end):
    from datetime import datetime
    import sys
    try:
        dataframe = pd.DataFrame()
        end_date = datetime.strptime(end, '%Y-%m-%d')
        for j in range(len(data)):
            time = datetime.strptime(data.Timestamp.iloc[j], '%Y-%m-%d %H:%M:%S.%f')
            if time <= end_date:
                dataframe = dataframe.append(data.iloc[j])
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in retrieving data for the specified timeframe")
    return dataframe


def get_interest_rating(data_resource, data_user_select):
    import sys
    data_time_sort = data_resource.sort_values(['Timestamp'], ascending=True)
    s_time = data_time_sort['Timestamp'].iloc[0]
    e_time = data_time_sort['Timestamp'].iloc[-1]
    dur = pd.to_datetime(e_time) - pd.to_datetime(s_time)

    try:
        data_previous_resources = time_df(data_user_select, e_time)
        resources_list = data_resource.Resource.unique()
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in retrieving data for the specified timeframe")
    total_duration = 0
    for res in resources_list:
        data_res_selected = data_previous_resources[data_resource["ResourceId"] == res]
        data_time_sort = data_res_selected.sort_values(['Timestamp'], ascending=True)
        while len(data_file_filtered.Operation.value_counts()) > 0:
            trace_length = 0
            start_time = data_file_filtered['Timestamp'].iloc[0]
            added_time_window = pd.to_datetime(start_time) + relativedelta(minutes=+24)
            end_time = added_time_window.strftime('%Y-%m-%d %H:%M:%S.%f')
            data_time_filtered = data_time_sort.loc[(data_time_sort['Timestamp'] >= start_time) &
                                                    (data_time_sort['Timestamp'] <= end_time)]
            trace = data_time_filtered["Operation"].to_list()
            trace_length = trace_length + len(trace)
            row_length = len(data_file_filtered.index)
            data_file_filtered = data_file_filtered.iloc[trace_length:row_length]
            if len(data_file_filtered) == 1:
                duratn = pd.to_datetime(5)
            else:
                data_time_sort = data_file_filtered.sort_values(['Timestamp'], ascending=True)
                st_time = data_time_sort['Timestamp'].iloc[0]
                e_time = data_time_sort['Timestamp'].iloc[-1]
                duratn = pd.to_datetime(e_time) - pd.to_datetime(st_time)
                total_duration = total_duration + duratn
    rating = dur / total_duration
    if rating >= 1:
        return 1
    else:
        return 0
