#!/bin/sh

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.


adaptivity=0
nprocs=0  # This is 2^0
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

SAVEDIR="./data/ampl"$amplitude"_adapt"$adaptivity"_p"$nprocs

if [ ! -d $SAVEDIR ]; then
    mkdir -p $SAVEDIR
else
    rm -rf $SAVEDIR/*
fi

cp input.gfs $SAVEDIR
cd $SAVEDIR


if [ $nprocs -gt 0 ]; then
    # First parallelize domain to 2^nprocs domains
    gerris2D -p $nprocs -DAMPLITUDE=$amplitude -DADAPTIVITY=$adaptivity input.gfs > pinput.gfs
    
    p=$(echo "2 ^ $nprocs" | bc)
    echo "Running: Amplitude "$amplitude" Adaptivity "$adaptivity" nprocs "$p

    mpirun -np $p gerris2D pinput.gfs
else
    p=$(echo "2 ^ $nprocs" | bc)
    echo "Running: Amplitude "$amplitude" Adaptivity "$adaptivity" nprocs "$p

    gerris2D -DAMPLITUDE=$amplitude -DADAPTIVITY=$adaptivity input.gfs
fi

