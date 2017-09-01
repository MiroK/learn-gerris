import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from math import pi


def parse_bubbles(path):
    '''
    Plots time evo of particles counts, histogram of time-ansambled particles,
    and history of radius distribution.
    '''    
    # Data for the time series
    series = defaultdict(list)
    with open(path, 'r') as f:
        for line in f:
            time, _, volume = line.strip().split()
            
            radius = (3*float(volume)/4/pi)**(1/3.)    
            series[time].append(float(radius))
            
    # How many particles in each time instance
    times, counts = zip(*[(float(time), len(particles))
                           for time, particles in series.iteritems()])

    plt.figure()
    plt.plot(times, counts, 'bo')
    plt.xlabel("time")
    plt.ylabel("particle count")
    
    # Smallest and largest redius recorded
    rmax = max(max(time_instance) for time_instance in series.itervalues())
    rmin = min(min(time_instance) for time_instance in series.itervalues())
    print 'Total particles', sum(counts), 'radii between', rmin, rmax

    # Time ansambled radius representation
    all_radii = np.hstack(series.values())

    plt.figure()
    plt.hist(all_radii)

    plt.show()

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    sys.exit(parse_bubbles(sys.argv[1]))
