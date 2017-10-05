from itertools import groupby
import re, os


def visit_merge_vtk(root, directory='.'):
    '''
    Combine all the files in directory which are like root_pid-iter.vtk
    to a single file to be read by visit.
    '''

    files = filter(lambda f: f.startswith(root) and f.endswith('.vtk'),
                   os.listdir(directory))

    if not files: return 1

    # Compile the regexp for getting cpu and iter info
    pattern = r'([0-9]+)'
    match = re.compile(pattern)

    merge_files, time_stamps = [], []
    for f in files:
        result = match.findall(f)
        if len(result) == 2:
            merge_files.append(f)
            # Order by iter then cpu
            time_stamps.append(tuple(map(int, reversed(result))))
    assert len(time_stamps) == len(merge_files)

    # Assuming data is consisten generate a sorting permutation
    # which orders that data by step number
    sort_perm = sorted(range(len(merge_files)), key=lambda i: time_stamps[i])

    time_stamps = [time_stamps[i] for i in sort_perm]
    # Make sure that the data is consistent, ie each iter has same
    # cpus
    groups = groupby(time_stamps, key=lambda p: p[0])
    get_len = lambda p: len(list(p[1]))
    
    ncpus = get_len(next(groups))
    assert all(get_len(p) == ncpus for p in groups)

    # # Orgfile by the iter number
    merge_files = [merge_files[i] for i in sort_perm]
    
    # We write the visit file in the directory of the files with absolute
    # path to vtk files
    visit = os.path.join(directory, '%s_driver.visit' % root)
    with open(visit, 'w') as out:
        out.write('!NBLOCKS %s\n' % ncpus)
        for f in merge_files:
            out.write('%s\n' % os.path.abspath(f))
    print 'Written', visit
    
    return 0

# -------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    # NOTE visit seems to have problem when there are too many vtk
    # files. By problems I mean opening the file. However, if you
    # comment/delete some files, load the files, uncomment the files 
    # and reload there seems to be no issue
    sys.exit(visit_merge_vtk(*sys.argv[1:]))
