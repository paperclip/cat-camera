
import os

def safemkdir(d):
    try:
        os.makedirs(d)
    except EnvironmentError:
        pass
