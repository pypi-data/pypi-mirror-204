import os
from inspect import getmembers, isfunction
from json import dumps

#######################################################

foldername = __file__.split("\\")[-2]

dataStruct = {foldername : {}}

for file in os.listdir():
    if file.endswith(".py"):
        if file not in ["__init__.py", __file__.split("\\")[-1]]:
            dataStruct[foldername][file.replace(".py", "")] = {}

for package in dataStruct[foldername].keys():
    exec(f"import {package}")
    exec(f"dataStruct[foldername][package]['doc'] = {package}.__doc__")

    dataStruct[foldername][package]["funcs"] = {}
    funclist = []
    exec(f"funclist = getmembers({package}, isfunction)")
    for name, func in funclist:
        dataStruct[foldername][package]["funcs"][name] = func.__doc__

#print(dumps(dataStruct, indent=4))
#######################################################

readme = f"# {foldername}\n"
with open("ModuleStart.txt", "r") as f2:
        readme += f2.read() + "\n\n"

readme += "# Table of Contents\n"
count = 1
for package in dataStruct[foldername].keys():
    readme += f"## {str(count)}. [{package}](#{foldername}.{package})\n"
    count += 1
readme += "\n"

for package, info in dataStruct[foldername].items():
    readme += f"# {package}\n{info['doc']}.\n```py\nfrom {foldername}.{package} import *\n```\n\n"
    for func, funcINFO in info["funcs"].items():
        readme += f"- **{func}**\n```{funcINFO}.\n```\n"
with open("ModuleEnd.txt", "r") as f3:
    readme += f3.read()

#print(readme)
#######################################################

if os.path.exists("README.md"):
    os.remove("README.md")
with open("README.md", "x") as f:
    f.write(readme)