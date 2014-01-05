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
from node import Node, NodeSet
import model 

class AStarNode(Node):
    f = g = h = 0
    def __init__(self, pos):
        Node.__init__(self, pos)

    def update_fgh(self, g, h):
        self.g, self.h = g, h
        self.f = g + h

    def steps(self):
        return self.g

    def __lt__(self, node):
        if self.f < node.f: return True
        else: return False

    def __str__(self):
        parent_node = "None" if not self.parent else str(self.parent.pos)
        s = [ "\n" + "=" * 60, 
              "node.pos: %s " % (str(self.pos)), 
              "node.fgh: %d, %d, %d" % (self.f, self.g, self.h),
              "node.parent: -> [ %s ]" % parent_node,
              "\n"
            ]
        return "\n".join(s)

    def __repr__(self):
        return self.__str__()

class AStar(model.SearchModel):
    """
       1，把起始格添加到开启列表。
       2，重复如下的工作：
          a) 寻找开启列表中F值最低的格子。我们称它为当前格。
          b) 把它切换到关闭列表。
          c) 对相邻的8格中的每一个？
              * 如果它不可通过或者已经在关闭列表中，略过它。反之如下。
              * 如果它不在开启列表中，把它添加进去。把当前格作为这一格的父节点,
                    并记录这一格的F,G,和H值。
              * 如果它已经在开启列表中，用G值为参考检查新的路径是否更好。更低的G值意味着更好的路径。
                    如果是这样，就把这一格的父节点改成当前格，并且重新计算这一格的G和F值。 
                    如果你保持你的开启列表按F值排序，改变之后你可能需要重新对开启列表排序。
          d) 停止，当你
              * 把目标格添加进了关闭列表(注解)，这时候路径被找到，或者
              * 没有找到目标格，开启列表已经空了。这时候，路径不存在
       3.保存路径。从目标格开始，沿着每一格的父节点移动直到回到起始格。这就是你的路径。
    """
    def __init__(self, nodeSet, **kargs):
        kargs['node_cls'] = AStarNode
        self.dist_measure = model.check_param(kargs, 'dist_measure', "euclidean", False)
        if self.dist_measure.strip() == "": 
            self.dist_measure = "euclidean"
        nodeSet.real_distance = self.distance 
        model.SearchModel.__init__(self, nodeSet, **kargs)

    def distance(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        if self.dist_measure == 'euclidean':
            d = math.sqrt(dx ** 2 + dy ** 2)
        elif self.dist_measure == 'manhatton':
            d = float(dx + dy)
        elif self.dist_measure == 'chebyshev':
            d = float(max(dx, dy))
        else:
            print "wrong distance measure approach!"
            assert(0)
        return d

    def init(self):
        start_node = self.nodes.get_start_node()
        g = 0
        h = self.nodes.distance(start_node, self.nodes.get_end_node())
        start_node.update_fgh(g, h)
        self.open_list.add_node(start_node)
        
    def find_path(self): 
        ret = False
        self.init()
        end_node = None
        while True:
            node = self.open_list.remove_head_node()
            if not node : break
            self.close_list.add_node(node)
            if self.nodes.is_end_node(node):
                ret = True
                end_node = node
                break
            node_list = self.nodes.enum_children(node)
            for child in node_list:
                if self.close_list.contains(child): continue ## ignore if node in close list
                g = self.nodes.step(node, child) 
                h = self.nodes.distance(child, self.nodes.get_end_node())
                if not self.open_list.contains(child):       ## node not in open_list, add it open_list
                    child.parent = node
                    child.update_fgh(node.steps() + g, h)
                    self.open_list.add_node(child)           ## meantime, update the F, G, H of this child
                    self.open_list.sort()                    ## resort
                    #print child
                else: ## child is already in open list yet
                    if node.steps() + g < child.steps():     ## find a shorter path
                        child.parent = node
                        g = nodes.steps() + g
                        child.update_fgh(g, h)
                        self.open_list.sort()   ## resort
                        #print child
        path = self.get_path(end_node)
        return path 
