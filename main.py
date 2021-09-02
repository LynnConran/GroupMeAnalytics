import datetime
import csv
from matplotlib import pyplot as plt
import numpy as np


def assign_names(filepath):
    name_dict = {}
    with open(filepath, 'r', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for line in reader:
            if line[1] == 'GroupMe':
                continue
            if line[0] not in name_dict:  # Assigns the most recent nickname to the persistent id
                name_dict[line[0]] = line[1]
    return name_dict


def get_months_of_messages(filepath):
    name_dict = assign_names(filepath)
    month_dict = {}
    with open(filepath, 'r', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for line in reader:
            month = str(datetime.datetime.fromtimestamp(int(line[3])))[:7]
            if line[1] == 'GroupMe':
                continue
            if month not in month_dict:
                month_dict[month] = {}
            if name_dict[line[0]] not in month_dict[month]:
                month_dict[month][name_dict[line[0]]] = 0
            month_dict[month][name_dict[line[0]]] += 1
    return month_dict


def make_pie_chart(month_data, name_dict):
    # Creating dataset
    names = []
    plt.figure(figsize=(20, 10))
    for i in name_dict:
        names.append(name_dict[i])
    data_count = 0
    data = {}
    for month in month_data:
        data[data_count] = []
        for name in name_dict:
            if name_dict[name] in month_data[month]:
                data[data_count].append(month_data[month][name_dict[name]])
            else:
                data[data_count].append(0)
        data_count += 1
    for i in data:
        plt.subplot(5, 5, i + 1)
        plt.pie(data[i], labels=names)
        # plt.title(month)
    plt.savefig('Stevie.png')
    plt.show()


if __name__ == '__main__':
    # path = 'direct messages/Kathleen Brewster.csv'
    # make_pie_chart(get_months_of_messages(path), assign_names(path))
    # path = 'groups/Qlarence.csv'
    # make_pie_chart(get_months_of_messages(path), assign_names(path))
    # path = 'groups/L.csv'
    # make_pie_chart(get_months_of_messages(path), assign_names(path))
    # path = 'direct messages/Sanji Albert.csv'
    # make_pie_chart(get_months_of_messages(path), assign_names(path))
    path = 'direct messages/Savannah H.csv'
    make_pie_chart(get_months_of_messages(path), assign_names(path))
    # path = 'groups/We\'re all traitors here.csv'
    # make_pie_chart(get_months_of_messages(path), assign_names(path))

