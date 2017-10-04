#!/bin/sh

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

adaptivity=0
nprocs=1  # This is 2^0
amplitude=0
wall_height=1.5
while getopts "W:H:ap:" opt; do
    case $opt in
    W)
        wall_height=$OPTARG;
        ;;
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

SAVEDIR="./data/ampl"$amplitude"wall"$wall_height"_adapt"$adaptivity"_p"$nprocs

if [ ! -d $SAVEDIR ]; then
    mkdir -p $SAVEDIR
else
    rm -rf $SAVEDIR/*
fi

cp input.gfs $SAVEDIR
cd $SAVEDIR


echo "Running: Amplitude "$amplitude" Wall "$wall_height" Adaptivity "$adaptivity" nprocs "$nprocs
if [ $nprocs -gt 1 ]; then
    # First parallelize domain to 2^nprocs domains
    gerris2D -b $nprocs -DAMPLITUDE=$amplitude -DADAPTIVITY=$adaptivity input.gfs > pinput.gfs
    
    mpirun -np $nprocs gerris2D pinput.gfs
else
    gerris2D -m ./input.gfs -DAMPLITUDE=$amplitude
    #-DWHEIGHT=$wall_height -DADAPTIVITY=$adaptivity
fi
