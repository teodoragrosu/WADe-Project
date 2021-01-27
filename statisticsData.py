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
        pie_dict['Total recovered'] = json_data[selected_date]['total_recovered'] if 'total_recovered' in json_data[selected_date] else '0'
        pie_dict['Total confirmed'] = json_data[selected_date]['total_confirmed'] if 'total_confirmed' in json_data[selected_date] else '0'
        pie_dict['Total deceased'] = json_data[selected_date]['total_deceased'] if 'total_deceased' in json_data[selected_date] else '0'

    return pie_dict


def save_chart_data():
    with open('templates/chart_data/country_data.json') as json_file:
        json_data = json.load(json_file)

        with open("templates/chart_data/evol_data.json", "w") as data:
            evol_labels, evol_recovered, evol_deceased = evol_chart_data(json_data)
            evol_json = {'date': evol_labels, 'recovered': evol_recovered, 'deceased': evol_deceased}
            json.dump(evol_json, data)

        with open("templates/chart_data/line_data.json", "w") as data:
            line_dict = line_chart_data(json_data, list(json_data.keys())[-1], list(json_data.keys())[0])
            json.dump(dict(sorted(line_dict.items())), data)

        with open("templates/chart_data/pie_data.json", "w") as data:
            pie_dict = pie_chart_data(json_data, list(json_data.keys())[0])
            json.dump(pie_dict, data)


def format_date(date):
    new_date = date[6:]+'-'+date[3:5]+'-'+date[0:2]
    return new_date

