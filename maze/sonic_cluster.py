import math

DIST_T = 50

# Finds the difference between two numbers in modular arithmetic.
def mod_diff(a, b, mod):
    diff = b - a
    if diff <= -mod/2:
        return diff + mod
    elif diff > mod/2:
        return diff - mod
    else:
        return diff

# Finds the average of two numbers in modular arithmetic.
def mod_avg(a, b, mod):
    diff = mod_diff(a, b, mod)
    if diff > 0:
        return (a + diff/2) % 360
    else:
        return (a - diff/2) % 360

# Convert ultrasonic sensor readings to link angles.
def get_link_angles(angles, left_dists, right_dists, robot_angle):
    dist_scan = []
    for reading in left_dists:
        if reading >= DIST_T:
            dist_scan.append(True)
        else:
            dist_scan.append(False)
    link_angles = []
    counting = False
    current_angle = robot_angle % 360 # Assume the scan starts and ends at the same angle.
    track_angle = current_angle
    scan_res = len(dist_scan)
    for i in range(scan_res):
        current_angle += 360 / scan_res
        current_angle %= 360
        if dist_scan[i] and not counting:
            counting = True
            track_angle = current_angle
            # current_angle = self.robot_angle + i/scan_res * 360
        elif dist_scan[i] and counting:
            track_angle += 0.5/scan_res * 360
            track_angle %= 360
        elif not dist_scan[i] and counting:
            counting = False
            track_angle += 0.5/scan_res * 360
            track_angle %= 360
            link_angles.append(track_angle)
    if counting and dist_scan[0]:
        # start = 2*current_angle - 360
        # end = 2*link_angles[0] + 360
        # link_angles.append(((start + end) / 2) % 360)
        right_dist = abs(mod_diff(robot_angle % 360, link_angles[0], 360))
        # left_dist = abs(self.tracker.mod_diff(self.robot_angle, current_angle) * 2)
        link_angles.append((track_angle + right_dist) % 360)
        link_angles.pop(0)
    elif counting and not dist_scan[0]:
        link_angles.append(track_angle)
    temp = []
    for angle in link_angles:
        temp.append((angle - 90) % 360)
    return temp

# def get_link_angles(pos, angle, last_vertex, left_dists):
#     diff = (pos[0] - last_vertex[0], last_vertex[1] - pos[1])
#     entry_angle = (90 - math.degrees(math.atan2(diff[1], diff[0]))) % 360
#     dist_scan = []
#     for reading in left_dists:
#         if reading >= DIST_T:
#             dist_scan.append(True)
#         else:
#             dist_scan.append(False)
#     temp = [180]
#     scan_res = len(dist_scan)
#     if dist_scan[0]:
#         temp.append(270)
#     if dist_scan[int(scan_res / 4)]:
#         temp.append(0)
#     if dist_scan[int(scan_res / 2)]:
#         temp.append(90)
#     link_angles = []
#     for angle in temp:
#         link_angles.append((angle + entry_angle) % 360)
#     return link_angles

# Rearrange link angles to have the first be closest to north.
def rearrange_link_angles(link_angles):
    closest_index = 0
    closest_dist = math.inf
    for i in range(len(link_angles)):
        if abs(mod_diff(link_angles[i], 0, 360)) < closest_dist:
            closest_index = i
            closest_dist = abs(mod_diff(link_angles[i], 0, 360))
    temp = []
    for i in range(len(link_angles)):
        temp.append(link_angles[(i + closest_index) % len(link_angles)])
    return temp

def find_link_angles(angles, left_dist, right_dist, robot_angle):
    return rearrange_link_angles(get_link_angles(angles, left_dist, right_dist, robot_angle))

# def find_link_angles(pos, last_vertex, left_dists):
#     return rearrange_link_angles(get_link_angles(pos, last_vertex, left_dists))

# def get_link_angles_cluster(robot_angle, angles, left, right=None):
#     assert len(angles) == len(left)
#     if right != None:
#         assert len(left) == len(right)
#     num_angles = len(angles)
#     dark_angles = []
#     for i in range(num_angles):
#         if left[i] <= SCAN_LIGHT_T:
#             angle = (angles[i] - 90) % 360
#             dark_angles.append(angle)
#     clusters = []
#     eps = 5
#     points_sorted = sorted(dark_angles)
#     curr_point = points_sorted[0]
#     curr_cluster = [curr_point]
#     for point in points_sorted[1:]:
#         if mod_diff(curr_point, point, 360) <= eps:
#         # if point <= curr_point + eps:
#             curr_cluster.append(point)
#         else:
#             clusters.append(curr_cluster)
#             curr_cluster = [point]
#         curr_point = point
#     clusters.append(curr_cluster)
#     if len(clusters) >= 2 and abs(mod_diff(points_sorted[0], points_sorted[-1], 360)) <= eps:
#         cluster = clusters[0] + clusters[-1]
#         clusters.pop(0)
#         clusters.pop()
#         clusters.append(cluster)
#     offset_link_angles = []
#     for cluster in clusters:
#         if len(cluster) == 0:
#             continue
#         start_angle = cluster[0]
#         avg = start_angle
#         for angle in cluster[1:]:
#             diff = mod_diff(start_angle, angle, 360)
#             avg += diff / len(cluster)
#         offset_link_angles.append(avg % 360)
#     temp = []
#     for angle in offset_link_angles:
#         temp.append((angle + robot_angle - angles[-1]) % 360)
#     print(temp)
#     return temp

# def get_link_angles_cluster(robot_angle, angles, left, right=None):
#     assert len(angles) == len(left)
#     if right != None:
#         assert len(left) == len(right)
#     num_angles = len(angles)
#     cluster = []
#     offset_link_angles = []
#     for i in range(num_angles):
#         if left[i] <= SCAN_LIGHT_T:
#             cluster.append((angles[i] - 90) % 360)
#         elif len(cluster) > 0:
#             offset_link_angles.append(mod_avg(cluster[0], cluster[-1], 360))
#             cluster.clear()
#     if len(cluster) > 0:
#         offset_link_angles.append(mod_avg(cluster[0], cluster[-1], 360))
#         cluster.clear()
#     if len(offset_link_angles) >= 2 and left[0] <= SCAN_LIGHT_T and left[-1] <= SCAN_LIGHT_T:
#         start_angle = offset_link_angles[0]
#         end_angle = offset_link_angles[-1]
#         offset_link_angles.pop(0)
#         offset_link_angles.pop()
#         offset_link_angles.append(mod_avg(start_angle, end_angle, 360))
#     temp = []
#     for angle in offset_link_angles:
#         temp.append((angle + robot_angle - angles[-1]) % 360)
#     print(angles)
#     print(left)
#     print(temp)
#     return temp

# def find_link_angles_cluster(robot_angle, angles, left, right=None):
#     return rearrange_link_angles(get_link_angles_cluster(robot_angle, angles, left, right))