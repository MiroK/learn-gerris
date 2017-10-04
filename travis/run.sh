#!/bin/sh

HOME=`pwd`
echo $HOME
for SIGMA in 0 1
do
    for FILTER in 0 1
    do
        SAVEDIR="./data/sigma"$SIGMA"_filter"$FILTER

        if [ ! -d $SAVEDIR ]; then
            mkdir -p $SAVEDIR
        else
            rm -rf $SAVEDIR/*
        fi

        cp input.gfs $SAVEDIR
        cd $SAVEDIR

        echo "Running:"$SIGMA"-"$FILTER

        gerris2D -DSIGMA=$SIGMA -DFILTER=$FILTER input.gfs > /dev/null &

        cd $HOME
    done
done
        
