#CSE6140 project local search of 2-opt implemented by Shenwei Gao
#In the given file, the N points represent specic Pokestop locations in some city
#x and y values are given as latitude and longitude points that have been multiplied by 1e6
import time
import sys
import math
import numpy
import random


#helper functions
#parse input file to store graph in a dictionary
#format is G{1:[x1, y1], 2:[x2, y2]...n:[xn,yn]}
def parseEdges(graph_file):
    graph = dict()
    file = open(graph_file, 'r')

    description = ''
    for i in range(1,6):
        description = description + file.readline()

    for line in file:
        nums = line.split()
        if len(nums)== 1:
            break
        else:
            graph[int(nums[0])] = [float(nums[1]), float(nums[2])]
    file.close()
    return graph

#create table to record distance between all cities
table = list()
def calculateAllDistance(G):
    for i in range(1, len(G)+1):
        row = list()
        for j in range(1, len(G)+1):
            x1 = G[i][0]
            y1 = G[i][1]
            x2 = G[j][0]
            y2 = G[j][1]
            xd = x1 - x2
            yd = y1 - y2
            dis = int(math.sqrt(xd*xd + yd*yd)+0.5)
            row.append(dis)
        table.append(row)

#Given a route in graph G, calculate the total euclidean distance in route
def calculateTotalDistance(route, G):
    dis = 0
    for i in range(len(route)):
        u = route[i]
        if i == len(route)-1:
            v = route[0]
        else:
            v = route[i+1]
        dis += table[u-1][v-1]
    return dis
'''
#Given a route in graph G, calculate the total euclidean distance in route
def calculateTotalDistance(route, G):
    dis = 0
    for i in range(len(route)):
        u = route[i]
        if i == len(route)-1:
            v = route[0]
        else:
            v = route[i+1]
        x1 = G[u][0]
        y1 = G[u][1]
        x2 = G[v][0]
        y2 = G[v][1]
        xd = x1 - x2
        yd = y1 - y2
        dis += int(math.sqrt(xd*xd + yd*yd)+0.5)
    return dis
'''

# helper function for 2 opt
#swap the route within the given index [i,k]
def twooptSwap(route, i, k):
    newroute = []
    for j in range(i):
        newroute.append(route[j])
    dec = 0
    for j in range(i, k+1):
        newroute.append(route[k-dec])
        dec += 1
    for j in range(k+1, len(route)):
        newroute.append(route[j])
    return newroute


#main function of 2 opt
def twoopt(G, random_seed, cutoff_time, output_trace_file, start_time):
    end_time = start_time + float(cutoff_time)
    random.seed(random_seed) #random seed
    existing_route = random.sample(range(1,len(G)+1),len(G)) # initialize arbitrary existing route
    output = open(output_trace_file, 'w')

    flag = 1 #flag for imporved solution
    total_best_distance = 100000000
    best_trace_distance = 100000000
    total_best_route = []
    avg_running_time = 0
    times = 0
    pre_timestamp = start_time
    #program stops when reaching cutoff time
    eps = 1.0 / 100000 
    while end_time - time.time()  > eps:
        #new solution appeared
        if(flag == 0):
            #existing_best_distance = calculateTotalDistance(existing_route, G)
            #compare with previous solution

            if(best_distance < total_best_distance):
                total_best_distance = best_distance
                total_best_route = existing_route[:]
                #print str(time.time()-start_time) + "\n"
            #output.write(str(time.time()-start_time) + "  ")
            #output.write(str(best_distance)+"\n")

            existing_route = random.sample(range(1,len(G)+1),len(G))
            '''
            #calcuate average running time
            avg_running_time += time.time()-pre_timestamp
            pre_timestamp = time.time()
            times += 1
            '''

        #find optimal solution with give arbitrary route
        best_distance = calculateTotalDistance(existing_route, G)
        size = len(existing_route)
        for i in range(size-1):
            for k in range(i+1, size):
                flag = 0
                new_route = twooptSwap(existing_route, i, k) #swap inside the route
                new_distance = calculateTotalDistance(new_route, G) #calculate new distance
                if new_distance < best_distance:
                    existing_route = new_route[:]
                    flag = 1
                    if new_distance < best_trace_distance:
                        best_trace_distance = new_distance
                        #record improved solution found
                        output.write(str(time.time()-start_time) + "  ")
                        output.write(str(new_distance)+"\n")
                        #calcuate average running time
                        avg_running_time += time.time()-pre_timestamp
                        pre_timestamp = time.time()
                        times += 1
                    break
            if flag == 1:
                break

    #check if there exists an imporved solution

    if total_best_distance == 100000000:
        #output.write(str(time.time()-start_time)+ "  ")
        #output.write(str(best_distance)+"\n")
        #print avg_running_time/times
        return existing_route
    else:
        #print avg_running_time/times
        return total_best_route


def main():

    num_args = len(sys.argv)

    if num_args < 4:
        print ("python 2opt.py graph_file cutoff_time random_seed")
        exit(1)

    graph_file = sys.argv[1]
    cutoff_time = sys.argv[2]
    random_seed = sys.argv[3]

    #create output filename
    cityname = sys.argv[1].split(".")
    output_file = cityname[0] + "_LS1_" + str(cutoff_time) + "_" + str(random_seed) + ".sol"
    output_trace_file = cityname[0] + "_LS1_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"

    start_time = time.time()
    G = parseEdges(graph_file) #parse input file
    calculateAllDistance(G) #create table to record distance between all cities
    route = twoopt(G, random_seed, cutoff_time, output_trace_file, start_time) #run 2 opt algorithm
    distance = calculateTotalDistance(route, G) #calculate optimal distance

    #write optimal route into ouput file
    output = open(output_file, 'w')
    output.write(str(int(distance))+ "\n")
    for i in range(len(route)):
        u = route[i]
        if i == len(route)-1:
            v = route[0]
        else:
            v = route[i+1]
        edge = [u, v]
        weight = calculateTotalDistance(edge, G)/2
        output.write(str(u)+ " " + str(v) + " "+ str(int(weight)) + "\n")

    #print distance
    #print time.time()-start_time
    # print route



if __name__ == '__main__':
    # run the experiments
    main()
