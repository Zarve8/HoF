import os
from copy import deepcopy
from PIL import Image
import numpy as np


def img_to_numpy(file, im=None):
    if im is None:
        im = Image.open(file)
    pix = im.load()
    x_size, y_size = im.size
    a = np.zeros((x_size, y_size, 4))
    for i in range(0, x_size):
        for j in range(0, y_size):
            a[i][j] = pix[i, j]
    return a


def convert_to_color(x):
    return (min(255, max(0, int(x[0]))), min(255, max(0, int(x[1]))), min(255, max(0, int(x[2]))), min(255, max(0, int(x[3]))))


def numpy_to_img(a, file=None):
    x_size, y_size, z_size = a.shape
    im = Image.new('RGBA', (x_size, y_size), (0, 0, 0, 0))
    pix = im.load()
    for i in range(0, x_size):
        for j in range(0, y_size):
            pix[i, j] = convert_to_color(a[i][j])
    if file is None:
        return im
    im.save(file)


def numpy_to_jpeg(a, file):
    x_size, y_size, z_size = a.shape
    im = Image.new('RGB', (x_size, y_size), (0, 0, 0, 0))
    pix = im.load()
    for i in range(0, x_size):
        for j in range(0, y_size):
            pix[i, j] = convert_to_color(a[i][j])
    im.save(file)


def cut_minimal(a):
    x_size, y_size, z_size = a.shape
    top, bottom, right, left = -1, -1, -1, -1
    for i in range(0, x_size):
        if top >= 0:
            break
        for j in range(0, y_size):
            if a[i][j][3] != 0.0:
                top = i
                break
    for i in range(x_size - 1, -1, -1):
        if bottom >= 0:
            break
        for j in range(0, y_size):
            if a[i][j][3] != 0.0:
                bottom = i
                break
    for j in range(0, y_size):
        if left >= 0:
            break
        for i in range(0, x_size):
            if a[i][j][3] != 0.0:
                left = j
                break
    for j in range(y_size-1, -1, -1):
        if right >= 0:
            break
        for i in range(0, x_size):
            if a[i][j][3] != 0.0:
                right = j
                break
    xx_size = bottom - top + 1
    yy_size = right - left + 1
    b = np.zeros((xx_size, yy_size, 4))
    for i in range(0, xx_size):
        for j in range(0, yy_size):
            b[i][j] = a[i+top][j+left]
    return b


def overlay(a, b):
    ta = (a[3]/255)
    tb = 1.0 - ta
    return (a[0]*ta+b[0]*tb, a[1]*ta+b[1]*tb, a[2]*ta+b[2]*tb, min(255, a[3]+b[3]))


def apply(a, b, func, shift_x=0, shift_y=0, copy=None):
    if copy is None:
        copy = b
    else:
        copy = deepcopy(b)
    x_size, y_size, z_size = a.shape
    for i in range(0, x_size):
        for j in range(0, y_size):
            copy[i+shift_x][j+shift_y] = func(a[i][j], b[i+shift_x][j+shift_y])
    return copy


def resize(a, x, y=None):
    x_size, y_size, z_size = a.shape
    if y is None:
        y = int((x * y_size) / x_size)
    im = numpy_to_img(a)
    im = im.resize((x, y))
    print("Size:", x, y)
    return img_to_numpy("", im)


def load_user_preview(id):
    filepath = "files/work_on_wall_" + id.__str__() + ".jpg"
    if os.path.exists(filepath):
        return open(filepath, 'rb')
    else:
        return None


def print_to_wall(filepath, new_path):
    a = img_to_numpy(filepath)
    b = img_to_numpy('files/wall.png')
    a = cut_minimal(a)
    x_size, y_size, z_size = a.shape
    y = (1000 * y_size) / x_size  # x = 1000px, original ratio
    w = 420 - y  # w+y = 420px
    print(y, w)
    if w >= 0:
        a = resize(a, 1000)
        a = apply(a, b, overlay, 100, 240+int(w/2))
        print(100, 240+int(w/2))
    else:
        x = (420 * x_size) / y_size
        a = resize(a, int(x))
        a = apply(a, b, overlay, 100+int((1000-x)/2), 240)
        print(100+int((1000-x)/2), 240)
    numpy_to_jpeg(a, new_path)
