import numpy as np
import matplotlib.pyplot as plt
import random
import os
from PIL import Image


def gabor_patch(size, lambda_, theta, sigma, phase, trim = .005, random_gamma = False):
    """Create a Gabor Patch

    size : int
        Image size (n x n)

    lambda_ : int
        Spatial frequency (px per cycle)

    theta : int or float
        Grating orientation in degrees

    sigma : int or float
        gaussian standard deviation (in pixels)

    phase : float
        0 to 1 inclusive
    """
    # make linear ramp
    X0 = (np.linspace(1, size, size) / size) - .5

    # Set wavelength and phase
    freq = size / float(lambda_)
    phaseRad = phase * 2 * np.pi

    # Make 2D grating
    Xm, Ym = np.meshgrid(X0, X0)

    # Change orientation by adding Xm and Ym together in different proportions
    thetaRad = (theta / 360.) * 2 * np.pi
    Xt = Xm * np.cos(thetaRad)
    Yt = Ym * np.sin(thetaRad)
    grating = np.sin(((Xt + Yt) * freq * 2 * np.pi) + phaseRad)

    # randimize brightness
    if random_gamma:
        grating += random.randint(-5, 5) / 10.0

    # 2D Gaussian distribution
    gauss = np.exp(-((Xm ** 2) + (Ym ** 2)) / (2 * (sigma / float(size)) ** 2))

    # Trim
    gauss[gauss < trim] = 0

    return grating * gauss

def crate_sheet(image_size, width, height):
    out_dir = "sheets"
    plt.gray()
    print("Output directory = " + out_dir)
    list_im = []

    for i in range(1, width * height + 1):
        spatial_freq = image_size / random.randint(5, 10)
        orientation = 10 * random.randint(0, 18)
        sigma = image_size / random.randint(6, 10)
        phase = random.randint(0, 1)
        img = gabor_patch(image_size, spatial_freq, orientation, sigma, phase, .005, False)
        file_name = out_dir + "/" + "tmp_gabor_{0}.png".format(str(i).zfill(3))
        plt.imsave(file_name, img)
        list_im.append(file_name)

    # creates a new empty image, RGB mode, and size 444 by 95
    new_im = Image.new('RGB', (width * image_size, height * image_size))
    x_offset = 0;
    y_offset = 0;
    for elem in list_im:
        img = Image.open(elem)
        new_im.paste(img, (x_offset, y_offset))
        x_offset += image_size
        if x_offset >= width * image_size:
            x_offset = 0
            y_offset += image_size
        img.close()
        os.remove(elem)

    output_file_name = out_dir + "/" + "sheet_{0}x{1}.png".format(width, height)
    new_im.save(output_file_name)
    print('File saved as "' + output_file_name + '"');

def create_random_set(count):
    out_dir = "set"
    plt.gray()
    print("Output directory = " + out_dir)
    for i in range(1, count + 1):
        image_size = random.randint(96, 512)
        spatial_freq = image_size / random.randint(5, 10)
        orientation = 10 * random.randint(0, 18)
        sigma = image_size / random.randint(6, 10)
        phase = random.randint(0, 1)
        img = gabor_patch(image_size, spatial_freq, orientation, sigma, phase, .005, True)
        file_name = out_dir + "/" + "gabor_{0}.png".format(str(i).zfill(3))
        print("...saving image " + file_name)
        plt.imsave(file_name, img)

crate_sheet(256, 4, 6)
create_random_set(4)
exit(0)


