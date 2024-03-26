#!/usr/bin/env python
# coding: utf-8

# # RGB PAL text writer for Python colormaps

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pyart # Only needed if you are planning to export Py-ART colormaps
# https://arm-doe.github.io/pyart/examples/plotting/plot_choose_a_colormap.html

def export_cmap_as_pal_txt(colormap = 'viridis', field = 'BR', units = 'DBZ', min = -25., max = 75., nlevels = 21, unique = True):
    '''
    Function to produce a PAL-formatted text file from any registered Python colormap, for use in WCT or GRLevelX.
    Input:
        colormap (str): the name of a colormap available in the current name space
        field (str): the name of the variable that this colormap will be used to plot
        units (str): the units of the variable in 'field'
        min (float): The lower end of the color scale
        max (float): The upper end of the color scale
        nlevels (int): The number of steps in the color scale.
        unique (bool): If true, a line will be written out for "range folded" (RF) values (default 800)
    Output:
        Writes out a PAL-formatted text file 'colormap_name.pal' in the current directory.
    '''
    levels, step = np.linspace(min, max, nlevels, retstep = True)
    cmap = mpl.colormaps[colormap]
    # Get the RGB values for each color in the colormap
    rgb_triplets = []
    for i in range(nlevels):
        rgb = cmap(i/(nlevels-1))[:3]  # Extract RGB values, scale from 0 to 1
        rgb_triplets.append((levels[i], int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
    
    with open('./' + colormap + '_' + field +'.pal', "w") as f:
        f.write('Product: ' + field + '\n')
        f.write('Units:   ' + units + '\n')
        # If the field is correlation coefficient, values need to be scaled by 100 to plot correctly, 
        # and the "step" argument is not needed.
        if field == 'CC':
            f.write('Scale: 100\n')
        else:
            f.write('Step: ' + str(step) + '\n')
        f.write('\n')
        # Must list colors in decreasing order, or the color scale in WCT will look strange.
        for triplet in rgb_triplets[::-1]:
            f.write('Color: %5.2f  %4d %4d %4d 255\n'%triplet)
        if unique: # Special color for 'range folded' or censored data - royal purple
            f.write('Unique: 800 \"RF\"    119   0  125\n')

# # Example usage

# Base reflectivity with colormap pyart_HomeyerRainbow
export_cmap_as_pal_txt('pyart_HomeyerRainbow', 'BR', 'DBZ', -25., 75., 21, True)

# ZDR with Matplotlib colormap Spectral
export_cmap_as_pal_txt('Spectral_r', 'ZDR', 'DB', -1., 5., 7, True)

# PhiDP with Matplotlib colormap YlGnBu
export_cmap_as_pal_txt('YlGnBu_r', 'PDP', 'DEG', 0., 200., 6, True)

# Base velocity with Matplotlib colormap RdBu
export_cmap_as_pal_txt('RdBu_r', 'BV', 'KTS', -70., 70., 15, True)

# Correlation coefficient with colormap pyart_HomeyerRainbow
# Note: a line "Scale: 100" needs to be added to the resulting text file for this PAL file to work properly. 
export_cmap_as_pal_txt('pyart_HomeyerRainbow', 'CC', 'Unitless', 20., 100., 9, True)

# Specific differential phase with Matplotlib colormap inferno
export_cmap_as_pal_txt('inferno', 'KDP', 'DEG/KM', -2., 7., 10, True)

# Spectrum width with Matplotlib colormap plasma
export_cmap_as_pal_txt('plasma', 'SW', 'KTS', 0., 30., 11, True)

## Original version of code suggested by ChatGPT 4.0 on 3/7/2024
#import matplotlib.pyplot as plt
#
## Define the number of levels
#N = 256
#
## Create a sample colormap
#cmap = plt.get_cmap('viridis')
#
## Get the RGB values for each color in the colormap
#rgb_triplets = []
#for i in range(N):
#    rgb = cmap(i/(N-1))[:3]  # Extract RGB values, scale from 0 to 1
#    rgb_triplets.append((int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
#
## Export RGB triplets to plain text file
#with open('viridis.pal', 'w') as f:
#    for triplet in rgb_triplets:
#        f.write('{} {} {}\n'.format(*triplet))