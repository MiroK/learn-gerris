import matplotlib.pyplot as plt
import numpy as np
import os, re


RED = '\033[1;37;31m%s\033[0m'


def parse_csrv(dir_path, save_data=False):
    '''
    Plot time evo of kinetic, potential and mass conservation.
    '''
    assert os.path.isdir(dir_path)

    mass = filter(lambda f: 'mass' in f, os.listdir(dir_path))
    energy = filter(lambda f: 'kinetic' in f or 'potential' in f, os.listdir(dir_path))

    if mass:
        assert len(mass) == 1, 'Multiple mass files'
        mass = mass.pop()
        path = os.path.join(dir_path, mass)
        plot_mass_csrv(path)
    else:
        print 'Mass csrv file missing'

    if energy:
        assert len(energy) == 2, 'Invalid energy files %r' % energy
        # Kinetic, potential
        paths = [os.path.join(dir_path, f) for f in sorted(energy)]
        print paths

        plot_energy_csrv(*paths)
    else:
        print 'Energy csrv missing'

    plt.show()

    
def read_data(path, time_list, sum_list):
    '''A line in data looks like "what time: Value sum: Value'''
    t_pattern = re.compile(r"time:\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
    s_pattern = re.compile(r"sum:\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")

    with open(path) as f:
        for line in f:
            print line
            # time: num
            match = t_pattern.search(line).group(0)
            assert match
            _, t = match.split(':')
            time_list.append(float(t))

            # sum:    num
            match = s_pattern.search(line).group(0)
            assert match
            _, m = match.split(':')
            sum_list.append(float(m))


def plot_mass_csrv(path):
    '''t vs total mass.'''
    time, mass = [], []
    read_data(path, time, mass)
            
    # IDEA mass is supposed to be conserved, plot relative to base init
    mass = np.array(mass)
    mass0 = mass[0]
    mass -= mass0
    print RED % ('\t Initial mass %g' % mass0)

    # Relative
    error = np.abs(mass)/mass0

    fig, ax1 = plt.subplots()
    ax1.plot(time, mass, 'b-')
    ax1.set_xlabel('time')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Sum (chi * rho * dV) - m0', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(time, error, 'r.')
    ax2.set_ylabel('|Sum (chi * rho * dV) - m0|/m0', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    
    return fig


def plot_energy_csrv(kin_path, pot_path):
    '''t vs total mass.'''
    kin_time, kinetic = [], []
    read_data(kin_path, kin_time, kinetic)

    pot_time, potential = [], []
    read_data(pot_path, pot_time, potential)
    
    potential = np.array(potential)
    # potential0 = potential[0]
    # potential -= potential0
    potential *= -1
    
    fig, ax1 = plt.subplots()
    l1, =ax1.plot(kin_time, kinetic, 'bo-', label='E_K')
    l2, = ax1.plot(pot_time, potential, 'gx-', label='E_P')
    ax1.set_xlabel('time')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Sum (chi * rho * v ^ 2 * dV); Sum (chi * g * rho * y * dV)')

    if len(kin_time) != len(pot_time):
        return fig

    if np.linalg.norm(np.array(kin_time) - np.array(pot_time), np.inf) < 1E-13:
        energy = np.array(kinetic) - potential
        ax2 = ax1.twinx()
        ax2.plot(kin_time, energy, 'r.')
        ax2.set_ylabel('E_K+E_P', color='r')
        ax2.tick_params('y', colors='r')

    fig.tight_layout()
    fig.legend((l1, l2), ('E_K', 'E_P'), loc='best')
    
    return fig            
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    sys.exit(parse_csrv(sys.argv[1], save_data=False))
