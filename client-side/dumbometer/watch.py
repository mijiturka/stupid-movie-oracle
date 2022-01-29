import pathvalidate
import pathlib
from datetime import datetime
import json
import logging

def input_movie():
    full_name = input('What movie are we watching tonight?\n')
    logging.debug(f'Watching {full_name}')

    usable_name = (
        pathvalidate.sanitize_filename(full_name)
        .replace(' ', '-')
        .replace('\'', '')
        .lower()
    )
    return (usable_name, full_name)

def start():
    return input('Ready???\n')

def input_fun_value():
    value = input('Here we go! Press Ctl+D to end\n')
    return (datetime.now(), value)

def viewing_data(name, start, end, fun):
    return {
        'movie': name,
        'start': start,
        'end': end,
        'fun': fun
    }

def report(name, start, end, raw_fun):
    # Pretty-print a viewing report

    by_scene = {
        'movie': name,
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
    movie, movie_full_name = input_movie()
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
    path.write_text(str(viewing_data(movie_full_name, beginning, end, fun)))
    logging.info(f'Fun values written to {path}')

    path = pathlib.Path(f'./{movie}_report.json')
    path.write_text(report(movie_full_name, beginning, end, fun))
    logging.info(f'Fun values report written to {path}')
