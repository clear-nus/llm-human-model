import sys
import scipy.stats as stats
import ast
import numpy as np
from IPython import embed

class OneWayAnova:
    def __init__(self, numfiles, files):
        self.data = {}
        self.files = []
        for i in range(numfiles):
            self.files.append(open(files[i], 'r'))
            self.data[i] = self.DiscountedReturn(self.files[i])

        # print self.data
        self.oneWayAnovaTest()

    def oneWayAnovaTest(self):
        print stats.f_oneway(*self.data.values())
        embed()

    def DiscountedReturn(self, f):
        line = f.readline()
        while line != '':
            if '## return ##' in line:
                line = f.readline()
                return np.array(ast.literal_eval(line.split(':')[1][2:]))
            line = f.readline()

        sys.exit(0)
        return []
        

if __name__=='__main__':
    numfiles = int(sys.argv[1])
    files = []
    for i in range(numfiles):
        files.append(sys.argv[i+2])
    OneWayAnova(numfiles, files)
