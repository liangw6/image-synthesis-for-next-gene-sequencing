import cv2
import numpy as np
import sys
from math import exp
from random import randint
from random import uniform
from random import choice
from itertools import product

# in micrometer
pixel_size = 0.65

maximum_possible_intensity = 65535

# initialize the image
image = np.zeros((100, 100), dtype = np.uint16)
height, width = image.shape

def main():

    if len(sys.argv) != 2:
        print('Usage: python3 simple_synthesis.py project_name')
        sys.exit(1)

    project_name = sys.argv[1]

    global image
    ans_key = []

    # Initialize the image
    for i in range(height):
        for j in range(width):
            image[i][j] += uniform_background()

    for i in range(500):
        x_pos = randint(0, height)
        y_pos = randint(0, width)
        ans_key.append((x_pos, y_pos))
        place_a_cluster(y_pos, x_pos)
        print('.', end='', flush=True)
    # add_poisson_background()
    # image = random_noise(image, mode='poisson')
    # image = (image * maximum_possible_intensity).astype(np.uint16)

    # Add phase
    for i in range(100):
        x_pos = randint(0, height)
        y_pos = randint(0, width)
        place_a_cluster(y_pos, x_pos, strand_per_cluster=40)
        print('.', end='', flush=True)

    cv2.imwrite('simple_{}.tif'.format(project_name), image)
    with open('ans_{}.txt'.format(project_name), 'w') as f:
        for i in ans_key:
            # x_pos, y_pos = i
            f.write('{} {}\n'.format(i[0], i[1]))

def uniform_background(background_base=800, backgroud_variation=0.05):
    """
    return the backgroud value of this pixel

    Parameters:
        background_base: the base of the backgroud
        backgroud_variation: maximum variation of the background
    """
    return background_base + randint(-backgroud_variation * background_base, backgroud_variation * background_base)

def add_poisson_background():
    """
    return original image with poisson background added

    Variable:
        image: because poisson distribution is noise dependent, this image should have clusters already
    """
    global image
    maximum_possible_intensity = 65535 # 2^ 16 - 1
    PEAK = 2.0

    float_image = image.astype(float)
    noisy = np.random.poisson(float_image) #/ maximum_possible_intensity * PEAK) / PEAK * maximum_possible_intensity
    noisy = noisy.astype(np.uint16)
    print(noisy)
    image += noisy




def place_a_cluster(x, y, strand_per_cluster=100, strand_var=0.1, all_cluster_size=range(2, 6)):
    """
    place one cluster

    Parameters:
        strand_per_cluster: the number of DNA strands in one cluster
        strand_var: variation of the above number
        all_cluster_size: the size in which strands are placed
    """
    strand = strand_per_cluster + randint(-strand_var * strand_per_cluster, strand_var * strand_per_cluster)
    for i in range(strand):
        cluster_size = choice(all_cluster_size)
        place_a_strand(uniform((x + 0.5 - cluster_size / 4)*pixel_size, (x + 0.5 + cluster_size / 4)*pixel_size),
                       uniform((y + 0.5 - cluster_size / 4)*pixel_size, (y + 0.5 + cluster_size / 4)*pixel_size))

## TODO: Inefficient
def place_a_strand(pos_x, pos_y, strand_intensity=10, delta=2, effect=3):
    """
    processing the whole image by placing this cluster at a specific position

    Parameters:
        pos_x, pos_y: the position of the strand
        strand_intensity: the intensity of this strand
        delta: determines how fast intensity fades as moving farther away from the strand

    Required Global Parameters:
        height, width: those of the image

    Required Global Variable:
        image: uint16, the image
    """

    effect_range = lambda k: range(int((k - effect) / pixel_size), int((k + effect + 1) / pixel_size))
    for i,j in product(effect_range(pos_x), effect_range(pos_y)):
        if i >= 0 and i < height and j >= 0 and j < width:
            tmp = (i * pixel_size - pos_x)**2 + (j * pixel_size- pos_y)**2
            image[i, j] += round(strand_intensity * exp(-0.5 * delta * tmp))

if __name__ == "__main__":
    main()
