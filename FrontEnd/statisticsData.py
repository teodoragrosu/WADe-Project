import json


def line_chart_data(json_data, start_date='', end_date=''):
    line_dict = {}
    line_labels = list(json_data.keys())
    line_values = []

    if start_date == '' and end_date == '':
        for case in json_data.values():
            line_values.append(case['active'])

        return line_labels, line_values
    else:
        interval_labels = line_labels[line_labels.index(end_date):line_labels.index(start_date) + 1]
        for date in interval_labels:
            line_dict[date] = json_data[date]['active']

        return line_dict


def evol_chart_data(json_data, start_date='', end_date=''):
    date = list(json_data.keys())
    recovered = []
    deceased = []

    for item in json_data.values():
        recovered.append(item['recovered'])
        deceased.append(item['deceased'])

    return date[::-1], recovered[::-1], deceased[::-1]


def pie_chart_data(json_data, selected_date=''):
    pie_dict = {}
    dates = list(json_data.keys())

    pie_labels = ['Total recovered', 'Total confirmed', 'Total deceased']

    if selected_date == '':
        pie_values = [json_data[dates[-1]]['total_recovered'], json_data[dates[-1]]['total_confirmed'],
                      json_data[dates[-1]]['total_deceased']]
    else:
        pie_dict['Total recovered'] = json_data[selected_date]['total_recovered']
        pie_dict['Total confirmed'] = json_data[selected_date]['total_confirmed']
        pie_dict['Total deceased'] = json_data[selected_date]['total_deceased']

    return pie_dict


def save_chart_data():
    with open('templates/chart_data/country_data.json') as json_file:
        json_data = json.load(json_file)

        with open("templates/chart_data/evol_data.json", "w") as data:
            evol_labels, evol_recovered, evol_deceased = evol_chart_data(json_data)
            evol_json = {'evol_labels': evol_labels, 'evol_recovered': evol_recovered, 'evol_deceased': evol_deceased}
            json.dump(evol_json, data)

        with open("templates/chart_data/line_data.json", "w") as data:
            line_labels, line_values = line_chart_data(json_data, list(json_data.keys())[-1], list(json_data.keys())[0])
            line_json = {'line_labels': line_labels, 'line_values': line_values}
            json.dump(line_json, data)

        with open("templates/chart_data/pie_data.json", "w") as data:
            pie_labels, pie_values = pie_chart_data(json_data, list(json_data.keys())[0])
            pie_json = {'pie_labels': pie_labels, 'pie_values': pie_values}
            json.dump(pie_json, data)


def format_date(date):
    new_date = date[6:]+'-'+date[3:5]+'-'+date[0:2]
    return new_date

