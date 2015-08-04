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
import hashlib

from numpy import *
from copy import deepcopy

tspglobal = None

testlist = [[3, 0],
    [3, 3],
    [4, 4],
    [1, 2],
    [1, 4],
    [4, 3],
    [2, 1],
    [0, 4],
    [1, 3]]

#testlist = [[0,0], [1,1], [2,2], [3,3], [4,4]]

class Neighbour:
    location = None
    edgecost = inf
    mstcost = None
    fvalue = None
    parent = None
    
class Node:
    identifier = None
    location = None
    visited = False
    neighbours = []  #(location, edgecost, mstcost)
    mstcost = None
    parent = None
    #connectedNodes = [] assuming that the every node is connected to each other

def MakeNode(location, parent):
    node = Node()
    node.location = location
    node.parent = parent
    return node

def InitTSPTree(numnodes, maxconnections=3):
    """
    maxconnections : future
    current : all nodes are connected to every other node
    """
    locations = []
    if 0:
        for i in range(1, numnodes+1):
            node = Node()
            node.location = [random.randint(1, nodes), random.randint(1, nodes)]
            locations.append(node)
    else:
        for i in testlist:
            node = Node()
            node.location = i
            locations.append(node)

    for node in locations:
        neighbours = GetNeigbours(node.location, locations)
        node.neighbours = []
        for neighbour in neighbours:
            n = Neighbour()
            n.location = neighbour.location
            n.edgecost = linalg.norm(array(n.location) - array(node.location))
            node.neighbours.append(n)
    return locations


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
    
    
def CheckLocationPresent(tree, location):
    for node in tree:
        if node.location == location:
            return True
    return False


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
    #print "Cost", cost
    return cost

def ComputeMST2(location, treelist):
    values = location[location.keys()[0]][0]
    newtreelist = deepcopy(treelist)

    print len(newtreelist)
    if len(newtreelist) < 2:
        return 0
    if len(newtreelist) < 3:
        return linalg.norm(array(newtreelist[1]) - array(newtreelist[0]))
    subtree = []
    for value in newtreelist:
        subtree.append(MakeNode(value, None))
    for node in subtree:
        neighbours = GetNeigbours(node.location, locations)
        node.neighbours = []
        for neighbour in neighbours:
            n = Neighbour()
            n.location = neighbour.location
            n.edgecost = linalg.norm(array(n.location) - array(node.location))
            node.neighbours.append(n)

    
    return ComputeMST(subtree, subtree[0])
        
        
def FindNodeFromNeighbour(neighbour, locations):
    for ilocation, location in enumerate(locations):
        if neighbour.location == location.location:
            return ilocation

def RemoveNeighbourFromNode(neighbour, node):
    neighbours  = node.neighbours
    for n in neighbours:
        if n.location == neighbour.location:
            neighbours.remove(n)
            break
    return node

def RemoveNodeFromTree(node, tree):
    tree2 = deepcopy(tree)
    for n in tree2:
        if n.location == node.location:
            tree2.remove(n)
            break
    return tree2
    
def CheckNode(nodelist, node):
    for n in nodelist:
        if node.location == n.location:
            return True
    return False

def CheckGoalTest(tree):
    for node in tree:
        if node.visited == False:
            return False
    return True

def popmin(dictionary):
    bestdistance = inf
    savekey = None
    for d in dictionary:
        if dictionary[d][1] < bestdistance:
            savekey = d
            save = {d:dictionary[d]}
            bestdistance = deepcopy(dictionary[d][1])
    if savekey is not None:
        dictionary.pop(savekey)
        return save, savekey
    else:
        return None, savekey
        

def SolveTSP2(tree):
    """
    used with Astar
    """
    solvertree = deepcopy(tree)
    def AddChildren(location, locationlist):
        value = location[location.keys()[0]]
        gcost = value[3]
        poses = value[0]
        childtestlist = deepcopy(testlist)
        for pose in poses:
            childtestlist.remove(pose)
        children = []
        for l in locationlist:
            add = True
            for pose in poses:
                if l == pose:
                    add = False
            if add:
                children.append(l)
        #prepare node
        childrendictionary = {}
        for child in children:
            newchildtestlist = deepcopy(childtestlist)
            finaldict = deepcopy(poses)
            finaldict.insert(0, child)
            pathcost = 0.0
            for ipose, individualposes in enumerate(finaldict[1:]):
                pathcost += linalg.norm(array(individualposes) - array(finaldict[ipose]))
            gcost = pathcost
            newchildtestlist.remove(child)
            mstcost = ComputeMST2({'1':[[child]]}, newchildtestlist) + linalg.norm(array(child) - array(testlist[0]))# the second heuristic allows to make a round trip 
            fcost = gcost + mstcost 
            childrendictionary[hashlib.md5(array(finaldict)).hexdigest()] = [finaldict, fcost, mstcost, gcost]

        return childrendictionary

    
    listofnodes = {}
    listofnodes[hashlib.md5(array(testlist[0])).hexdigest()] = [[testlist[0]], 10, 0, 0]
    listofnodes[hashlib.md5(array(testlist[0])).hexdigest()][2] = ComputeMST2(listofnodes, testlist)
    listofnodes[hashlib.md5(array(testlist[0])).hexdigest()][1] = listofnodes[hashlib.md5(array(testlist[0])).hexdigest()][2] + listofnodes[hashlib.md5(array(testlist[0])).hexdigest()][3]
    while len(listofnodes) > 0:
        minvalue = popmin(listofnodes)
        pair = minvalue[0]
        key = minvalue[1]
        if len(pair[key][0]) >= len(testlist):
            return pair
        children = AddChildren(pair, testlist)
        listofnodes.update(children)

    
if __name__=="__main__":
    global tspglobal
    nodes = 5
    locations = InitTSPTree(nodes)
    print "Given"
    for n in locations:
        print n.location
    pair = SolveTSP2(locations)
    print pair
    
