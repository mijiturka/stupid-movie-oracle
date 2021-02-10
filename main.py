import os
import random
from PIL import Image

posters_path = './movies'

movies = os.listdir(posters_path)
tonight_we_watch = random.choice(movies)

poster = Image.open(os.path.join(posters_path, tonight_we_watch))
poster.show()

print(tonight_we_watch)
