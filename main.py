import os
import random
from PIL import Image
import time

print(1)
time.sleep(0.1)
print(2)
time.sleep(0.1)
print(3)
time.sleep(0.1)
print('Очаквам да знаеш за Екзюпари')
time.sleep(1)

posters_path = './movies'

movies = os.listdir(posters_path)

for i in range(1, 5):
    tonight_we_watch = random.choice(movies)
    poster = Image.open(os.path.join(posters_path, tonight_we_watch))
    poster.show()
    time.sleep(0.1)
