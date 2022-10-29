import json


def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def update_config(json_str: str):
    with open('config.json', 'w') as f:
        json.dump(json_str, f)
