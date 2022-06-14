import os
import shutil
from stl import mesh
import numpy

def recreateDir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        print("created folder: ", path)
    else:
        shutil.rmtree(path)

def checkFileType(obj):
    return "ASCII" if obj.name else "Binary"

def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies

def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz

def fiind_side_sizes(obj):
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(
        obj)
    return maxx - minx, maxy - miny, maxz - minz

def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


def translateToZero(model):
    minpipex, maxpipex, minpipey, maxpipey, minpipez, maxpipez = find_mins_maxs(
        model)
    model.translate(numpy.array(
        [0-minpipex, 0-minpipey, 0-minpipez]))
