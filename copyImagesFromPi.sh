#!/bin/bash
DEST="$1"
[[ -n "$DEST" ]] || DEST="cat"
rsync -va "douglas@pi:webdata/camera/" "$DEST"
