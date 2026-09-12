import random

from config import NOISE_TOPICS

def get_query():
    return random.choice(NOISE_TOPICS)