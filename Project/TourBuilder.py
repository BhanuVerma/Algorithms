# Central engine file that reads the data and calls different classes as per given arguments, by Bhanu Verma
import BranchAndBound
import MSTApprox
import NNApprox
import Opt2Search
import SimulatedAnnealing
import networkx as nx
from os.path import isfile
from math import sqrt
import argparse
import sys


class TourBuilder:
    def __init__(self, graph):
        self.graph = graph

    def build_tour(self, instance='Cincinnati', algorithm='BnB', seed=1, limit=1):

        if algorithm == 'BnB':
            bnb = BranchAndBound.BranchAndBound(self.graph,limit)
            return bnb.generate_tour()
        elif algorithm == 'MSTApprox':
            approx_1 = MSTApprox.MSTApprox(self.graph,instance,seed,limit)
            approx_1.generate_tour()
        elif algorithm == 'Heur':
            approx_2 = NNApprox.NNApprox(self.graph,instance,seed,limit)
            approx_2.generate_tour()
        elif algorithm == 'LS1':
            ls_1 = Opt2Search.Opt2Search(self.graph,instance,seed,limit)
            ls_1.generate_tour()
        elif algorithm == 'LS2':
            ls_2 = SimulatedAnnealing.SimulatedAnnealing(self.graph,instance,seed,limit)
            ls_2.generate_tour()
        else:
            return None


def main():

    # Optimal Tour Lengths
    opt_tour_lengths = {
        'SanFrancisco': 810196,
        'NYC': 1555060,
        'Roanoke': 655454,
        'Atlanta': 2003763,
        'Champaign': 52643,
        'Cincinnati': 277952,
        'Philadelphia': 1395981,
        'UKansasState': 62962,
        'Toronto': 1176151,
        'UMissouri': 132709,
        'Boston': 893536,
        'Denver': 100431
    }

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

    if args.algorithm == 'BnB':
        tour_data = builder.build_tour(**kwargs)
        file_name = 'Output/' + str(args.instance) + '_' + str(args.algorithm) + '_' + str(args.limit)

        sol_file = file_name + '.sol'
        trace_file = file_name + '.trace'

        # Generating solution file
        with open(sol_file, 'w') as f:
            f.write('{}\n'.format(tour_data[-1][1]))
            for edge in zip(tour_data[-1][0], tour_data[-1][0][1:]):
                f.write('{} {} {}\n'.format(edge[0], edge[1], graph[edge[0]][edge[1]]['weight']))

        # Generating trace file
        with open(trace_file, 'w') as f:
            for entry in tour_data:
                f.write('{:.2f} {}\n'.format(entry[2], entry[1]))

        if tour_data:
            opt = opt_tour_lengths[args.instance]
            rel_err = (tour_data[-1][1] - opt)/opt
            print('Relative error is ', rel_err)
    else:
        builder.build_tour(**kwargs)

    # # Formatting output file name
    # if args.algorithm == 'BnB':
    #   file_name = 'Output/' + str(args.instance) + '_' + str(args.algorithm) + '_' + str(args.limit)
    # else:
    #   file_name = 'Output/' + str(args.instance) + '_' + str(args.algorithm) + '_' + str(args.limit) + '_' + str(args.seed)

if __name__ == '__main__':
    main()