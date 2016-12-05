import networkx as nx
import sys,operator,itertools
import numpy as np
import time
import BranchState


class BranchAndBound:

	def __init__(self, graph, limit=600):
		self.graph = graph
		self.winner = None
		self.results = []
		self.limit = limit


	def run_DFS(self, graph, matrix):
		stack = []
		initial_city = 1
		a = graph.copy()
		initial_state = BranchState.BranchState(graph.copy(), [], 0, matrix)
		initial_state.add_stop(initial_city)
		stack.append(initial_state)
		i = 0

		while len(stack):
			if time.time() - self.begin_time > self.limit:
				break

			last_state = stack.pop()
			if not self.winner or last_state.bound_val < self.winner.bound_val:

				# checking for a candidate solution
				if len(graph.node.keys()) == len(last_state.path):

					# checking if we have a cycle
					if last_state.path[0] in graph[last_state.path[-1]].keys(): 
						last_state.add_stop(last_state.path[0])

						# checking if upper bound needs to be updated
						if not self.winner or self.winner.bound_val > last_state.bound_val:
							i += 1
							self.results.append((last_state.path, last_state.path_cost, time.time() - self.begin_time))
							print("Solution" + str(i) + ": ",(last_state.path, last_state.path_cost, time.time() - self.begin_time))
							self.winner = last_state
				else:
					sorted_list = self.sort_edges(graph[last_state.path[-1]])
					for node,cost in sorted_list:
						if node not in last_state.path:
							new_state = BranchState.BranchState(graph, last_state.path[:], last_state.path_cost, matrix)
							new_state.add_stop(node)

							# checking if a branch can be pruned
							if not self.winner or self.winner.bound_val > new_state.bound_val: 
								stack.append(new_state)


	def sort_edges(self,edge_dict):
		tup = []
		for key in edge_dict:
			tup.append((key,edge_dict[key]['weight']))

		sorted(tup, key=lambda edge:edge[1], reverse=True)

		return tup


	def generate_tour(self):
		graph = self.graph
		mat = [[0 for i in range(len(graph.node.keys()))] for j in range(len(graph.node.keys()))]
		for i in range(len(graph.node.keys())):
			for j in range(len(graph.node.keys())):
				if i != j:
					mat[i][j] = graph[i+1][j+1]['weight']
				else:
					mat[i][j] = sys.maxsize
		self.mat = np.array(mat)
		self.begin_time = time.time()
		self.run_DFS(graph, self.mat)

		return self.results

