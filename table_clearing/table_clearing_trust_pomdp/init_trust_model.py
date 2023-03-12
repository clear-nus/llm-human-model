import numpy as np
import json
from copy import *

RobotAction = {
        0: "Bottle",
        1: "Bottle",
        2: "Bottle",
        3: "Glass"
        }

HumanAction = {
        0: "Intervene",
        1: "Stay put"
        }

numTrustLevels = 10

def InitTrustDynaNoTransfer(path2data):
    # Init human behavioral policy 
    hBehav = {}
    hBehav['Glass Cup'] = [] 
    hBehav['Water Bottle'] = [] 
    for i in range(numTrustLevels):
        hBehav['Glass Cup'].append([1 - i/10.0, i / 10.0])
        inter_water = max(1 - (i + 3) / 10.0, 0)
        hBehav['Water Bottle'].append([inter_water, 1.0 - inter_water])
    hBehav['Glass Cup'] = np.array(hBehav['Glass Cup'])
    hBehav['Water Bottle'] = np.array(hBehav['Water Bottle'])
    
    # Init trust dynamics
    with open(path2data, 'r') as f:
        dyna_table = json.load(f)
    
    trustDyna = {}
    trustDyna[0, 'Water Bottle'] = []
    trustDyna[0, 'Glass Cup'] = []
    for i in range(numTrustLevels):
        tmp = [0] * numTrustLevels
        tmp[i] = 1.0
        trustDyna[0, 'Water Bottle'].append(copy(tmp))
        tmp = [0] * numTrustLevels
        tmp[i] = 1.0
        trustDyna[0, 'Glass Cup'].append(copy(tmp))
    trustDyna[0, 'Water Bottle'] = np.array(trustDyna[0, 'Water Bottle'])
    trustDyna[0, 'Glass Cup'] = np.array(trustDyna[0, 'Glass Cup'])

    trustDyna[1, 'Water Bottle'] = []
    trustDyna[1, 'Glass Cup'] = []
    trustDyna[1, 'Navigation'] = []
    for i in range(numTrustLevels):
        bottlei = min(numTrustLevels - 1, i + dyna_table['Water Bottle'][i])
        tmp = [0] * numTrustLevels
        tmp[bottlei] = 1.0
        trustDyna[1, 'Water Bottle'].append(copy(tmp))
        glassi = min(numTrustLevels - 1, i + dyna_table['Glass Cup'][i])
        tmp = [0] * numTrustLevels
        tmp[glassi] = 1.0
        trustDyna[1, 'Glass Cup'].append(copy(tmp))
        navi = min(numTrustLevels - 1, i + dyna_table['Navigation'][i])
        tmp = [0] * numTrustLevels
        tmp[navi] = 1.0
        trustDyna[1, 'Navigation'].append(copy(tmp))
    trustDyna[1, 'Water Bottle'] = np.array(trustDyna[1, 'Water Bottle'])
    trustDyna[1, 'Glass Cup'] = np.array(trustDyna[1, 'Glass Cup'])
    trustDyna[1, 'Navigation'] = np.array(trustDyna[1, 'Navigation'])

    return trustDyna, hBehav


def InitTrustDynaTransfer(path2data):
    # Init human behavioral policy 
    hBehav = {}
    hBehav['Glass Cup'] = [] 
    hBehav['Water Bottle'] = [] 
    for i in range(numTrustLevels):
        hBehav['Glass Cup'].append([1 - i/10.0, i / 10.0])
        inter_water = max(1 - (i + 3) / 10.0, 0)
        hBehav['Water Bottle'].append([inter_water, 1.0 - inter_water])
    hBehav['Glass Cup'] = np.array(hBehav['Glass Cup'])
    hBehav['Water Bottle'] = np.array(hBehav['Water Bottle'])
    
    # Init trust dynamics
    with open(path2data, 'r') as f:
        dyna_table = json.load(f)
    
    trustDyna = {}
    trustDyna[(0, 'Water Bottle')] = []
    trustDyna[(0, 'Glass Cup')] = []
    for i in range(numTrustLevels):
        tmp = [0] * numTrustLevels
        tmp[i] = 1.0
        trustDyna[(0, 'Water Bottle')].append(copy(tmp))
        tmp = [0] * numTrustLevels
        tmp[i] = 1.0
        trustDyna[(0, 'Glass Cup')].append(copy(tmp))
    trustDyna[(0, 'Water Bottle')] = np.array(trustDyna[(0, 'Water Bottle')])
    trustDyna[(0, 'Glass Cup')] = np.array(trustDyna[(0, 'Glass Cup')])

    trustDyna[(1, 'Water Bottle')] = {} 
    trustDyna[(1, 'Glass Cup')] = {}
    list_tasks = ["Navigation", "Glass Cup", "Water Bottle"]
    for ptask in list_tasks:
        trustDyna[(1, 'Water Bottle')][ptask] = []
        trustDyna[(1, 'Glass Cup')][ptask] = []
        for i in range(numTrustLevels):
            bottlei = min(numTrustLevels - 1, i + dyna_table[ptask]['Water Bottle'][i])
            tmp = [0] * numTrustLevels
            tmp[bottlei] = 1.0
            trustDyna[(1, 'Water Bottle')][ptask].append(copy(tmp))
            glassi = min(numTrustLevels - 1, i + dyna_table[ptask]['Glass Cup'][i])
            tmp = [0] * numTrustLevels
            tmp[glassi] = 1.0
            trustDyna[(1, 'Glass Cup')][ptask].append(copy(tmp))
        trustDyna[(1, 'Water Bottle')][ptask] = np.array(trustDyna[(1, 'Water Bottle')][ptask])
        trustDyna[(1, 'Glass Cup')][ptask] = np.array(trustDyna[(1, 'Glass Cup')][ptask])

    print 'trust dyna: ', trustDyna

    return trustDyna, hBehav
