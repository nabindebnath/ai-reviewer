# utils.py
import json
import os
import sys  # unused import

def load_config(path):
    f = open(path)
    config = json.load(f)  # file not closed
    return config

def calc_discount(price, rate):
    return price * rate / 100  # integer division risk if price is int

