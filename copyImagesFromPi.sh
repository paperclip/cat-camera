#!/bin/bash
DEST="$1"
[[ -n "$DEST" ]] || DEST="camera"
rsync -va "douglas@pi:webdata/camera/" "$DEST"
