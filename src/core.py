import json as json
import os


def get_instructions_as_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def get_instruction_as_json(path, preference_name):

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get(preference_name)