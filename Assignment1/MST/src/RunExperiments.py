#!/usr/bin/python
##  CSE6140 HW1
##  This assignment requires installation of networkx package if you want to make use of available graph data structures or you can write your own!!
##  Please feel free to modify this code or write your own

import networkx as nx
import time
import sys

class UnionFind:
    # Union-find data structure. Based on Josiah Carlson's code,
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
    # with significant additional changes by D. Eppstein.
    # http://www.ics.uci.edu/~eppstein/PADS/UnionFind.py
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def parseEdges(graph_file):
    with open(graph_file) as file:
        count = 0
        edge_list = []
        for line in file:
            if count == 0:
                pass
            else:
                edge = line.split()
                edge_list.append((int(edge[0]),int(edge[1]),int(edge[2])))
            count += 1

    graph = nx.MultiGraph()
    graph.add_weighted_edges_from(edge_list)
    edge_list.sort(key=lambda tup: tup[2])  # sorts in place

    return graph,edge_list


def computeMST(graph,edge_list):
    # KRUSKAL ALGORITHM
    t = []
    set_list = []
    unique_d = {}
    cost = 0
    uf = UnionFind()

    for i in range(0,len(edge_list)):
        u,v = edge_list[i][0], edge_list[i][1]
        if unique_d.get((u,v),None) == None:
            unique_d[(u,v)] = 1  
            if uf[u] != uf[v]:
                t.append((u,v,edge_list[i][2]))
                cost += edge_list[i][2]
                uf.union(u,v)

    return cost,uf,t


def recomputeMST(u,v,w,G,uf,mst,cost):
    if uf[u] != uf[v]:
        mst[u][v]["weight"] = w
        cost += w
        uf.union(u,v)
    else:
        if mst.get_edge_data(u,v) or mst.get_edge_data(v,u):
            d = {}
            if mst.get_edge_data(u,v):
                d = mst.get_edge_data(u,v)
                if isinstance(d,dict):
                    if w < d['weight']:
                        cost += w - d['weight']
                        mst[u][v]['weight'] = w
            if mst.get_edge_data(v,u):
                d = mst.get_edge_data(v,u)
                if isinstance(d,dict):
                    if w < d['weight']:
                        cost += w - d['weight']
                        mst[v][u]['weight'] = w
        else:
            path = nx.shortest_path(mst,u,v)
            tri = []
            for i in range(0,len(path)-1):
                tri.append((path[i],path[i+1],mst[path[i]][path[i+1]]['weight']))
            tri.sort(key=lambda tup: tup[2])  # sorts in place
            if w < tri[-1][2]:
                mst.remove_edge(tri[-1][0],tri[-1][1])
                mst.add_edge(u,v,weight=w)
                cost += w - tri[-1][2]
    return cost,uf,mst


def main():

    num_args = len(sys.argv)

    if num_args < 4:
        print("error: not enough input arguments")
        exit(1)

    graph_file = sys.argv[1]
    change_file = sys.argv[2]
    output_file = sys.argv[3]

    #Construct graph
    G,edge_list = parseEdges(graph_file) #TODO: Write this method to read the graph file input

    start_MST = time.time() #time in seconds
    MSTweight,uf,t = computeMST(G,edge_list) #TODO: Write this method to return total weight of MST
    total_time = (time.time() - start_MST) * 1000 #to convert to milliseconds

    # Write initial MST weight and time to file
    output = open(output_file, 'w')
    output.write(str(MSTweight) + " " + str(total_time) + "\n")

    mst = nx.Graph()
    mst.add_weighted_edges_from(t)
    recomputeTime = 0
    #Changes file
    with open(change_file, 'r') as changes:
        num_changes = changes.readline()
        new_weight = MSTweight
        for line in changes:
            #parse edge and weight
            edge_data = list(map(lambda x: int(x), line.split()))
            assert(len(edge_data) == 3)

            u,v,weight = edge_data[0], edge_data[1], edge_data[2]

            #call recomputeMST function
            start_recompute = time.time()
            new_weight, uf, mst = recomputeMST(u,v,weight,G,uf,mst,new_weight)
            total_recompute = (time.time() - start_recompute) * 1000 # to convert to milliseconds
            recomputeTime += total_recompute

            #write new weight and time to output file
            output.write(str(new_weight) + " " + str(total_recompute) + "\n")


if __name__ == '__main__':
    # run the experiments
    main()
