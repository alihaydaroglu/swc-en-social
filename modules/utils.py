import numpy as n
import numpy.lib.recfunctions as rfn
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

def compute_and_add_vectors(experiment, vectors):
    names = []
    datas = []
    dtypes = []
    for vec in vectors.keys():
        names.append(vec+'_ang')
        names.append(vec+'_vec_x')
        names.append(vec+'_vec_y')    
        names.append(vec+'_start_x')
        names.append(vec+'_start_y')
        dtypes += [n.float]*5
        datas += [n.zeros(experiment.shape[0])]*5
    # %%time
    exp = rfn.append_fields(experiment, names, datas, dtypes)
    exp = n.array(exp, exp.dtype)
    for vec in vectors:
        start = vectors[vec][0]
        end = vectors[vec][1]

        if type(start) == tuple:
            start_xs = 0.5*(exp[start[0] + '_x'] + exp[start[1] + '_x'] )
            start_ys = 0.5*(exp[start[0] + '_y'] + exp[start[1] + '_y'] )
        else: 
            start_xs = exp[start + '_x']
            start_ys = exp[start + '_y']

        if type(end) == tuple:
            end_xs = 0.5*(exp[end[0] + '_x'] + exp[end[1] + '_x'] )
            end_ys = 0.5*(exp[end[0] + '_y'] + exp[end[1] + '_y'] )
        else:
            end_xs = exp[end + '_x']
            end_ys = exp[end + '_y']

        vector = n.stack((end_xs-start_xs, end_ys-start_ys),axis=1)
        angles = get_angle(vector, n.array([[1,0]]*vector.shape[0]))
        exp[vec+'_ang'] = angles
        exp[vec+'_vec_x'] = vector[:,0]
        exp[vec+'_vec_y'] = vector[:,1]
        exp[vec+'_start_x'] = start_xs
        exp[vec+'_start_y'] = start_ys

    return exp

def compute_and_add_velocities(experiment, velocities):

    names = []; dtypes = []; datas = []
    for label in velocities:
        names.append(label+'_vel_mag')
        names.append(label+'_vel_ang')
        names.append(label+'_vel_x')
        names.append(label+'_vel_y')    
        dtypes += [n.float]*4
        datas += [n.zeros(experiment.shape[0])]*4

    exp_with_vs = rfn.append_fields(experiment, names, datas, dtypes)
    exp_with_vs = n.array(exp_with_vs, exp_with_vs.dtype)

    for label in velocities:
        vel_x = n.gradient(exp_with_vs[label+'_x'])
        vel_y = n.gradient(exp_with_vs[label+'_y'])
        vel_mag = n.sqrt(vel_x**2 + vel_y**2)
        xy_vec = n.stack((vel_x, vel_y), axis=1)
        vel_ang = get_angle(xy_vec,n.array([[1,0]]*xy_vec.shape[0]) )
        vel_label = label + '_vel'
        exp_with_vs[vel_label + '_mag'] = vel_mag
        exp_with_vs[vel_label + '_ang'] = vel_mag
        exp_with_vs[vel_label + '_x'] = vel_x
        exp_with_vs[vel_label + '_y'] = vel_y

    return exp_with_vs