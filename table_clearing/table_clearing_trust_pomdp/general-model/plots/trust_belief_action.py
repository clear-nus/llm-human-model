#!/usr/category/env python
import numpy as np
import os
import sys
import ast
from make_plots3 import plot_bar_graph
from make_plots3 import plot


# input parameter
if len(sys.argv) != 6:
    print 'Usage: python trust_belief_action.py num-bottle num-can num-glass discount-factor intervene'
    sys.exit(0)

numBottle = int(sys.argv[1])
numCan = int(sys.argv[2])
numGlass = int(sys.argv[3])
discount = float(sys.argv[4])

numSteps = numBottle + numCan + numGlass

path2img = str(numBottle) + 'bottle-' + str(numCan) + \
        'can-' + str(numGlass) + 'glass-' + str(discount) + \
        '-' + sys.argv[5]
if not os.path.exists(path2img):
    os.mkdir(path2img)

filename = path2img + '.txt'

def act2obj(act):
    if act < numBottle:
        return 'Bottle'
    elif act < numBottle + numCan:
        return 'Can'
    else:
        return 'Glass'

# read data from file
bels = []
actions = []
f = open(filename, 'r')
line = f.readline()
while line != '':
    bels.append(ast.literal_eval(line))
    line = f.readline()
    act = int(line.split()[0])
    actions.append(act2obj(act))
    line = f.readline()


series_colors = ['red']
category_labels = ['1','','','','','','7']

ylabel = r'Prob'
xlabel = r'Trust level'
ylim = ((0,0.5))

for i in range(numSteps):
    title = '$T=%s$, %s' % (i+1, actions[i])
    xval = [1,2,3,4,5,6,7]
    yval1 = bels[i] 

    print path2img
    series_means =  [[xval,yval1]]
    plot(series_means, series_colors,
              plot_title = title,
                 plot_xlabel = xlabel,
                 plot_ylabel = ylabel,
                 plot_ylim = ylim,
                 y_ticks = [0.0,0.5],
                 x_ticks = [1,7],
                 plot_xlabel_coords = (0.5,-0.07),
                 plot_ylabel_coords = (-0.05,0.5),
                savefile_size = (1.32, 1),
                 savefile=path2img + '/T=%s.png' % (i+1))
