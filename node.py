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

import os, sys, math
import pdb

class Node(object):
    parent=None
    pos = None
    def __init__(self, pos):
        self.pos = pos
    def __eq__(self, node):
        if node == None: return False
        return True if self.pos == node.pos else False
    def __lt__(self, node):
        assert(0)

class NodeSet(object):
    node_cls = Node
    def get_start_node(self):
        return self.get_node(self.start)

    def get_end_node(self):
        return self.get_node(self.end)

    def is_end_node(self, node):
        return True if self.get_end_node() == node else False

    def enum_children(self, node):
        assert(0)

    def step(self, node1, node2):
        """
           steps from node1 to node2
        """
        assert(0)
        pass
    def distance(self, node1, node2):
        """
           compute distance between node1 and node2
        """
        assert(0)

class NodeList(object):
    def __init__(self):
        self.node_list = []

    def sort(self):
        self.node_list.sort()

    def remove_head_node(self):
        if self.node_list: 
            return self.node_list.pop(0)
        else:
            return None
              
    def contains(self, node):         
        for tmp in self.node_list:
            if tmp == node:
                return True
        return False

    def add_node(self, node):         
        self.node_list.append(node)

    def add_node_to_head(self, node):         
        self.node_list.insert(0, node)

    def append_node(self, node):         
        self.node_list.append(node)

class MatrixNodeSet(NodeSet):
    BLOCKING   = 1
    NONBLOCKING= 0
    TARGET     = 0xFF
    STEP_UNIT  = 10
    directions = ( ( (-1, -1), (0, -1), (1, -1) ),
                   ( (-1, 0 ), (0,  0), (1, 0 ) ), 
                   ( (-1, 1 ), (0,  1), (1, 1 ) ) 
                 )
    def __init__(self, matrix, start, end):
        """
            matrix: two-dimension list array
            start:  point tuple
            end:    point tuple
        """
        NodeSet.__init__(self)
        self.matrix, self.start, self.end = matrix, start, end
        self.xmax = len(self.matrix[0]) 
        self.ymax = len(self.matrix) 

    def get_node(self, pos):
        return self.node_cls(pos)

    def get_value(self, pos):
        """
            must check whether pos is bigger than array dimension first!
        """
        x, y = pos
        return self.matrix[y][x]

    def set_value(self, pos, value):
        x, y = pos
        self.matrix[y][x] = value

    def isValid(self, pos):
        x, y = pos 
        if x >= self.xmax or x < 0: return False
        if y >= self.ymax or y < 0: return False
        try:
            v = self.get_value(pos)
        except Exception, e:
            print e
            pass
        if v == self.BLOCKING : return False 
        else: return True

    def enum_children(self, node):
        l = []
        x, y = node.pos
        for pts in self.directions:
            for pt in pts:
                if pt[0] == 0 and pt[1] == 0: continue
                pos = (x + pt[0], y + pt[1])
                if self.isValid(pos):
                    l.append(self.get_node(pos))
        return l

    def step(self, node1, node2):
        """
           steps from node1 to node2
           两个节点之间的G值
        """
        dx = node2.pos[0] - node1.pos[0]
        dy = node2.pos[1] - node1.pos[1]
        d  = int(math.sqrt(dx ** 2 + dy ** 2) * self.STEP_UNIT)
        return d

    def distance(self, node1, node2):
        """
           compute distance between node1 and node2
        """
        if hasattr(self, 'real_distance'):
            return int(self.STEP_UNIT * self.real_distance(node1.pos, node2.pos))
        else:
            assert(0)
            return 0 ## TODO

    def mark_path(self, path):
        if not path: return False
        for node in path:
            v = self.get_value(node.pos) 
            if v == self.BLOCKING :
                print "path error: position(%d, %d) is a blocking block!"
            self.set_value(node.pos, "#")
        node = self.get_start_node()
        self.set_value(node.pos, "S")
        node = self.get_end_node()
        self.set_value(node.pos, "E")

    def dump(self):
        return "\n".join( map(lambda l : "".join(map( lambda x: str(x), l)), self.matrix ) )

