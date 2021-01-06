import numpy as np 

from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

# plot normals' x y z components
def plot_normal(normal_map):
    fig, axes = plt.subplots(nrows=1, ncols=3)
    plt.suptitle("Recovered normal field")
    titles = ['x', 'y','z']
    for i, ax in enumerate(axes.flat):
        ax.set_axis_off()
        ax.set_title(titles[i])
        im = ax.imshow(normal_map[:, :, i], cmap=plt.cm.RdBu, vmin=-1, vmax=1) # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.imshow.html
        # cmap: https://matplotlib.org/examples/color/colormaps_reference.html
        # tutorial: https://matplotlib.org/tutorials/introductory/images.html
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.4) # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.colorbar.html
    plt.show()

def plot_albedo(albedo_map):
    h,w = albedo_map.shape
    albedo = np.zeros((h,w,3)) # create a rgb image
    for i in range(3):
        albedo[:,:,i] = albedo_map/np.max(albedo_map) # normalize
    plt.suptitle("Recovered albedo")
    plt.imshow(albedo)
    plt.show()

def plot_surface(height_map):
    figure = plt.figure()
    ax = Axes3D(figure)
    h,w = height_map.shape
    y = np.linspace(0, h-1, h)
    x = np.linspace(0, w-1, w)
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, height_map, rstride=1, cstride=1) # https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
    plt.show()

def plot_face(height_map, albedo_map):
    h,w = albedo_map.shape
    albedo = np.zeros((h,w,3)) # create a rgb image
    for i in range(3):
        albedo[:,:,i] = albedo_map/np.max(albedo_map) # normalize

    figure = plt.figure()
    ax = Axes3D(figure)
    y = np.linspace(0, h-1, h)
    x = np.linspace(0, w-1, w)
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, height_map, facecolors=albedo, rstride=1, cstride=1)
    plt.show()

def plot_data(images):
    fig, axes = plt.subplots(nrows=8, ncols=8)
    plt.suptitle("Raw Data")
    for i, ax in enumerate(axes.flat):
        ax.set_axis_off()
        im = ax.imshow(images[:, :, i], cmap=plt.cm.gray)
    plt.show()












