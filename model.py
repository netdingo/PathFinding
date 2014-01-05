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
from node import Node, NodeSet, NodeList 

class SearchModel(object):
    def __init__(self, nodeSet, **kargs):
         self.nodes = nodeSet
         node_cls = Node
         if 'node_cls' in kargs: node_cls = kargs['node_cls']
         self.nodes.node_cls = node_cls
         self.open_list = NodeList() 
         self.close_list = NodeList() 
         pass

    def init(self):
        assert(0)
        pass

    def find_path(self):
        assert(0)
        pass

    def get_path(self, end_node):
        node = end_node
        path = []
        if not end_node : return path
        path.append(node)
        while node.parent:
                node = node.parent
                path.insert(0, node)
        return path

def check_param(kargs, name, def_value, del_key= True):
    v = def_value
    if name in kargs : 
        v = kargs[name]
        if del_key: del kargs[name]
    return v
