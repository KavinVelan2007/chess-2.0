#!/bin/bash

echo "Press enter to copy clouds and trim here."
read

set -exu

rm -f *.png
cp -r ../raw_clouds/*.png .
find . -name "*.png" -exec convert {} -trim {} \;
