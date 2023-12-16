import os
import json
import matplotlib.pyplot as plt
import pandas as pd


def get_json_files(directory):
    # Traverse the directory and get all JSON files
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def parse_json(json_file):
    # Open and parse the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    # Extract necessary data
    # TODO: Add your extraction logic here
    return data