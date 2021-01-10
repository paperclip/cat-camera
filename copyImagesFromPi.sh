#!/bin/bash
DEST="$1"
[[ -n "$DEST" ]] || DEST="cat"
rsync -va "douglas@pi3:webdata/camera/" "$DEST"
