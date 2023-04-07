from multiprocessing import Pool

import functions
from config import *

if __name__ == "__main__":
    with open(TXT_WITH_PRIVATE_KEYS) as file:
        list_of_private_keys = [line.strip() for line in file.readlines()]

    with Pool(NUMBER_OF_MULTIPROCESSINGS) as p:
        answer = p.map(functions.main_function, list_of_private_keys)