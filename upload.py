#!/usr/bin/env python3

import xmltodict
import requests
import html
import os
import time
import json

attr_file = 'C:/Program Files (x86)/Steam/steamapps/common/Hunt Showdown/user/profiles/default/attributes.xml'
upload_url = 'https://huntplayers.com/collector/upload/'
match_url = 'https://huntplayers.com/match/{}'


def parse_attr_file(filepath):
    with open(attr_file, encoding='utf8') as xml:
        data = xmltodict.parse(xml.read())['Attributes']['Attr']

    attrs = [(x['@name'] + ('\t\t' + html.escape(x['@value'])) if x['@value'] else x['@name']) for x in data if 'uiName' not in x['@name'] and 'iconPath' not in x['@name'] and (x['@name'].startswith('Mission') or 'Region' in x['@name'])]

    return attrs


def post_request(attrs):
    print('Reporting match...')
    payload = '\r\n'.join(attrs).encode()
    r = requests.post(url=upload_url, data=payload)
    if r.text:
        uuid = json.loads(r.text)['uuid']
        print(match_url.format(uuid))
    return r


def load_last_modified():
    if not os.path.isfile('last_modified.txt'):
        return 0
    with open('last_modified.txt', 'r') as file:
        time = file.read()
    return float(time)


def save_last_modified(time):
    with open('last_modified.txt', 'w') as file:
        file.write(str(time))


def run(filepath):
    print("Auto-uploading Hunt: Showdown stats.")
    last_modified = load_last_modified()
    while True:
        modified = os.path.getmtime(filepath)
        if not last_modified or last_modified < modified:
            print("attributes.xml file was updated.")
            last_modified = modified
            save_last_modified(last_modified)
            post_request(parse_attr_file(filepath))
        time.sleep(60)


run(attr_file)
