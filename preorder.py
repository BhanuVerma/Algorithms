
import numpy as np
import math
import sys
import timeit as tt

#E=[[1,2],[2,3],[6,7],[6,8],[2,4],[2,5],[8,9],[1,6]]
cites = ["Atlanta"	,	"Cincinnati"		,"SanFrancisco",
"Boston",		"Denver"	,	"Toronto",		"NYC"	,		"UKansasState",
"Champaign"	,	"Philadelphia",	"UMissouri",		"Roanoke"]
#G=[[1000,1,1,1,1],[1,1000,1.414,2,1.414],[1,1.414,1000,1,2],[1,2,1.414,1000,1.414],[1,1.414,2,1.414,1000]]
inf=float("inf")
path = []
total=0.0

def mst(G):
	
	GG = np.array(G)
	E = []
	visited = [0]

	while len(visited) < len(G):

		(row,col) = np.unravel_index(GG[visited].argmin(),GG[visited].shape)

		visited.append(col)
		E.append((visited[row],col))
	
		s = [(col,v) for v in visited]
	
		for (k,v) in s:
			GG[k][v] = inf
			GG[v][k] = inf
	#duplicate mst
	E2 = [(y,x) for (x,y) in E]
	E.extend(E2)

	return E

def preorder(E,parent):
	global path
	if parent not in path:
		path.append(parent)
		child = [x[1] for x in E if x[0] == parent]
		if len(child) > 0 :
			for node in child:
				preorder(E,node)
		else:
			return

def walk(G):
	global path
	global total
	O = []
	for i in range(0,len(path)-1):
		dist = G[path[i]][path[i+1]]
		O.append((path[i],path[i+1],dist))
		total += dist
	dist = G[path[-1]][path[0]]
	O.append((path[-1],path[0],dist))
	total+=dist
	return O

def read_data(fname):
	L = []
	with open('./DATA/'+fname+'.tsp') as f:
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

		for i in xrange(n):
			for j in xrange(n):
				if i == j:
					G[i][j] = inf
				else:
					G[i][j] = math.sqrt((L[i]['x'] - L[j]['x']) ** 2 + (L[i]['y'] - L[j]['y']) ** 2)
	return G

def write_data(output,total,city):
	total = (str)((int)(total))
	with open(city+'.sol','wb') as f:
		f.write(total)
		f.write('\n')
		for (a,b,c) in output:
			f.write(str(a) + ' ' + str(b) + ' ' + str(c))
			f.write('\n')
			
def write_trace(time,total,city):
	total = (str)((int)(total))
	time = (str)(time)
	with open(city+'.trace','wb') as f:
		f.write(time)
		f.write(' ')
		f.write(total)
		f.write('\n')
	
if __name__=="__main__":
	global path
	global total
	for city in cites:
		start = tt.default_timer()
		total = 0.0
		for seed in range(0,10):
			path = []
			graph = read_data(city)
			edge = mst(graph)
			preorder(edge,seed)
			output = walk(graph)
		stop = tt.default_timer()
		write_trace((stop-start)/10.0,total/10,city)
		write_data(output,total,city)
		#print 'node:' +str(len(output))
		#print 'average dist:' + str(total/10)
		#print 'time:' + str((stop-start)/10)
