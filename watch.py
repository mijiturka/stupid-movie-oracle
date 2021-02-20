import pathvalidate
import pathlib
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
    return input('Here we go! Press Ctl+D to end\n')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Prep for the collection
    movie = input_movie()
    logging.debug(f'Usable movie name is {movie}')


    # Start collecting the fun values
    start()

    fun = []
    try:
        while True:
            fun.append(input_fun_value())
    except EOFError:
        logging.info('END')


    # Save the fun values
    logging.debug(f'Fun values: {fun}')

    path = pathlib.Path(f'./{movie}')
    path.write_text(str(fun))
    logging.info(f'Fun values written to {path}')
