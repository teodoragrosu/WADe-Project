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

        return interval_labels[::-1], line_values[::-1]


def evol_chart_data(json_data, start_date='', end_date=''):
    evol_labels = list(json_data.keys())
    evol_recovered = []
    evol_deceased = []

    for date in json_data.values():
        evol_recovered.append(date['recovered'])
        evol_deceased.append(date['deceased'])

    return evol_labels[::-1], evol_recovered[::-1], evol_deceased[::-1]


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


def save_chart_data():
    with open('templates/country_data.json') as json_file:
        json_data = json.load(json_file)

        with open("templates/evol_data.json", "w") as data:
            evol_labels, evol_recovered, evol_deceased = evol_chart_data(json_data)
            evol_json = {'evol_labels': evol_labels, 'evol_recovered': evol_recovered, 'evol_deceased': evol_deceased}
            json.dump(evol_json, data)

        with open("templates/line_data.json", "w") as data:
            line_labels, line_values = line_chart_data(json_data, list(json_data.keys())[-1], list(json_data.keys())[0])
            line_json = {'line_labels': line_labels, 'line_values': line_values}
            json.dump(line_json, data)

        with open("templates/pie_data.json", "w") as data:
            pie_labels, pie_values = pie_chart_data(json_data, list(json_data.keys())[0])
            pie_json = {'pie_labels': pie_labels, 'pie_values': pie_values}
            json.dump(pie_json, data)


def format_date(date):
    new_date = date[6:]+'-'+date[3:5]+'-'+date[0:2]
    return new_date

