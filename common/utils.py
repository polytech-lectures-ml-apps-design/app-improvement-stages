import logging
import os
import pickle
import re
import time
import uuid
from multiprocessing import Pool, Process
from multiprocessing import cpu_count


def parse_input_string(s):
    pattern = re.compile(r"(\d+(?:\.\d+)?)")
    return re.findall(pattern, s)


def load_classifier(model_pickle_path: str):
    model_pickle_path = os.path.join(os.path.dirname(__file__), model_pickle_path)
    with open(model_pickle_path, 'rb') as p:
        clf = pickle.load(p)
        return clf


class CpuLoadGenerator:
    def __init__(self, interval: float):
        self.interval = interval

    def __call__(self, x):
        start_time = time.time()
        while time.time() - start_time < self.interval:
            x * x  # cpu load, just some calculations


def load_all_cpus(interval: float):
    """
    Produces load on all available CPU cores during given time interval
    """
    num_processes = cpu_count()
    logging.debug(f"Utilizing {num_processes} cores\n")

    pool = Pool(num_processes)
    pool.map(CpuLoadGenerator(interval), range(num_processes))


def generate_task_id():
    return uuid.uuid4()
