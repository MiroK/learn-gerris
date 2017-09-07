import matplotlib.pyplot as plt
import numpy as np
import os, re


RED = '\033[1;37;31m%s\033[0m'


def read_data(path, data):
    '''A line in data looks like "what time: Value sum: Value'''
    keys = data.keys()
    patterns = [re.compile(r"%s:\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?" % key)
                for key in keys]

    with open(path) as f:
        for line in f:
            for key, pattern in zip(keys, patterns):
                match = pattern.search(line).group(0)
                assert match
                _, value = match.split(':')
                data[key].append(float(value))

                
def parse_position(dir_path, save=False):
    '''Plot time evo of time step.'''
    assert os.path.isdir(dir_path)

    path = filter(lambda f: 'position' in f, os.listdir(dir_path))
    assert len(path) == 1
    path = path.pop()
    path = os.path.join(dir_path, path)
    
    data = {'time': [], 'infty': []}
    read_data(path, data)
    time, height = data['time'], data['infty']
    
    fig = plt.figure()
    plt.plot(time, height)
    plt.xlabel("time")
    plt.ylabel("height")

    plt.show()

# -------------------------------------------------------------------    

if __name__ == '__main__':
    import sys

    path = sys.argv[1]

    sys.exit(parse_position(path))
