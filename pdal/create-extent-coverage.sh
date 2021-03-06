#!/bin/bash

# Create a polygon coverage (shapefile) from a .las file
env
set -x

echo Starting translate of "$INPUT_FILE"
LOCALNAME_SRC=`echo "$INPUT_FILE" | sed "s/.*\///" `
echo Translate to "$LOCALNAME_SRC"
S3DIR=`echo "$INPUT_FILE" | sed "s/\/[^\/]\+$/\//"`
echo S3DIR is "$S3DIR"
SHP_ENDING_FILE_NAME=`echo "$LOCALNAME_SRC" | sed "s/\.[^\.]\+$//"`
echo Intermediate name "$SHP_ENDING_FILE_NAME".shp

echo destination requested "$DESTINATION_FILE"
S3DEST_DIR=`echo "$DESTINATION_FILE" | sed "s/\/[^\/]\+$/\//"`
echo "destination placed (may be different) $S3DEST_DIR"

/usr/local/bin/aws s3 cp "$INPUT_FILE" "$LOCALNAME_SRC"

pdal tindex create --tindex "$SHP_ENDING_FILE_NAME".shp --filters.hexbin.threshold=1 --filters.hexbin.edge_size=0.00001 --lyr_name bathymetrycoverage --verbose=Debug "$LOCALNAME_SRC" 2> errors.txt

/usr/local/bin/aws s3 cp . "$S3DEST_DIR" --recursive --exclude "*" --include "$SHP_ENDING_FILE_NAME*"  