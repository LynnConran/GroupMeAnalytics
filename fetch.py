import requests
import csv
import os

URL = 'https://api.groupme.com/v3'
# TOKEN = [Removed for privacy purposes, groupme token can be accessed via their website]


def get_groups():
    params = {'per_page' : 100}
    response = requests.get(URL + '/groups?token=' + TOKEN, params=params)
    r = response.json()['response']
    with open('groups.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for group in r:
            writer.writerow([group['name'], group['group_id'], group['messages']['count']])


def get_dms():
    params = {'per_page': 100}
    response = requests.get(URL + '/chats?token=' + TOKEN, params=params)
    r = response.json()['response']
    with open('messages.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for chat in r:
            writer.writerow([chat['other_user']['name'], chat['other_user']['id'], chat['messages_count']])


def get_messages(group_name, group_id, message_total):
    message_count = 0
    message_id = 0
    message_list = []
    while message_count < message_total:
        params = {'limit': 100}
        if message_id:
            params['before_id'] = message_id
        response = requests.get('https://api.groupme.com/v3/groups/%s/messages?token=%s' % (group_id, TOKEN),
                                params=params)
        messages = response.json()['response']['messages']
        for message in messages:
            message_count += 1
            message_id = message['id']
            message_list.append([message['user_id'], message['name'], remove_delimiters(['|', '\n'], message['text']),
                                 message['created_at'], message['favorited_by']])
    dir_name = 'groups'
    file_name = group_name + '.csv'
    directory = os.path.join(dir_name, file_name)
    with open(directory, 'w+', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerows(message_list)


def write_all_messages():
    with open('messages.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print('Working on: ' + row[0])
            get_direct_messages(row[0], int(row[1]), int(row[2]))
    with open('groups.csv', newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print('Working on: ' + row[0])
            get_messages(row[0], int(row[1]), int(row[2]))


def get_direct_messages(chat_name, chat_id, message_total):
    message_count = 0
    message_id = 0
    message_list = []
    while message_count < message_total:
        params = {'limit': 100, 'other_user_id': chat_id}
        if message_id:
            params['before_id'] = message_id
        response = requests.get('https://api.groupme.com/v3/direct_messages?token=%s' % TOKEN,
                                params=params)
        messages = response.json()['response']['direct_messages']
        for message in messages:
            message_count += 1
            message_id = message['id']
            message_list.append([message['user_id'], message['name'], remove_delimiters(['|', '\n'], message['text']),
                                 message['created_at'], message['favorited_by']])
    dir_name = 'direct messages'
    file_name = chat_name + '.csv'
    directory = os.path.join(dir_name, file_name)
    with open(directory, 'w+', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerows(message_list)


def remove_delimiters (delimiters, s):
    new_s = s
    if type(s) is str:
        for i in delimiters:  # replace each delimiter in turn with a space
            new_s = new_s.replace(i, ' ')
        return ' '.join(new_s.split())
    else:
        return ''


if __name__ == '__main__':
    get_groups()
    get_dms()
    write_all_messages()
