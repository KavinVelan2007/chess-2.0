#!/usr/bin/python3

import os, sys

index=0

for filename in sorted(os.listdir()):

    if not filename.endswith(".png"):
        continue

    index+=1

    new_name="cloud%s.png"%(str(index).zfill(2))
    os.rename(filename,new_name)
