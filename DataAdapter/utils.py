import os
import shutil
from colored import fore, style

def recreateDir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print("- created folder: " + fore.YELLOW + path + style.RESET + ", status: " + fore.GREEN + "OK" + style.RESET)

def checkFileType(obj):
    return "ASCII" if obj.name else "Binary"

def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz
