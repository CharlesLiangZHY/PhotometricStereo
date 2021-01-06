import numpy as np
from scipy.ndimage.filters import gaussian_filter

### reconstruct surface normal N(x,y) and albedo p(x,y)
def reconstruct_normals(images, S):
    '''
    Lambert's Law: I(x,y) = k*p(x,y)*(N(x,y)*S) = V*g(x,y)
    Here, we assume that the response function of the camera is a linear scaling by factor k.
    Plus, we assume that k = 1, which means there is no distortion.
    Since N is the unit normal, albedo p(x,y) is the  2-norm of g(x,y).
    '''
    h, w, _ = images.shape
    normal_map = np.zeros((h, w, 3))
    albedo_map = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            I = images[i, j, :]
            # Giving the value of each pixel I and source lights V, I(x,y) = V*g(x,y) is a least square problem
            normal, _, _, _ = np.linalg.lstsq(S, I, rcond=None) # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.lstsq.html
            albedo = np.linalg.norm(normal, ord=2) # https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
            normal_map[i, j] = normal / albedo
            albedo_map[i, j] = albedo

    return [normal_map, albedo_map] 

def reconstruct_surface(normal_map, pathNum=1, smooth=False):
    '''
    We can now recover the surface height at any point by integration along gridline path, since we have got the partial derivatives.
    Note that we can get gradient of the height function from the normals of the surface. 
    For robustness, we can take integrals over many different paths and average the results
    '''
    h, w, _ = normal_map.shape
    grad_x = normal_map[:, :, 0] / normal_map[:, :, 2]
    grad_y = normal_map[:, :, 1] / normal_map[:, :, 2]

    maps = np.zeros((h,w,pathNum))
    n = 0
    if n == 0: # intergral along x axis first then y axis
        for y in range(h):
            for x in range(w):
                f = 0.0
                for i in range(x):
                    f += grad_x[0,i]
                for j in range(y):
                    f += grad_y[j,x]
                maps[y,x,n] = f
    if n < pathNum-1:
        n += 1

    if n == 1: # intergral along y axis first then x axis
        for y in range(h):
            for x in range(w):
                f = 0.0
                for i in range(y):
                    f += grad_y[i,0]
                for j in range(x):
                    f += grad_x[y,j]
                maps[y,x,n] = f
    if n < pathNum-1:
        n += 1

    for m in range(n+1, pathNum): # generate random paths
       for y in range(h):
            for x in range(w):
                f = 0.0
                dx = 0
                dy = 0
                while dx < x-1 and dy < y-1:
                    if np.random.randint(2) == 0: # 0 along x ; 1 along y
                        f += grad_x[dy,dx]
                        dx += 1
                    else:
                        f += grad_y[dy,dx]
                        dy += 1
                for i in range(dx, x-1):
                    f += grad_x[dy,i]
                for i in range(dy, y-1):
                    f += grad_y[i,dx]
                maps[y,x,m] = f

    height_map = np.mean(maps, axis=2)
    if smooth:
        height_map = gaussian_filter(height_map, sigma=5) # https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.ndimage.filters.gaussian_filter.html
    return height_map















