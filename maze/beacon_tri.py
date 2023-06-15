import math
from scipy.optimize import minimize

class BeaconTri:

    NUM_BEACONS = 3

    # beacon_pos is a list of beacon positions. Each element is a 2-tuple (x, y).
    # x_lim and y_lim are the dimensions of the arena.
    def __init__(self, x_lim, y_lim):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.beacon_pos = []
        self.beacon_dist = []
    
    def reset(self):
        self.beacon_pos = []
        self.beacon_dist = []
    
    def set_beacons(self, beacon_pos):
        if len(beacon_pos) != self.NUM_BEACONS:
            raise ValueError('Wrong number of beacons.')
        self.beacon_pos = beacon_pos
        self.beacon_dist = []
        for i in range(self.NUM_BEACONS - 1):
            row = []
            for j in range(i + 1, self.NUM_BEACONS):
                row.append(math.dist(beacon_pos[i], beacon_pos[j]))
            self.beacon_dist.append(row)
    
    def func(self, params):
        total = 0
        for i in range(self.NUM_BEACONS - 1):
            for j in range(i + 1, self.NUM_BEACONS):
                d = self.beacon_dist[i][j - i - 1]
                a = self.angles[i][j - i - 1]
                xi, yi = self.beacon_pos[i]
                xj, yj = self.beacon_pos[j]
                x, y = params
                val = (x-xi)**2 + (x-xj)**2 + (y-yi)**2 + (y-yj)**2 - 2*math.sqrt(((x-xi)**2 + (y-yi)**2)*((x-xj)**2 + (y-yj)**2))*math.cos(math.radians(a)) - d**2
                total += val**2
        return total
    
    # Triangules position for any number of beacons.
    def find_pos_general(self, angles):
        self.angles = angles
        res = minimize(self.func, [self.x_lim/2, self.y_lim/2], bounds=[(0, self.x_lim), (0, self.y_lim)]) # First guess is the centre of the arena.
        best_fit = res.x
        return (best_fit[0], best_fit[1])
    
    # Triangules position using three beacons.
    # alpha is the angle between beacons 1 and 2.
    # beta is the angle between beacons 1 and 3.
    # gamma is the angle between beacons 2 and 3.
    def find_pos(self, alpha, beta, gamma):
        return self.find_pos_general([[alpha, beta], [gamma]])