import json
import pathlib
import logging

import plotly.express as px

def from_report(movie):
    path = pathlib.Path(f'../../data/{movie}_report.json')
    return json.loads(path.read_text())

def is_positive(value):
    return value.count('+') == len(value)

def is_negative(value):
    return value.count('-') == len(value)

movie = 'turbulence-3-heavy-metal'
data = from_report(movie)

timestamps = data['fun'].keys()
fun = []

for value in data['fun'].values():
    quantity = len(value)
    if is_positive(value):
        fun.append(quantity)
    elif is_negative(value):
        fun.append(-quantity)
    else:
        logging.warning(f'Ignoring value {value}')

fig = px.scatter(x=timestamps, y=fun)
fig.show()
