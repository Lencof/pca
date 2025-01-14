#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from __future__ import division, print_function
import numpy as np
from PIL import Image

from mypca import mypcp


def bitmap_to_mat(bitmap_seq):
    """from blog.shriphani.com"""
    matrix = []
    shape = None
    for bitmap_file in bitmap_seq:
        img = Image.open(bitmap_file).convert("L")
        if shape is None:
            shape = img.size
        assert img.size == shape
        img = np.array(img.getdata())
        matrix.append(img)
    return np.array(matrix), shape[::-1]


def do_plot(ax, img, shape):
    ax.cla()
    ax.imshow(img.reshape(shape), cmap="gray", interpolation="nearest",
              vmin=0, vmax=255)
    ax.set_xticklabels([])
    ax.set_yticklabels([])


if __name__ == "__main__":
    import sys
    import glob
    import matplotlib.pyplot as pl

    if "--test" in sys.argv:
        M = (10*np.ones((10, 10))) + (-5 * np.eye(10))
        L, S, svd = mypcp(M, verbose=True, svd_method="exact")
        assert np.allclose(M, L + S), "Failed"
        print("passed")
        sys.exit(0)

    gl = glob.glob("/home/vighnesh/images/Escalator/*.bmp")[:500:2]
    M, shape = bitmap_to_mat(gl)
    print(M.shape)
    L, S, _, _ = mypcp(M)

    fig, axes = pl.subplots(1, 3, figsize=(10, 4))
    fig.subplots_adjust(left=0, right=1, hspace=0, wspace=0.01)

    i = 0
    for i in range(10):
        do_plot(axes[0], M[i], shape)
        axes[0].set_title("raw")
        do_plot(axes[1], L[i], shape)
        axes[1].set_title("low rank")
        do_plot(axes[2], S[i], shape)
        axes[2].set_title("sparse")
    pl.show()
