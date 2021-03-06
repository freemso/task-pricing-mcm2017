# !/usr/bin/env python3

from math import acos, sin, cos
from random import shuffle


# a and b are two tuples (latitude, longitude)
def centralAngle(a, b):
    return acos(sin(a[0]) * sin(b[0]) + cos(a[0]) * cos(b[0]) * cos(a[1] - b[1]))


class QuadNode(object):
    def __init__(self, key):
        self.key = key
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None


def quadTreeInsert(tree, node):
    if not tree:
        return node
    if node.key[0] < tree.key[0]:
        if node.key[1] < tree.key[1]:
            tree.c1 = quadTreeInsert(tree.c1, node)
        else:
            tree.c2 = quadTreeInsert(tree.c2, node)
    elif node.key[1] < tree.key[1]:
        tree.c3 = quadTreeInsert(tree.c3, node)
    else:
        tree.c4 = quadTreeInsert(tree.c4, node)
    return tree


def buildQuadTree(data):
    tree = None
    shuffle(data)
    for task in data:
        tree = quadTreeInsert(tree, QuadNode((task.latitude, task.longitude)))
    return tree


def queryRange(tree, lower, upper):
    if tree:
        cond1 = cond2 = False
        if tree.key[0] < lower[0]:
            explore = set([tree.c3, tree.c4])
        elif tree.key[0] < upper[0]:
            cond1 = True
            explore = set([tree.c1, tree.c2, tree.c3, tree.c4])
        else:
            explore = set([tree.c1, tree.c2])

        (lo, hi) = (lower[1], upper[1])
        (lo, hi) = min((lo, hi), (hi, lo))

        if tree.key[1] < lo:
            explore = explore.intersection([tree.c2, tree.c4])
        elif tree.key[1] < hi:
            cond2 = True
            explore = explore.intersection([tree.c1, tree.c2, tree.c3, tree.c4])
        else:
            explore = explore.intersection([tree.c1, tree.c3])

        if cond1 and cond2:
            yield tree
        for subtree in explore:
            for el in queryRange(subtree, lower, upper):
                yield el

# returns the index of the nearest user
def nearestUser(task, users):
    taskcoord = (task.latitude, task.longitude)
    indices = [(centralAngle(taskcoord, (users[i].latitude, users[i].longitude)), i) for i in range(len(users))]
    return min(indices, key=lambda x: x[0])[1]
