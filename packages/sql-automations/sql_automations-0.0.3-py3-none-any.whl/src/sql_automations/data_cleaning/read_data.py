#!/usr/bin/env python3

def read_data(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
    return data

