import json
import pathlib
import logging

import argparse

import plotly.express

import utils

def from_report(path):
    return json.loads(path.read_text())

def timestamped(original, zone_name):
    start = utils.localize_if_naive(utils.to_timestamp(original['start']), zone_name)
    end = utils.localize_if_naive(utils.to_timestamp(original['end']), zone_name)

    timezoned = {}
    timezoned['movie'] = original['movie']
    timezoned['start'] = start
    timezoned['end'] = end
    timezoned['fun'] = {}
    for scene in original['fun'].keys():
        timestamp = utils.localize_if_naive(utils.scene_to_timestamp(scene, start), zone_name)
        timezoned['fun'][timestamp] = original['fun'][scene]

    return timezoned

def is_positive(value):
    if not value:
        return False
    return value.count('+') == len(value)

def is_negative(value):
    if not value:
        return False
    return value.count('-') == len(value)

def line_chart(timestamps, fun):
    return plotly.express.line(x=timestamps, y=fun)

def binary_chart(timestams, fun_quality, fun_quantity):
    fig = plotly.graph_objects.Figure()
    fig.add_trace(
        plotly.graph_objects.Scatter(
            x=timestamps,
            y=fun_quality,
            mode='markers',
            marker=dict(
                size=fun_quantity
            ),
            name='Capellyana'
        )
    )
    return fig

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    movie_args = parser.add_mutually_exclusive_group(required=True)
    movie_args.add_argument('--movie', metavar='NAME', type=str,
        help='Usable movie name, e.g as generated by watch.py. \
            Plotter will use it to look for a file \
            and expect it to contain watch data')
    movie_args.add_argument('--file', metavar='PATH', type=str,
        help='File containing watch data')

    args = parser.parse_args()

    if args.movie is not None:
        path = pathlib.Path(f'../../data/{args.movie}_report.json')
    elif args.file is not None:
        path = pathlib.Path(args.file)


    # Get the data
    data = timestamped(from_report(path), 'Europe/London')

    # Massage it to make it more graphable
    timestamps = []
    fun = []
    fun_quality = []
    fun_quantity = []
    # This helps visibilty, but depends on how trigger-happy we've been throughout the movie
    multiplier = 10

    for (timestamp, value) in data['fun'].items():
        quantity = len(value)
        if is_positive(value):
            # Determines where this value would go on the plot
            fun_quality.append(1)
            # Determines size of the representation of this value
            fun_quantity.append(quantity*multiplier)
            # All-in-one value, useful for line charts
            fun.append(quantity)
            timestamps.append(timestamp)
        elif is_negative(value):
            fun_quality.append(-1)
            fun_quantity.append(quantity*multiplier)
            fun.append(-quantity)
            timestamps.append(timestamp)
        else:
            # The record is invalid. We don't want its value or timestamp
            logging.warning(f'Ignoring value {value} at {timestamp}')


    # Prepare the plot

    # fig = line_chart(timestamps, fun)

    fig = binary_chart(timestamps, fun_quality, fun_quantity)

    # Start up a server and serve this one page; display in browser window
    fig.show()