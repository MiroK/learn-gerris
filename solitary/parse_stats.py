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

        plot_energy_csrv(*paths)
    else:
        print 'Energy csrv missing'

    plt.show()

    
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

                
def plot_mass_csrv(path):
    '''t vs total mass.'''
    data = {'time': [], 'sum': []}
    read_data(path, data)
    time, mass = data['time'], data['sum']
    
    # IDEA mass is supposed to be conserved, plot relative to base init
    mass = np.array(mass)
    mass0 = mass[0]
    mass -= mass0
    print RED % ('\t Initial mass %g' % mass0)

    # Relative
    error = np.abs(mass)/mass0

    fig, ax1 = plt.subplots()
    ax1.plot(time, mass, 'bo-')
    ax1.set_xlabel('time')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Sum (chi * rho * dV) - m0', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    ax2.plot(time, error, 'rd-')
    ax2.set_ylabel('|Sum (chi * rho * dV) - m0|/m0', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    
    return fig


def plot_energy_csrv(kin_path, pot_path):
    '''t vs total mass.'''
    data = {'time': [], 'sum': []}
    read_data(kin_path, data)
    kin_time, kinetic = data['time'], data['sum']
    

    data = {'time': [], 'sum': []}
    read_data(pot_path, data)
    pot_time, potential = data['time'], data['sum']
    
    potential = np.array(potential)
    # potential0 = potential[0]
    # potential -= potential0
    potential *= -1
    
    fig, ax1 = plt.subplots()
    l1, = ax1.plot(kin_time, kinetic, 'bo-', label='E_K')
    l2, = ax1.plot(pot_time, potential-potential[0], 'gx-', label='E_P')
    ax1.set_xlabel('time')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('Sum (chi * rho * v ^ 2 * dV); Sum (chi * g * rho * y * dV)')

    if len(kin_time) != len(pot_time):
        return fig

    if np.linalg.norm(np.array(kin_time) - np.array(pot_time), np.inf) < 1E-13:
        energy = np.array(kinetic) - (potential - potential[0])
        ax2 = ax1.twinx()
        ax2.plot(kin_time, energy, 'r.')
        ax2.set_ylabel('E_K+E_P', color='r')
        ax2.tick_params('y', colors='r')

    fig.tight_layout()
    fig.legend((l1, l2), ('E_K', 'E_P'))
    
    return fig


def parse_dt(dir_path, save=False):
    '''Plot time evo of time step.'''
    assert os.path.isdir(dir_path)

    path = filter(lambda f: 'time' in f, os.listdir(dir_path))
    assert len(path) == 1
    path = path.pop()
    path = os.path.join(dir_path, path)
    
    data = {'t': [], 'dt': []}
    read_data(path, data)
    time, dt = data['t'], data['dt']
    
    fig = plt.figure()
    plt.plot(time, dt)
    plt.xlabel("time")
    plt.ylabel("dt")

    plt.show()

    
def parse_adapt(dir_path, save=False):
    '''Plot time evo of cells created / removed total / total.'''
    assert os.path.isdir(dir_path)

    path = filter(lambda f: 'adapt' in f, os.listdir(dir_path))
    assert len(path) == 1
    path = path.pop()
    path = os.path.join(dir_path, path)

    cpattern, rpattern = (re.compile(r"  Cells created:\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"),
                          re.compile(r"  Cells removed:\s+[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"))

    removed, created = [], []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('Adaptive'): continue
            
            c = cpattern.match(line)
            if c is not None:
                _, value = c.group(0).split(':')
                created.append(int(value))

            r = rpattern.match(line)
            if r is not None:
                _, value = r.group(0).split(':')
                removed.append(int(value))

    total = np.cumsum(created) - np.cumsum(removed)

    time = np.arange(len(total))
    
    fig, axarr = plt.subplots(3, sharex=True)

    # Don't want to see first peak
    created[0] = 0
    axarr[0].plot(time, created, 'r')
    axarr[0].set_ylabel('created')

    axarr[1].plot(time, removed, 'b')
    axarr[1].set_ylabel('removed')

    axarr[2].plot(time, total, 'g')
    axarr[2].set_ylabel('total')

    plt.xlabel('time')
    plt.show()

    
def parse_amplitude(dir_path, ampl, save=False):
    '''Plot time evo of amplitude.'''
    assert os.path.isdir(dir_path)

    path = filter(lambda f: 'yposition' in f, os.listdir(dir_path))
    assert len(path) == 1
    path = path.pop()
    path = os.path.join(dir_path, path)
    
    data = {'time': [], 'infty': []}
    read_data(path, data)
    time, y = data['time'], data['infty']

    path = filter(lambda f: 'xposition' in f, os.listdir(dir_path))
    assert len(path) == 1
    path = path.pop()
    data = np.loadtxt(os.path.join(dir_path, path))
    timex, x = data[:, 1], data[:, 2]

    A = np.vstack([timex, np.ones(len(timex))]).T
    velo, _ = np.linalg.lstsq(A, x)[0]
    # Based on value of g and depth = 1
    print velo, np.sqrt(9.81*1*(1 + ampl/1))

    fig, ax1 = plt.subplots()
    ax1.plot(time, y, 'bo-')
    ax1.set_xlabel('time')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('ampl', color='b')
    ax1.tick_params('y', colors='b')

    # ax2 = ax1.twinx()
    # ax2.plot(timex, x, 'r.')
    # ax2.set_ylabel('x', color='r')
    # ax2.tick_params('y', colors='r')

    fig.tight_layout()    
    
    plt.show()
    
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    assert len(args) >= 2
    save = len(args) == 3

    path, what = args[0], args[1]

    if what == 'csrv':
        sys.exit(parse_csrv(path, save))

    elif what == 'time':
        sys.exit(parse_dt(path, save))

    elif what == 'adapt':
        sys.exit(parse_adapt(path, save))

    else:
        assert what == 'ampl'
        ampl = 0.5
        sys.exit(parse_amplitude(path, ampl, save))
