import random
import sys
import pandas as pd
import numpy as np
from time import time
from scipy.spatial.distance import squareform, pdist


def diag_inf(mat, i): 
    """
    Change the value of the ith element in a matrix diagonal to positive infinty
    """
    mat.loc[i,i] = float('Inf')


def prepare_data(city):
    """
    Perform data ETL on the original dataset
    1. Extract data from the original file
    2. Transform the dataset into a dataframe
    3. Generate a distance matrix based on the x, y values of locations
    """
    # Get the data file path, open and read the original dataset
    # If prefer to enter city name rather than filename: 
    # file_path = './DATA/'+ city + '.tsp' 
    file_path = './DATA/'+ city
    with open (file_path) as f: data = f.readlines()
        
    # Draw the information of locations, and based on the information we create a dataframe
    loc_details = data[5:-1] 
    locs = map(lambda x: x.rstrip().split(' '), loc_details) 
    num_locs = len(locs) 
    df = pd.DataFrame(locs).loc[:,[1,2]] 
    df.index = xrange(1,1+num_locs)
    
    # Generate the distance matrix to represent the Euclidean distance between two locations
    dist_matrix = pd.DataFrame(squareform(pdist(df)), columns=df.index.unique(), index=df.index.unique())
    
    # Change the diagonal of the distance matrix to infinity to prepare for the future sorting
    mod = map(lambda x: diag_inf(dist_matrix, x), range(1, num_locs+1))
    return dist_matrix, num_locs


def Heur(randSeed, dist_matrix, num_locs, cutoff):
    """
    Construct Heuristics with Nearest Neighbor 
    """ 
    # Initialization
    unvisited = range(1, num_locs+1)
    total_distance = 0
    res = []
    start_time = time()
    
    # Choose a random index as the random start loction of our path
    random.seed(randSeed)
    start = random.randrange(1, num_locs+1)
    temp = start
    
    # Main heuristic algorithm
    while len(unvisited) != 0 and time() - start_time < cutoff:
        unvisited.remove(temp)
        row = dist_matrix.loc[temp, :]
        sort_index = map(lambda x: x+1, np.argsort(row))
        if len(unvisited) != 0: 
            min_index = filter(lambda x: x in unvisited, sort_index)[0]
            dist = dist_matrix.loc[temp,min_index]
            res.append([temp, min_index, int(dist)])
            temp = min_index
            total_distance += dist
        else: 
            back_distance = dist_matrix.loc[temp,start]
            total_distance += back_distance
            res.append([temp, start, int(back_distance)])
            res = [int(total_distance)] + res
            res.append(round(time()-start_time, 2))
            # res.append(time()-start_time)
            return res



def main():
    num_argv = len(sys.argv)
    if (num_argv < 4): 
        print"python Heur.py filename Heur cutoff randSeed"
        exit(1)

    city = sys.argv[1]
    cutoff = sys.argv[2]
    randSeed = sys.argv[3]
    
    dist_mat, num_locs = prepare_data(city)
    res = Heur(randSeed, dist_mat, num_locs, cutoff)

    city = city.split('.')[0] # If choose city name rather than filename, comment out this line
    
    # Output the result into a sol file 
    with open (city+'_Heur_'+str(cutoff)+'_'+str(randSeed)+'.sol', 'w') as handle:
        handle.write(str(res[0]) + '\n')
        for element in res[1:-1]:
            output_str = "{} {} {}\n".format("%.0f" % element[0], "%.0f" % element[1], "%.0f" % element[2])
            handle.write(output_str)
    # Ouput the trace into a trace file
    with open(city+'_Heur_'+str(cutoff)+'_'+str(randSeed)+'.trace', 'w') as handle:
        handle.write("%.2f" % res[-1] + ', ' + str(res[0]))
    # print res[-1]
    # print res[0]


if __name__ == '__main__':
    # run the experiments
    main()

