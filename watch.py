import pathvalidate
import pathlib
from datetime import datetime
import json
import logging

def input_movie():
    movie = input('What movie are we watching tonight?\n')
    logging.debug(f'Watching {movie}')

    return (
        pathvalidate.sanitize_filename(movie)
        .replace(' ', '-')
        .lower()
        )

def start():
    return input('Ready???\n')

def input_fun_value():
    value = input('Here we go! Press Ctl+D to end\n')
    return (datetime.now(), value)

def viewing_data(start, end, fun):
    return {
        'start': start,
        'end': end,
        'fun': fun
    }

def report(start, end, raw_fun):
    # Pretty-print a viewing report

    by_scene = {
        'start': start.strftime('%a %d/%m/%Y %H:%M:%S'),
        'end': end.strftime('%a %d/%m/%Y %H:%M:%S'),
        'fun': {}
    }
    # Return fun values by scene time from the beginning of the movie
    for timestamp in raw_fun.keys():
        scene = timestamp - start
        by_scene['fun'][str(scene)] = raw_fun[timestamp]

    return json.dumps(by_scene, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Prep for the collection
    movie = input_movie()
    logging.debug(f'Usable movie name is {movie}')


    # Start collecting the fun values
    start()
    beginning = datetime.now()

    fun = {}
    try:
        while True:
            timestamp, value = input_fun_value()
            # Replace previous value if it exists.
            # Makes the dictionary more manageable.
            # It's very unlikely that we'll be able to squeeze two values in at the same microsecond, especially with all the I/O going on.
            # If we somehow do, we won't lose much by replacing the previous value.
            fun[timestamp] = value
    except EOFError:
        logging.info('END')

    end = datetime.now()


    # Save the fun values
    logging.debug(f'Fun values: {fun}')

    path = pathlib.Path(f'./{movie}.json')
    path.write_text(str(viewing_data(beginning, end, fun)))
    logging.info(f'Fun values written to {path}')

    path = pathlib.Path(f'./{movie}_report.json')
    path.write_text(report(beginning, end, fun))
    logging.info(f'Fun values report written to {path}')
