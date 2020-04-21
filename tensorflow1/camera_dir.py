import os

def cd_camera_dir():
    if os.path.isdir("/home/douglas/camera"):
        os.chdir("/home/douglas/camera")
    else:
        os.chdir(r"I:\Camera\camera")
