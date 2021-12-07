import numpy as n
from matplotlib import pyplot as plt


def dot(a, b):
    return n.sum(a * b, axis=-1)

def mag(a):
    return n.sqrt(n.sum(a*a, axis=-1))

def get_angle(a, b):
    cosab = dot(a, b) / (mag(a) * mag(b)) # cosine of angle between vectors
    angle = n.arccos(cosab) # what you currently have (absolute angle)

    b_t = b[:,[1,0]] * [1, -1] # perpendicular of b

    is_cc = dot(a, b_t) < 0

    # invert the angles for counter-clockwise rotations
    angle[is_cc] = 2*n.pi - angle[is_cc]
    return 360 - n.rad2deg(angle)

def compare_angles(ang1, ang2, reduce=False):
    if reduce: diff = n.min([(ang1-ang2)%360, 360-((ang1-ang2)%360)], axis=0)
    else: diff = (ang1 - ang2) % 360
    return diff

def plot_rad_hist(diff,n_bins=50, bin_width=0.1, figsize=(8,8), title=None):
    f, ax = plt.subplots(figsize=figsize, subplot_kw = {'projection' : 'polar'})
    hist, bins = n.histogram(diff, bins=n_bins, range=(0,360))
    bins = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)] 
    ax.set_rgrids([])
    bars = ax.bar(n.deg2rad(bins), hist, width=bin_width)
    ax.set_title(title)
    return f, bins, hist