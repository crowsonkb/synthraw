"""Synthesizes a DNG file from an image."""

import argparse

import numpy as np
from PIL import Image

from synthraw import DNG

SRGB_MATRIX = [[3.2406, -1.5372, -0.4986],
               [-0.9689, 1.8758, 0.0415],
               [0.0557, -0.2040, 1.0570]]


def main():
    """The main function."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='input image file')
    ap.add_argument('output', help='output DNG file')
    args = ap.parse_args()

    image = np.float32(Image.open(args.input).convert('RGB'))
    image = np.uint16((image / 255)**2.2 * 65535)
    data = np.zeros(image.shape[:2], np.uint16)
    data[::2, ::2] = image[::2, ::2, 0]
    data[::2, 1::2] = image[::2, 1::2, 1]
    data[1::2, ::2] = image[1::2, ::2, 1]
    data[1::2, 1::2] = image[1::2, 1::2, 2]

    dng = DNG(args.output)
    dng.set_matrix(SRGB_MATRIX)
    dng.write_data(data)
    dng.close()

if __name__ == '__main__':
    main()
