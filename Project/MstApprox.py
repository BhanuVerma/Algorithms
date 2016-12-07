import numpy as np
import math
import sys
import timeit as tt

class MSTApprox:

    def __init__(self,graph,instance,seed,limit=600):
        self.city = instance
        self.random_seed = seed
        self.cutoff_time = limit
        self.inf=float("inf")
        self.path = []
        self.total=0.0

    def mst(self,G):
        
        GG = np.array(G)
        E = []
        visited = [0]

        while len(visited) < len(G):
            (row,col) = np.unravel_index(GG[visited].argmin(),GG[visited].shape)

            visited.append(col)
            E.append((visited[row],col))
        
            s = [(col,v) for v in visited]
        
            for (k,v) in s:
                GG[k][v] = self.inf
                GG[v][k] = self.inf

        #duplicate mst
        E2 = [(y,x) for (x,y) in E]
        E.extend(E2)

        return E

    def preorder(self,E,parent):
        if parent not in self.path:
            self.path.append(parent)
            child = [x[1] for x in E if x[0] == parent]
            if len(child) > 0 :
                for node in child:
                    self.preorder(E,node)
            else:
                return

    def walk(self,G):
        O = []
        for i in range(0,len(self.path)-1):
            dist = G[self.path[i]][self.path[i+1]]
            O.append((self.path[i],self.path[i+1],dist))
            self.total += dist
        dist = G[self.path[-1]][self.path[0]]
        O.append((self.path[-1],self.path[0],dist))
        self.total+=dist

        return O

    def read_data(self):
        L = []
        with open('./DATA/'+self.city+'.tsp') as f:
            next(f)
            next(f)
            next(f)
            next(f)
            next(f)
            for line in f:
                if line == 'EOF\n':
                    break
                l=line[:-1].split(' ')
                #print line
                L.append({'x':float(l[1]),'y':float(l[2])})
            
            n = len(L)
            G = np.zeros((n,n))

            for i in range(n):
                for j in range(n):
                    if i == j:
                        G[i][j] = self.inf
                    else:
                        G[i][j] = int(round(math.sqrt((L[i]['x'] - L[j]['x']) ** 2 + (L[i]['y'] - L[j]['y']) ** 2)))
        return G


    def write_data(self,output,total):
        total = (str)((int)(total))
        with open('Output/'+self.city+ "_MSTApprox_" + str(self.cutoff_time) + "_" + str(self.random_seed)+'.sol','w') as f:
            f.write(total)
            f.write('\n')
            for (a,b,c) in output:
                f.write(str(a) + ' ' + str(b) + ' ' + str(int(c)))
                f.write('\n')
            

    def write_trace(self,time,total):
        with open('Output/'+self.city + "_MSTApprox_" + str(self.cutoff_time) + "_" + str(self.random_seed)+'.trace','w') as f:
            f.write('{:.2f} {}\n'.format(time, total))


    def generate_tour(self):
        start = tt.default_timer()
        self.total = 0.0
        self.path = []
        graph = self.read_data()
        edge = self.mst(graph)
        self.preorder(edge,self.random_seed)
        output = self.walk(graph)
        stop = tt.default_timer()
        self.write_trace(stop-start,int(self.total))
        self.write_data(output,self.total)
        
