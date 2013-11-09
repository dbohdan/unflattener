#!/bin/sh
python unflatter.py
convert result.png zombie-normal-spritelamp-scaled.png -compose difference -composite -evaluate Pow 2 -separate -evaluate-sequence Add -evaluate Pow 0.5 diff.png
