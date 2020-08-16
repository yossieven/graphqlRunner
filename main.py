import ast
import inspect
import os
import subprocess
import sys
from json.decoder import JSONDecodeError

import requests
import json

import config
from config import CREATE_ENTITY_URL, LOGIN_REQUEST_URL

'''
This class will take a template as an argument and will fill it according to requested
sections in the jason. The section you need to fill should have its own json file
with the data expected to reside within it.
'''


class GraphQLRunner:

    login_string: str

    def __init__(self, action: int, username, password, role):
        with open(config.ACTIONS_TEMPLATES[action]["template"]) as json_file:
            # obj = json.loads(json_file.read())
            self.template_content = json_file.read()
            self.user = username
            self.role = role
            self.password = password
            self.action = action

    def replace_object_in_dict(self, key: str, dictionary: dict, value: any):
        """ go over all items in the json dictionary """
        for k, v in dictionary.items():
            """ for endpoints make sure the value is a string and not a complex structure """
            if type(value) != dict and type(value) != list:
                if k == key:
                    if type(value) == dict or type(value) == list:
                        raise Exception('key is a leaf and cannot be assigned a dictionary or list')
                    dictionary[k] = value
                    return dictionary
            elif isinstance(v, dict):
                """ for a dictionary type of key make sure the value is also a dictionary and add all items """
                if k == key:
                    if type(value) != dict:
                        raise Exception('value must be a dictionary object')
                    for new_key, new_value in value.items():
                        dictionary[k][new_key] = new_value
                    return dictionary
                else:
                    self.replace_object_in_dict(key, dictionary[k], value)
            elif isinstance(v, list):
                """ for list type, if the value is a list also, add it as is, otherwise make sure it is encapsulated """
                if k == key:
                    if type(value) == list:
                        dictionary[k] = value
                    else:
                        dictionary[k] = [value]
                    return dictionary
                else:
                    self.replace_object_in_dict(key, dictionary[k], value)

    def prepare_request(self, variables=None, links=None, remarks=None, tags=None,
                        classification=None, permissions=None):

        sections = {'variables': variables, 'links': links, 'remarks': remarks, 'tags': tags, 'classification': classification, 'permissions': permissions}

        for key in [k for k in sections if k != 'self']:
            if sections[key] is not None and sections[key] != '':
                with open(sections[key]) as json_file:
                    data = json_file.read()
                self.template_content = self.transform_json(key, data, self.template_content)

        content_json = json.loads(self.template_content)
        """ add the query string to template """
        self.replace_object_in_dict(key="query", dictionary=content_json,
                                    value=config.ACTIONS_TEMPLATES[self.action]["query"])

        pretty_json = json.dumps(content_json, indent=4)
        self.template_content = pretty_json
        print(pretty_json)
        f = open('result.json', 'w')
        f.write(pretty_json)
        f.close
        self.call_login_token()
        self.call_create_entity()

    def call_login_token(self):
        url = LOGIN_REQUEST_URL
        data = {"userName": self.user, "password": self.password}
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=data, headers=headers)
        self.login_string = r.json()['jwt']
        print(r.status_code)
        print(self.login_string)

    def call_create_entity(self):
        url = CREATE_ENTITY_URL
        data = json.loads(self.template_content)
        token = 'Bearer ' + self.login_string
        headers = {"Content-Type": "application/json", "Authorization": token,
                   "WS-USER-INFO.NAME": self.user, "WS-USER-INFO.ROLES": self.role}
        r = requests.post(url, json=data, headers=headers)
        print(r.status_code)
        print(r.json())

    def transform_json(self, section, data, template_content):
        try:
            json_template = json.loads(template_content)
            json_data = json.loads(data)
            self.replace_object_in_dict(key=section, dictionary=json_template, value=json_data)

            dump = json.dumps(json_template)
            final_dump = dump.replace('\\n', '')

            return final_dump
        except JSONDecodeError as e:
            print("provided json" + section + " has caused an error.")
            return template_content


if __name__ == '__main__':
    with open('create_phone_variables.json') as json_file:
        variables_data = json_file.read()
    # with open('create_phone_links.json') as json_file:
    #     links_data = json_file.read()
    # with open('create_phone_remarks.json') as json_file:
    #     remarks_data = json_file.read()
    # with open('create_phone_tags.json') as json_file:
    #     tags_data = json_file.read()
    # with open('create_phone_classification.json') as json_file:
    #     classification_data = json_file.read()
    # with open('create_phone_permissions.json') as json_file:
    #     permissions_data = json_file.read()
    action = None
    while action is None:
        try:
            action = int(input("Please choose action: \n (1) Create New Phone \n (2) Create New Vehicle \n (3) Create News \n Action >> "))
        except TypeError:
            action = None
        except ValueError:
            action = None

    if sys.platform.startswith('linux'):
        clear = lambda: os.system('clear')
    else:
        clear = lambda: os.system('cls')
    clear()
    variables_data = input("\n Variables: Enter name of json file : ")
    links_data = input("\n Links: Enter name of json file : ")
    tags_data = input("\n Tags: Enter name of json file : ")
    remarks_data = input("\n Remarks: Enter name of json file : ")
    permissions_data = input("\n Permissions: Enter name of json file : ")

    graphQLRunner = GraphQLRunner(action, 'wstu9', 'Pass123', 'system_role_analyst')
    graphQLRunner.prepare_request(variables=variables_data)
