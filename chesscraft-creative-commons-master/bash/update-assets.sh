#!/bin/bash

# This script updates all art files in this repository using the chesscraft repository.
# First it deletes everything, then it copies from ~/projects/chesscraft

PROJECT_ROOT=$(dirname $(dirname $(realpath $0)))
VENV=$($PROJECT_ROOT/bash/print-venv-path.sh)

if [[ ! -d $VENV ]] ; then
    echo "Aborted. venv not setup: $VENV"
    exit 1
fi

set -exu
cd $PROJECT_ROOT
CHESSCRAFT_ROOT=$HOME/projects/chesscraft
CHESSCRAFT_UNITY_FOLDER=$CHESSCRAFT_ROOT/unity
CHESSCRAFT_PYTHON_FOLDER=$CHESSCRAFT_ROOT/python3
FOLDER="chesscraft-creative-commons"

if [ $(basename $PWD) != "$FOLDER" ] ; then
	echo "Run this script from the folder: $FOLDER"
	exit 1
fi

if [ ! -d $CHESSCRAFT_UNITY_FOLDER ] ; then
	echo "Source directory does not exist: $CHESSCRAFT_UNITY_FOLDER"
	exit 1
fi

if [ ! -d $CHESSCRAFT_PYTHON_FOLDER ] ; then
	echo "Source directory does not exist: $CHESSCRAFT_PYTHON_FOLDER"
	exit 1
fi

# Copy Piece PNGs
PIECES_FOLDER=pieces
rm -rf $PIECES_FOLDER
mkdir -p $PIECES_FOLDER
EXCLUDES="--exclude=*.meta --exclude=*.xcf"
rsync -vr $CHESSCRAFT_UNITY_FOLDER/Assets/Resources/Pieces/ $PIECES_FOLDER/ $EXCLUDES

# Assets/Sprites folders
for sprite_folder in themes board editor splash adventure loot search ; do
	rsync -vr $CHESSCRAFT_UNITY_FOLDER/Assets/Sprites/$sprite_folder . $EXCLUDES
done

# Icons
folder=icons
mkdir -p $folder
rsync -vr $CHESSCRAFT_UNITY_FOLDER/Assets/Sprites/*icon*.png $folder/

# JSON schemas
rm -rf schemas
cp -a $CHESSCRAFT_PYTHON_FOLDER/schemas .

# remove utility files nobody needs to see
for folder in $PIECES_FOLDER adventure loot search ; do
	for extension in py json ; do
		find $PIECES_FOLDER -type f -name "*.$extension" -delete
	done
done
rm -f $PIECES_FOLDER/piece-sprite-map.txt

echo "Generating Previews"

$VENV/bin/python3 $PROJECT_ROOT/python3/generate-previews.py --color-pairs --width=1024 --rows=6 --columns=12

echo "Done."
