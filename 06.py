# --- Day 6: Universal Orbit Map ---
# You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

# Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:

#                   \
#                    \
#                     |
#                     |
# AAA--> o            o <--BBB
#                     |
#                     |
#                    /
#                   /
# In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.

# Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

# For example, suppose you have the following map:

# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# Visually, the above map of orbits looks like this:

#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I
# In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.

# Here, we can count the total number of orbits as follows:

# D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
# L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
# COM orbits nothing.
# The total number of direct and indirect orbits in this example is 42.

# What is the total number of direct and indirect orbits in your map data?
import copy


def read_file(filename):
    orbits = []
    with open(filename) as fp:
        for line in fp:
            line = line.replace("\n", "")
            orbit = line.split(")")
            orbits.append(orbit)

    return orbits


def get_nodes(orbits):
    nodes = set()
    for orbit in orbits:
        for o in orbit:
            nodes.add(o)

    return list(nodes)


def build_graph(nodes, orbits):
    direct_graph = {node: [] for node in nodes}
    # Add direct nodes to the direct_graph
    for orbited, orbiter in orbits:
        direct_graph[orbiter].append(orbited)

    graph = copy.deepcopy(direct_graph)

    # Add indirect nodes
    for key in graph.keys():
        if key == 'COM':
            continue
        [direct_node] = direct_graph[key]
        while direct_node != "COM":
            [indirect_node] = direct_graph[direct_node]
            graph[key].append(indirect_node)
            direct_node = indirect_node

    return graph


def count_orbits(graph):
    num_orbits = 0
    for key, val in graph.items():
        num_orbits += len(val)
    return num_orbits


orbits = read_file("06_orbit_data.txt")
# orbits = read_file("06_test.txt")

nodes = get_nodes(orbits)

graph = build_graph(nodes, orbits)

# print("Number of direct and indirect orbits: ", count_orbits(graph))

# =========================================================================================================================
# --- Part Two ---
# Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

# You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.

# For example, suppose you have the following map:

# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN
# Visually, the above map of orbits looks like this:

#                           YOU
#                          /
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
# In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:

# K to J
# J to E
# E to D
# D to I
# Afterward, the map of orbits looks like this:

#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#                  \
#                   YOU
# What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

# Obtain trajectories to COM for YOU and SAN

YOU = graph["YOU"]
SAN = graph["SAN"]

# Find the intersection node/object to merge both trajectories with
intersection_node = None
for y in YOU:
    for s in SAN:
        if y == s:
            intersection_node = y
            break
    if intersection_node is not None:
        break

idx_y = YOU.index(intersection_node)
idx_s = SAN.index(intersection_node)
buffer = SAN[0:idx_s]
buffer.reverse()
full_trajectory = YOU[:idx_y+1] + buffer

num_transfers = len(full_trajectory)-1

print(full_trajectory[197:201])
print(YOU[idx_y-1:idx_y+2])
print(SAN[idx_s-1:idx_s+2])
print("Length of the shortest path is: ", num_transfers)

# 467 too high
