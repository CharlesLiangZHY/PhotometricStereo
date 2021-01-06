import os
import re

import numpy as np
from PIL import Image

def parse(filename):
    chunks = re.split(r'A|E',filename[0:-4])
    A = int(chunks[1])
    E = int(chunks[2])
    return [A, E]

### Transform spherical coordinates into cartesian coordinate
def sph2cart(theta, phi, r=1): # theta is elevation and phi is azimuth
    '''
        y
        |
        |____ x
       /
     z
    '''
    z = r * np.cos(theta/180 * np.pi) * np.cos(phi/180 * np.pi)
    x = r * np.cos(theta/180 * np.pi) * np.sin(phi/180 * np.pi)
    y = r * np.sin(theta)
    return np.array([x,y,z])


def load_dataset(path):
    files = [filename for filename in os.listdir(path) if re.match(r'.*\.pgm', filename) and (not re.match(r'.*_Ambient\.pgm', filename))]
    h, w = np.array(Image.open(os.path.join(path, files[0]))).shape
    images = np.zeros((h, w, len(files)))
    source = np.zeros((len(files), 3))
    for i, filename in enumerate(files):
        A, E = parse(filename)
        source[i] = sph2cart(E,A)
        images[:, :, i] = Image.open(os.path.join(path, filename))
    return [images, source]

