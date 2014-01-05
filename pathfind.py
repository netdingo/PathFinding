#!/usr/bin/env python
#encoding=utf-8 

# Copyright (C) 2012 by guohong.xie <guohong.xie@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, sys, types, math
from node import  MatrixNodeSet
import astar, bfs_dfs, dijkstra 
from   model import check_param
import pdb

def find_path(**kargs):
    """
       find path from begin point to end one in data map.
       searching_method: "bfs, dfs, dijkstra, astar" 
       nodeset: node map
       dist_measure: euclidean, chebyshev, manhatton
    """
    searching_method = check_param(kargs, 'searching_method', "astar")
    nodeset = check_param(kargs, 'nodeset', "astar")
    dist_measure = check_param(kargs, 'dist_measure', "", False)
    cls_tbl = {'astar': astar.AStar, 'bfs': bfs_dfs.BFS, 'dfs': bfs_dfs.DFS, 'dijkstra': dijkstra.Dijkstra }
    if searching_method not in cls_tbl:
        print "Fail to find specified searching approach!"
        return False
    cls = cls_tbl[searching_method]
    pfo = cls(nodeset, **kargs) 
    path = pfo.find_path()
    print path
    return path

def test_astar():
    map1="""\
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000010000000000000
00000000000010000000003000
00000000000010000000000000
00000000000010000000000000
00000000000010000000000000
00000000000010000000000000
00000000000010000000000000
00000000000010000000000000
00020000000010000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000"""

    map2="""\
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000010000000000000
00000000000010000011111110
00000000000010000010000010
00111100000010000010111010
00000100000010000010100010
01020100000010000010103010
01000100000010000010111110
01111100000010000010000000
00000000000010000011111110
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000
00000000000000000000000000"""

    matrix = [ list(s) for s in map1.split() ] 
    data = map(lambda l: map(lambda x: int(x), l), matrix)
    start = None
    end = None
    x = y = 0
    while y < len(data):
        x = 0
        while x < len(data[0]):
            if data[y][x] == 2:  ## find start node
                start = (x, y)
                data[y][x] = 0
            elif data[y][x] == 3:## find end node
                end = (x, y)
                data[y][x] = 0
            x += 1
        y += 1
    mns = MatrixNodeSet(data, start, end)
    searching_method = "astar" ## "bfs", "dfs", "dijkstra", "astar" 
    dist_measure = 'euclidean'
    path = find_path(nodeset = mns, searching_method = searching_method , dist_measure = dist_measure )
    print path
    if path: 
        mns.mark_path(path)
        print mns.dump()

if __name__ == '__main__':
    test_astar()
