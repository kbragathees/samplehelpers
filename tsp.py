# -*- coding: utf-8 -*-
# Copyright (C) 2015 Praveen Ramanujam <pramanujam86@gmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 

"""
Travelling Salesman Problem, finds the minimal path given a set of nodes.
Algorithm as suggested in Peter Norvig's book.
Solves TSP as a A-star problem with MST as a heuristic function.
NP-Complete or NP-Hard ?
"""
import random
from numpy import *
from copy import deepcopy

tspglobal = None

testlist = {0:[3, 0],
    1:[3, 3],
    2:[4, 4],
    3:[1, 2],
    4:[1, 4],
    5:[4, 3],
    6:[2, 1],
    7:[0, 4],
    8:[1, 3]}

class Neighbour:
    location = None
    edgecost = inf
    mstcost = None
    fvalue = None
    parent = None
    
class Node:
    location = None
    visited = False
    neighbours = []  
    mstcost = None
    parent = None

def MakeNode(location, parent):
    node = Node()
    node.location = location
    node.parent = parent
    return node

def GetNeigbours(value, locations):
    """
    trivial
    """
    graph = deepcopy(locations)
    for node in graph:
        if node.location== value:
            graph.remove(node)
            break
    return graph
    
    
def CheckAllVisited(tree):
    for node in tree:
        if node.visited == False:
            return False
    return True

def SortNeighbours(neighbours):
    prepare = [(neighbour.fvalue, i, neighbour) for i, neighbour in enumerate(neighbours)]
    prepare.sort()
    return [neighbour for fvalue, i , neighbour in prepare]


def ComputeMST(subtree, rootnode):
    """
    Computes MST with Prim's algorithm
    """
    tree = deepcopy(subtree)
    root = deepcopy(rootnode)
    spannedtree = []
    for n in tree:
        if n.location == root.location:
            n.visited = True
            break
    while True:
        spannedtree.append(root)
        if CheckAllVisited(tree):
            break
        neighbours = []
        for node in spannedtree:
            for n in node.neighbours:
                n.parent = node
                neighbours.append(n)
                n.fvalue = linalg.norm(array(n.location) - array(node.location))
        # sort the neighbours
        sortedneighbours = SortNeighbours(neighbours)
        # find the neighbour in the parent tree
        i = 0
        for neighbour in sortedneighbours:
            found = False
            for node in tree:
                if neighbour.location == node.location and node.visited == False:
                    node.visited = True
                    found = True
                    break
            if found:
                break
        node.parent = neighbour.parent
        root = node

    #compute MST cost
    cost = 0.0
    for node in spannedtree[1:]:
        cost += linalg.norm(array(node.location) - array(node.parent.location))
    return cost

def ComputeMST2(node):

    indices = where(node.visitedNodes == 0)[0]
    if len(indices) < 2:
        return 0
    if len(indices) < 3:
        return linalg.norm(array(testlist[indices[0]]) - array(testlist[indices[1]]))

    subtree = []
    for i in indices:
        subtree.append(MakeNode(testlist[i], None))

    for node in subtree:
        neighbours = GetNeigbours(node.location, subtree)
        node.neighbours = []
        for neighbour in neighbours:
            n = Neighbour()
            n.location = neighbour.location
            n.edgecost = linalg.norm(array(n.location) - array(node.location))
            node.neighbours.append(n)

    return ComputeMST(subtree, subtree[0])

class TSPNode:
    visitedNodes = zeros(len(testlist))
    currentNode = None
    parent = None
    startNode = None
    gcost = 0.
    fcost = 0.
    hcost = 0.


def UpdateState(states):
    """
    equivalent of AddChildren
    states structure :  [VistedNodes, currentnode, parent, startnode, g, f, h]
    """
    currentstate = states.visitedNodes
    indices = where(currentstate == 0)[0]
    neighbours = []
    
    for index in indices:
        node = TSPNode()
        node = deepcopy(states)
        node.visitedNodes[index] = max(node.visitedNodes) + 1
        node.currentNode = index
        node.parent = states.currentNode
        stepcost = linalg.norm(array(testlist[index]) - array(testlist[node.parent]))
        node.gcost += stepcost
        node.hcost = ComputeMST2(node)
        node.fcost = node.gcost + node.hcost + linalg.norm(array(testlist[index]) - array(testlist[0]))
        neighbours.append(node)

    return neighbours
    
def popmin2(listofnodes):
    bestdist = inf
    minnode = None
    for node in listofnodes:
        if node.fcost < bestdist:
            bestdist = node.fcost
            minnode = node
    return minnode


def SolveTSP2():
    """
    used with Astar
    """
    listofnodes = []
    staterep = zeros(len(testlist))
    staterep[0] = 1
    states = TSPNode()
    states.visitedNodes = staterep
    states.currentNode = 0
    states.parent = None
    states.startNode = 0
    states.gcost = 0
    states.hcost = ComputeMST2(states) 
    states.fcost = states.gcost + states.fcost
    listofnodes.append(states)
    while len(listofnodes) > 0:
        minnode = popmin2(listofnodes)
        listofnodes.remove(minnode)
        if len(where(minnode.visitedNodes == 0)[0]) == 0:
            return minnode
        listofnodes.extend(UpdateState(minnode))
    
if __name__=="__main__":
    pair = SolveTSP2()
    print "Sequence of visits"
    print pair.visitedNodes.tolist()

