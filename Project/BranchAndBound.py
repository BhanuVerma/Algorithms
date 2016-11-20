import networkx as nx
# import sys,operator,itertools
# import numpy as np
import time
import BranchState


class BranchAndBound:

	def __init__(self, graph):
		self.graph = graph
		self.winner = None
		self.results = []


	def run_DFS(self, graph):
		stack = []
		currentCity = 1
		a = graph.copy()
		startState = BranchState.BranchState(graph.copy(), [], 0)
		startState.addToPath(currentCity)
		stack.append(startState)

		while len(stack):
			if time.time() - self.begin_time > 300:
				break
				
			currentState = stack.pop()
			if not self.winner or currentState.boundValue < self.winner.boundValue:
				if len(currentState.path) == len(graph.node.keys()): #if we have a candidate solution
					if currentState.path[0] in graph[currentState.path[-1]].keys(): #if the last city is connected to the first one to create a cycle
						currentState.addToPath(currentState.path[0])
						if not self.winner or self.winner.boundValue > currentState.boundValue:#updating upper bound
							self.results.append((time.time() - self.begin_time, currentState.path_cost, currentState.path))
							print("Candidate- ",(time.time() - self.begin_time, currentState.path_cost, currentState.path))
							self.winner = currentState
				else:
					sorted_list = self.sort_edges(graph[currentState.path[-1]])
					for new_city,dist in sorted_list:
						if new_city not in currentState.path:
							newState = BranchState.BranchState(graph, currentState.path[:], currentState.path_cost)
							newState.addToPath(new_city) #discovering new paths
							if not self.winner or self.winner.boundValue > newState.boundValue: #only visiting a path if its lowerbound is lesser than upperbound
								stack.append(newState)


	def sort_edges(self,edge_dict):
		tup = []
		for key in edge_dict:
			tup.append((key,edge_dict[key]['weight']))

		sorted(tup, key=lambda edge:edge[1], reverse=True)

		return tup


	def generate_tour(self, limit=1):
		graph = self.graph
		# mat = [[0 for i in range(len(graph.node.keys()))] for j in range(len(graph.node.keys()))]
		# for i in range(len(graph.node.keys())):
		# 	for j in range(len(graph.node.keys())):
		# 		if i != j:
		# 			mat[i][j] = graph[i+1][j+1]
		# 		else:
		# 			mat[i][j] = sys.maxint
		# self.mat = np.array(mat)
		self.begin_time = time.time()
		self.run_DFS(graph)

		return self.results

