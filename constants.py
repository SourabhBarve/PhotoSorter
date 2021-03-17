import json
from types import SimpleNamespace

f = open("./frontend/constants.json")
Constants = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

# class ConstantsObj:
#     def __init__(self, **entries):
#         self.__dict__.update(entries)

# Constants = ConstantsObj(**c)