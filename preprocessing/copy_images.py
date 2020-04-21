
import os
import shutil
import sys

dest = sys.argv[1]
src = sys.argv[2]

dest_files = os.listdir(dest)

for f in dest_files:
    if not f.endswith(".xml"):
        continue
    f = f.replace(".xml", ".jpeg")
    if f in dest_files:
        continue
    print(f)
    shutil.copy(
        os.path.join(src, f),
        os.path.join(dest, f)
    )
