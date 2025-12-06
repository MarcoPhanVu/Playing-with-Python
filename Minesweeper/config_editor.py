import random
import math
import json
import os
import tkinter as tk
from tkinter import *

class Configurator:
    def __init__(self):
        pass
    
    def load_settings(self, path: str):
        pass

    def load_highscores(self, path: str):
        pass

    def save_settings(self, path: str):
        pass
    def save_highscores(self, path: str):
        pass

    def set_highscore(self, name: str, score: int):
        pass

    def get_colors(self) -> dict:
        pass

    def get_color(self, element: str) -> str:
        pass

    def set_colors(self, colors: dict):
        pass

# VSC -> root starts at project's workspace -> disabled
file = open("./data/highscores_org.txt")
highscores_JSON = {}
cars_JSON = {
    "Toyota": {
        "Camry": {
            "Type" : "Sedan",
            "weight": 1.6
        },
        "RAV4": {
            "Type" : "SUV",
            "weight": 1.8 
        },
        "Corolla": {
            "Type" : "Sedan",
            "weight": 1.5
        },
        "Highlander": {
            "Type" : "SUV",
            "weight": 1.8
        },
        "Tacoma": {
            "Type" : "Truck",
            "weight": 2
        },
        "Prius": {
            "Type" : "Sedan",
            "weight": 1.2
        }
    },
    "Honda": {
        "Civic": {
            "Type" : "Sedan",
            "weight": 1.5
        },
        "CR-V": {
            "Type" : "SUV",
            "weight": 1.7 
        },
        "Accord": {
            "Type" : "Sedan",
            "weight": 1.6
        },
        "Odyssey": {
            "Type" : "Minivan",
            "weight": 1.9
        },
        "Ridgeline": {
            "Type" : "Truck",
            "weight": 2.1
        },
        "Insight": {
            "Type" : "Sedan",
            "weight": 1.3
        }
    }
}

for count, line in enumerate(file):
    if(count == 20):
        break
    name = line.split(": ")[0]
    score = line.split(": ")[1][:-2]
    highscores_JSON[name] = score

print(f"len: {len(highscores_JSON)}")
print(highscores_JSON)

with open("highscores.json", "w") as file:
    json.dump(highscores_JSON, file, indent = 4)
    file.close()

# json.loads -> to dict
# json.dumps -> to json

# def main():
#     pass

# main()

