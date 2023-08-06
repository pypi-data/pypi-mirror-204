import json
import os
from pathlib import Path

BASE_PATH = Path.cwd().joinpath('data')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))


def load_files(data_file="headers"):
    """Use this function in order to load a json file in the data folder"""
    data_folder = {}
    try:
        with open(os.path.join(ROOT_DIR, f"data/{data_file}.json"), encoding="utf-8") as json_data:
            data_folder[f'{data_file}'] = json.load(json_data)
    except IOError as error:
        return error
    return data_folder[f"{data_file}"]


def write_files(payload, data_file="headers"):
    """Use this function in order to write to a json file in the data folder"""
    try:
        with open(os.path.join(ROOT_DIR, f"data/{data_file}.json"), encoding="utf-8", mode='w') as json_data:
            json.dump(payload, json_data)
    except IOError as error:
        return error


def read_file(file_name):
    path = get_file_with_json_extension(file_name)
    with path.open(mode='r') as f:
        return json.load(f)


def get_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = BASE_PATH.joinpath(file_name)
    else:
        path = BASE_PATH.joinpath(f'{file_name}.json')
    return path


def update_json_file(_file_name, _id=None, _name=None, _address=None, _gender=None, _age=None):
    try:
        """load file to modify"""
        payload = load_files(_file_name)
        """update values"""
        payload[0]['id'] = _id
        payload[0]['name'] = _name
        payload[0]['age'] = _age
        payload[0]['address'] = _address
        payload[0]['gender'] = _gender
        """update json file"""
        write_files(payload=payload, data_file=_file_name)
    except Exception as error:
        return error
    return payload
