def dieable(movies, sides):
    if len(movies) == sides:
        return movies
    if len(movies) > sides:
        # Pick the first n
        return movies[:sides]
    if len(movies) < sides:
        # Fill in with duplicate options, starting from the beginning of the list
        return (movies*sides)[:sides]
