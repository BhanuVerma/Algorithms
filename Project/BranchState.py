# Class for storing the state of path covered till now

import networkx as nx
import numpy as np
import sys

class BranchState:

	def __init__(self,graph, path, path_cost, matrix):
		self.graph = graph
		self.path = path
		self.path_cost = path_cost
		self.matrix = matrix


	def add_stop(self, stop):
		if len(self.path):
			self.path_cost = self.path_cost + self.graph[self.path[-1]][stop]['weight']
		self.path.append(stop)
		# self.bound_val = self.get_1tree_lower_bound(self.graph, self.path, self.path_cost)
		self.bound_val = self.get_min_dist_lower_bound(self.matrix, self.path, self.path_cost)


	def get_1tree_lower_bound(self, graph, path, path_cost):
		sub_graph = graph.copy()
		if len(path) > 1 and path[0] == path[-1]:
			path = path[:-1]

		for n in path:
			sub_graph.remove_node(n)

		mst = nx.minimum_spanning_tree(sub_graph)
		start_u = path[0]
		start_v = self.get_cheapest_neighbour(start_u,graph)
		end_u = path[-1]
		end_v = self.get_cheapest_neighbour(end_u,graph)

		mst.add_edge(start_u, start_v, weight=graph[start_u][start_v]['weight'])
		mst.add_edge(end_u, end_v, weight= graph[end_u][end_v]['weight'])

		return path_cost + mst.size(weight='weight')


	def get_min_dist_lower_bound(self, matrix, path, path_cost):
		mat = matrix.copy()
		if len(path) > 1:
			i=0
			while i < len(path)-2:
				mat[path[i]-1] = sys.maxsize
				mat[path[i+1]-1] = sys.maxsize
				i += 2
		row_min = np.amin(mat, axis=1)
		mat = mat - np.reshape(row_min,(len(matrix),1))
		col_min = np.amin(mat, axis=0)

		return np.sum(row_min) + np.sum(col_min) + path_cost


	def get_cheapest_neighbour(self, node, graph):
		temp_dict = graph[node]
		tup = []
		for key in temp_dict:
			tup.append((key,temp_dict[key]['weight']))

		return min(tup,key =lambda edge:edge[1])[0]
