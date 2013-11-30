#!/bin/sh
TESTDIR=test-images
python unflatten.py --top $TESTDIR/zombie-top.png --bottom $TESTDIR/zombie-bottom.png --left $TESTDIR/zombie-left.png --right $TESTDIR/zombie-right.png -o result.png
convert result.png $TESTDIR/zombie-normal-test.png -compose difference -composite -evaluate Pow 2 -separate -evaluate-sequence Add -evaluate Pow 0.5 diff.png
