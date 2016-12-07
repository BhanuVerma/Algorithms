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

def all_same(items):
    return all(x == items[0] for x in items)

#simulated annealing
def annealing(G,random_seed, cutoff_time, output_trace_file, start_time):
    end_time = int(start_time) + int(cutoff_time)
    random.seed(random_seed) #random seed
    current_route = random.sample(range(1,len(G)+1),len(G)) # initialize arbitrary existing route
    output = open(output_trace_file, 'w')

    temperature = 1000
    temperature_min = 0.0001
    cooling_rate = 0.99
    best_route = []
    best_distance = 1000000000000
    avg_running_time = 0
    times = 0
    pre_timestamp = start_time
    q = list()

    iter = 0
    eps = 1.0 / 100000
    while temperature > temperature_min or end_time - time.time()  > eps:
        #if current route has not been changed for a while, initialize it to an arbitrary route
        if len(q) == 500 and all_same(q):
            current_route = random.sample(range(1,len(G)+1),len(G)) # initialize arbitrary existing route

        #randomly exchange the order of two cities for new route
        index = random.sample(range(len(G)), 2)
        new_route = current_route[:]
        new_route[index[0]], new_route[index[1]] = new_route[index[1]], new_route[index[0]]

        #compare new distance with current distance
        current_distance = calculateTotalDistance(current_route, G)
        new_distance = calculateTotalDistance(new_route, G)
        diff = new_distance - current_distance
        #print current_distance

        #If the new distance, computed after the change, is shorter than the current distance, it is kept.
        #If the new distance is longer than the current one, it is kept with a certain probability.
        if diff < 0 or math.exp(-diff/temperature) > random.random():
            current_distance = new_distance
            current_route = new_route[:]

        #record the previous 500 current distance in a queue
        if(len(q) < 500):
            q.append(current_distance)
        else:
            q.pop(0)
            q.append(current_distance)

        #update improved solution
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_route[:]
            #record improved solution found
            output.write(str(time.time()-start_time) + "  ")
            output.write(str(best_distance)+"\n")
            #calcuate average running time
            avg_running_time += time.time()-pre_timestamp
            pre_timestamp = time.time()
            times += 1

        #update the temperature at every iteration by slowly cooling down
        temperature = temperature * cooling_rate
        iter += 1
    #print "avg running time"
    #print avg_running_time/times
    return best_route


def main():

    num_args = len(sys.argv)

    if num_args < 4:
        print ("python annealing.py graph_file cutoff_time random_seed")
        exit(1)

    graph_file = sys.argv[1]
    cutoff_time = sys.argv[2]
    random_seed = sys.argv[3]

    #create output filename
    cityname = sys.argv[1].split(".")
    output_file = cityname[0] + "_LS2_" + str(cutoff_time) + "_" + str(random_seed) + ".sol"
    output_trace_file = cityname[0] + "_LS2_" + str(cutoff_time) + "_" + str(random_seed) + ".trace"

    start_time = time.time()
    G = parseEdges(graph_file) #parse input file
    calculateAllDistance(G) #caculate total distance table
    route = annealing(G, random_seed, cutoff_time, output_trace_file, start_time) #run simulated annealing algorithm
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



if __name__ == '__main__':
    # run the experiments
    main()
