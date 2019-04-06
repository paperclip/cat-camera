#!/bin/bash
DEST="$1"
[[ -n "$DEST" ]] || DEST="redboot"
rsync -va "douglas@192.168.1.112:public_html/" "$DEST"
