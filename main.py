import os
import random
from PIL import Image
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Print out countdown

logging.info(1)
time.sleep(0.1)
logging.info(2)
time.sleep(0.1)
logging.info(3)
time.sleep(0.1)
logging.info('Очаквам да знаеш за Екзюпари')
time.sleep(1)


# Display some random posters followed by tonight's movie

posters_path = './movies'

movies = os.listdir(posters_path)

for i in range(1, 5):
    tonight_we_watch = random.choice(movies)
    poster = Image.open(os.path.join(posters_path, tonight_we_watch))
    poster.show()
    time.sleep(0.1)
