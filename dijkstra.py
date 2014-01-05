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

import os, sys
import model
from node import Node

class DijkstraNode(Node):
    d = 0
    def __init__(self, pos):
        Node.__init__(self, pos)

    def update_step(self, d):
        self.d = d

    def steps(self):
        return self.d

    def __lt__(self, node):
        if self.d < node.d: return True
        else: return False

    def __str__(self):
        parent_node = "None" if not self.parent else str(self.parent.pos)
        s = [ "\n" + "=" * 60, 
              "node.pos: %s " % (str(self.pos)), 
              "node.fgh: %d" % (self.d),
              "node.parent: -> [ %s ]" % parent_node,
              "\n"
            ]
        return "\n".join(s)

    def __repr__(self):
        return self.__str__()

class Dijkstra(model.SearchModel):
    """
    wikipedia 上的算法描述：
    function Dijkstra(G, w, s)
        for each vertex v in V[G]                        // 初始化
              d[v] := infinity                           // 將各點的已知最短距離先設成無窮大
              previous[v] := undefined                   // 各点的已知最短路径上的前趋都未知
        d[s] := 0                                        // 因为出发点到出发点间不需移动任何距离，所以可以直接将s到s的最小距离设为0
        S := empty set                                   // close list
        Q := set of all vertices
        while Q is not an empty set                      // Dijkstra演算法主體
              u := Extract_Min(Q)
              S.append(u)                                // add u to close list
              for each edge outgoing from u as (u,v)
                     if d[v] > d[u] + w(u,v)             // 拓展边（u,v）。w(u,v)为从u到v的路径长度。
                           d[v] := d[u] + w(u,v)         // 更新路径长度到更小的那个和值。
                           previous[v] := u              // 紀錄前趨頂點
    Dijkstra 算法实际是A*的简化版，即当A*的h估计值为0时的特例。
    """
    def __init__(self, nodeSet, **kargs):
        kargs['node_cls'] = DijkstraNode
        model.SearchModel.__init__(self, nodeSet, **kargs)
    def init(self):
        start_node = self.nodes.get_start_node()
        start_node.update_step(0)
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
                d = self.nodes.step(node, child) 
                if not self.open_list.contains(child):       ## node not in open_list, add it open_list
                    child.parent = node
                    child.update_step(node.steps() + d)
                    self.open_list.add_node(child)           ## meantime, update the F, G, H of this child
                    self.open_list.sort()                    ## resort
                else: ## child is already in open list yet
                    if node.steps() + d < child.steps():     ## find a shorter path
                        child.parent = node
                        d = nodes.steps() + d
                        child.update_step(d)
                        self.open_list.sort()   ## resort
        return self.get_path(end_node)
