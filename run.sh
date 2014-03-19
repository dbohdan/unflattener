#!/bin/sh
TEST_DIR=test-images

process_image() {
    python ./unflattener/unflatten.py --top $1-top.png --bottom $1-bottom.png --left $1-left.png --right $1-right.png -o result-$2.png
}

diff_normals () {
    # `convert` is part of ImageMagick.
    convert result-$2.png $1-normal-test.png -compose difference -composite -evaluate Pow 2 -separate -evaluate-sequence Add -evaluate Pow 0.5 diff-$2.png
}

process_image $TEST_DIR/robot robot
#diff_normals robot
