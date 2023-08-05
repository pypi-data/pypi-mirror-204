# Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import uuid
from collections import OrderedDict

from graphlearn import pywrap_graphlearn as pywrap


class Dag(object):
  def __init__(self, graph):
    self._dag_def = None
    self._name = None
    self._nodes = OrderedDict()

    # User defined alias, excludes the LookupDagNodes alias generated by system.
    self._ud_alias = []

    self.sink_node = None
    self.graph = graph
    self.topo = self.graph.get_topology()
    self.value_func = None
    self._alias_to_index = OrderedDict()
    self._edge_types, self._node_types = [], []

    self._ready = False

  def __str__(self):
    return pywrap.debug_string(self._dag_def)

  def get_node(self, alias):
    node = self._nodes.get(alias)
    if node is None:
      raise ValueError("The Dag has no DagNode named {}.".format(alias))
    return node

  def add_node(self, alias, node, temp=False):
    def unique_append(item_list, item):
      if item not in item_list:
        item_list.append(item)

    if alias in self._alias_to_index.keys():
      raise ValueError("alias {} already existed.".format(alias))
    self._nodes[alias] = node
    if not temp:
      self._ud_alias.append(alias)
      dag_node_type = node.type
      if self.topo.is_exist(dag_node_type):
        unique_append(self._edge_types, 
          (self.topo.get_src_type(dag_node_type), 
           dag_node_type, 
           self.topo.get_dst_type(dag_node_type)))
      else:
        unique_append(self._node_types, dag_node_type)

  def list_alias(self):
    """ Return the list alias of user defined.
    """
    return self._ud_alias

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, name):
    self._name = name

  @property
  def dag_def(self):
    return self._dag_def

  @property
  def node_types(self):
    """ Return all node types in this Dag."""
    return self._node_types

  @property
  def edge_types(self):
    """ Return all edge types(a tuple of (src_type, edge_type, dst_type)) 
    in this Dag.
    """
    return self._edge_types

  def is_ready(self):
    return self._ready

  def set_ready(self, func):
    self.value_func = func

    # Set alias for sink node,
    # which will add in_edges for sink node.
    # And add the sink node to nodes.
    self.sink_node.alias(str(uuid.uuid1()))

    self._dag_def = pywrap.new_dag()
    self._name = get_dag_name()
    pywrap.set_dag_id(self._dag_def, self._name)

    # Link nodes with in_edges and out_edges.
    nid = 1
    for alias, node in self._nodes.items():
      if node.set_ready(nid):
        self._alias_to_index[alias] = nid
        nid += 1
        pywrap.add_dag_node(self._dag_def, node.node_def)
    
    self._ready = True

dag_name = 0

def get_dag_name():
  global dag_name
  dag_name += 1
  return dag_name
