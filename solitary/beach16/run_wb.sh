#!/bin/sh

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

GFSINPUT=wall_on_beach.gfs

adaptivity=0
nprocs=1  # This is 2^0
amplitude=0
while getopts "H:ap:" opt; do
    case $opt in
    H)
        amplitude=$OPTARG;
        ;;
    a)
        adaptivity=1
        ;;
    p)
        nprocs=$OPTARG
        ;;
    \?)
        echo "Illegal option"
        exit 1
        ;;
    esac
done

SAVEDIR="./data/wb_ampl"$amplitude"_adapt"$adaptivity"_p"$nprocs

if [ ! -d $SAVEDIR ]; then
    mkdir -p $SAVEDIR
else
    rm -rf $SAVEDIR/*
fi

cp $GFSINPUT $SAVEDIR
cd $SAVEDIR


echo "Running: Amplitude "$amplitude" Adaptivity "$adaptivity" nprocs "$nprocs
if [ $nprocs -gt 1 ]; then
    # First parallelize domain to 2^nprocs domains
    gerris2D -b $nprocs -DAMPLITUDE=$amplitude -DADAPTIVITY=$adaptivity $GFSINPUT > pinput.gfs
    echo 'Done partitioning'
    mpirun -np $nprocs gerris2D pinput.gfs
else
    gerris2D -DAMPLITUDE=$amplitude -DADAPTIVITY=$adaptivity $GFSINPUT
fi
