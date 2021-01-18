import json


def line_chart_data(json_data, start_date='', end_date=''):
    line_labels = list(json_data.keys())
    line_values = []

    if start_date == '' and end_date == '':
        for case in json_data.values():
            line_values.append(case['active'])

        return line_labels, line_values
    else:
        interval_labels = line_labels[line_labels.index(end_date):line_labels.index(start_date) + 1]
        for date in interval_labels:
            line_values.append(json_data[date]['active'])

        return interval_labels, line_values



def pie_chart_data(json_data, selected_date=''):
    dates = list(json_data.keys())

    pie_labels = ['Total recovered', 'Total confirmed', 'Total deceased']

    if selected_date == '':
        pie_values = [json_data[dates[-1]]['total_recovered'], json_data[dates[-1]]['total_confirmed'],
                      json_data[dates[-1]]['total_deceased']]
    else:
        pie_values = [json_data[selected_date]['total_recovered'], json_data[selected_date]['total_confirmed'],
                      json_data[selected_date]['total_deceased']]

    return pie_labels, pie_values


def format_date(date):
    new_date = date[6:]+'-'+date[3:5]+'-'+date[0:2]
    return new_date

