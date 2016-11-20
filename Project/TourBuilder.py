import BranchAndBound
# import MstApprox
# import NNApprox
# import Opt2Search
import networkx as nx
from os.path import isfile
from math import sqrt
import argparse
import sys


class TourBuilder:
    def __init__(self, graph):
        self.graph = graph

    def build_tour(self, instance='Cincinnati', algorithm='bnb', seed=1, limit=1):

        if algorithm == 'bnb':
            bnb = BranchAndBound.BranchAndBound(self.graph)
            return bnb.generate_tour(limit=limit)
        # elif alg == 'mst_approx':
        # 	approx_1 = MstApprox(self.graph)
        #     return approx_1.generate_tour(seed=seed, time=time)
        # elif alg == 'nn_approx':
        # 	approx_1 = NNApprox(self.graph)
        #     return approx_1.generate_tour(seed=seed, time=time)
        # elif method == 'opt2_search':
        # 	ls_1 = Opt2Search(self.graph)
        #     return ls_1.generate_tour(seed=seed, time=time)
        else:
        	return None


def main():
    # building an argument parser for taking in values from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', type=str, dest="instance", default='Cincinnati', help='This argument takes in name of the cities')
    parser.add_argument('-alg', type=str, dest="algorithm", default='bnb', help='This argument takes in name of the algorithm')
    parser.add_argument('-time', type=int, dest="limit", default=1, help='This argument takes in cutoff time for the algorithm')
    parser.add_argument('-seed', type=int, dest="seed", default=1, help='This argument takes in randomized seed value for non deterministic algorithm')
    args = parser.parse_args()

    # Checking if file exists
    city_data = "./DATA/{}.tsp".format(args.instance)
    if not isfile(city_data):
        print("File not found in the Data folder. Please enter the correct file name.")
        sys.exit(1)

    # building city/graph data
    city_dict = {}
    with open(city_data) as f:
        while True:
            line = f.readline()
            if 'NODE_COORD_SECTION\n' in line:
                break
        for line in f:
            if 'EOF\n' in line:
                break
            v = line.split(' ')
            city_dict[int(v[0])] = {'x': float(v[1]), 'y': float(v[2])}

    # building cost matrix for each edge
    graph = nx.Graph()
    for u in city_dict:
        for v in city_dict:
            if u != v:
            	x_dist = city_dict[u]['x'] - city_dict[v]['x']
            	y_dist = city_dict[u]['y'] - city_dict[v]['y']
            	val = int(round(sqrt(x_dist**2 + y_dist**2)))
            	graph.add_edge(u, v, weight= val)

    # passing the graph to TourBuilder
    builder = TourBuilder(graph)
    kwargs = vars(args).copy()
    tour_data = builder.build_tour(**kwargs)

    # Formatting output file name
    if args.algorithm == 'bnb':
    	file_name = 'Output/' + str(args.instance) + '_' + str(args.algorithm) + '_' + str(args.limit)
    else:
    	file_name = 'Output/' + str(args.instance) + '_' + str(args.algorithm) + '_' + str(args.limit) + '_' + str(args.seed)

    sol_file = file_name + '.sol'
    trace_file = file_name + '.trace'

    # Writing solution file
    with open(sol_file, 'w') as f:
        f.write('{}\n'.format(tour_data[-1][1]))
        for edge in zip(tour_data[-1][2], tour_data[-1][2][1:]):
            f.write('{} {} {}\n'.format(edge[0], edge[1], graph[edge[0]][edge[1]]['weight']))

    # Writing trace file
    with open(trace_file, 'w') as f:
        for entry in tour_data:
            f.write('{:.2f} {}\n'.format(entry[0], entry[1]))


if __name__ == '__main__':
    main()