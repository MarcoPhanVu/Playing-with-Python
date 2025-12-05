import random
import math
import json
import os
import tkinter as tk
from tkinter import *

class Configurator:


    def __init__(self):
        pass


# VSC -> root starts at project's workspace
file = open("./data/highscores_org.txt")

highscores_JSON = {}


for line in file:
    print(line)
    name = line.split(": ")[0]
    score = line.split(": ")[1][:-2]
    highscores_JSON[name] = score

print(highscores_JSON)


# json.loads -> to dict
# json.dumps -> to json

# def main():
#     pass

# main()