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

class XFSNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos)
    def __str__(self):
        parent_node = "None" if not self.parent else str(self.parent.pos)
        s = [ "\n" + "=" * 60, 
              "node.pos: %s " % (str(self.pos)), 
              "node.parent: -> [ %s ]" % parent_node,
              "\n"
            ]
        return "\n".join(s)
    def __repr__(self):
        return self.__str__()

class XFS(model.SearchModel):
    def __init__(self, nodeSet, **kargs):
        kargs['node_cls'] = XFSNode
        model.SearchModel.__init__(self, nodeSet, **kargs)
        self.xfs = 0 if kargs['xfs'] == 'bfs' else 1

    def init(self):
        start_node = self.nodes.get_start_node()
        self.open_list.add_node(start_node)

    def find_path(self):
        ret = False
        self.init()
        end_node = None
        while True:
            node = self.open_list.remove_head_node()
            if not node: break
            if self.nodes.is_end_node(node): ## 目前只找一个解
                ret = True
                end_node = node
                break
            self.close_list.add_node(node)
            node_list = self.nodes.enum_children(node)
            for child in node_list:
                if self.close_list.contains(child): continue ## ignore if node in close list
                if not self.open_list.contains(child):       ## node not in open_list, add it open_list
                    child.parent = node
                    if self.xfs == 0:
                        self.open_list.append_node(child)
                    else:
                        self.open_list.add_node_to_head(child)
        path = self.get_path(end_node)
        return path                    

class BFS(XFS):
    """
    BFS（Breadth-First-Search 宽度优先搜索）
    首先将起始结点放入OPEN表，CLOSE表置空，算法开始时：
        1、如果OPEN表不为空，从表中开始取一个结点S，如果为空算法失败
        2、S是目标解吗？是，找到一个解（继续寻找，或终止算法）；不是到3
        3、将S的所有后继结点展开，就是从S可以直接关联的结点（子结点），如果不在CLOSE表中，
           就将它们放入OPEN表末尾，而把S放入CLOSE表，重复算法到1。
    BFS是从表头取结点，从表尾添加结点，OPEN表是一个队列。
    """
    def __init__(self, nodeSet, **kargs):
        kargs['xfs'] = 'bfs'
        XFS.__init__(self, nodeSet, **kargs)

class DFS(XFS):
    """
    DFS（Depth-First-Search 深度优先搜索）
    首先将起始结点放入OPEN表，CLOSE表置空，算法开始时：
        1、如果OPEN表不为空，从表中开始取一个结点S，如果为空算法失败
        2、S是目标解吗？是，找到一个解（继续寻找，或终止算法）；不是到3
        3、将S的所有后继结点展开，就是从S可以直接关联的结点（子结点），如果不在CLOSE表中，
           就将它们放入OPEN表开始，而把S放入CLOSE表，重复算法到1。
    DFS从OPEN表头取结点，也从表头添加结点，OPEN表是一个栈
    """
    def __init__(self, nodeSet, **kargs):
        kargs['xfs'] = 'dfs'
        XFS.__init__(self, nodeSet, **kargs)
