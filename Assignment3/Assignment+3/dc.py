import os
import time
from os import listdir
from os.path import isfile, join
import sys


class divide_and_conquer(object):
    def __init__(self):
        # Initialize your data structure here.

        self.day_arr = []       # each entry in this array contains array of interests
        self.data_files = []    # each entry in this array contains file name for each file in data folder
        

    def load_file_data(self,input_path):
        self.data_files = [f for f in listdir(input_path) if '.txt' in f and isfile(join(input_path, f))]


    def load_day_data(self,file_name):

        with open(file_name) as f:
            content = [line.strip('\n') for line in f.readlines()]
            temp = content[0].split(',')
            no_of_days, no_of_instances = int(temp[0]), int(temp[1])

            for i in range(1,no_of_instances+1,1):
                temp_days = content[i].split(',')
                days = [float(rate) for rate in temp_days]
                self.day_arr.append(days)
        

    def get_max_overlapping_arr(self,nums,start,end,middle):
        sum_val = 0
        left_sum = -sys.maxsize-1
        right_sum = -sys.maxsize-1
        s_i = 0
        e_i = 0

        # calculate left sum
        for i in range(middle,-1,-1):
            sum_val += nums[i]
            if sum_val >= left_sum:
                left_sum = sum_val
                s_i = i

        sum_val = 0
        # calculate right sum
        for i in range(middle+1,end+1,1):
            sum_val += nums[i]
            if sum_val >= right_sum:
                right_sum = sum_val
                e_i = i

        return left_sum+right_sum, s_i, e_i


    def get_max_sum_arr(self,nums,start,end):

        if start == end:
            return nums[end],start,end

        middle = int((start+end)/2)
        left_sum, left_start, left_end = self.get_max_sum_arr(nums,start,middle)
        right_sum, right_start, right_end = self.get_max_sum_arr(nums,middle+1,end)
        overlapping_sum, cross_start, cross_end = self.get_max_overlapping_arr(nums,start,end,middle)

        # print(left_sum,left_start,left_end)
        # print(right_sum,right_start,right_end)
        # print(overlapping_sum,cross_start,cross_end)
        # print('\n')

        i = 0
        j = 0
        max_sum = 0

        if left_sum > right_sum:
            i = left_start
            j = left_end
            max_sum = left_sum
        else:
            i = right_start
            j = right_end
            max_sum = right_sum

        if overlapping_sum > max_sum:
            i = cross_start
            j = cross_end
            max_sum = overlapping_sum

        return max_sum,i,j


    def save_output(self,file_name,data):
        file_name = 'output/bverma3_output_dc_' + file_name

        with open(file_name,'w') as f:
            for i in range(len(data)):
                f.write(data[i])

                # avoid printing extra line in the end
                if i < len(data)-1:
                    f.write('\n')


dc = divide_and_conquer()
path = os.path.join(os.path.dirname(__file__), 'data/')
dc.load_file_data(path)

for file in dc.data_files:
    # print("Loading data for file ", file,'\n')
    dc.load_day_data('data/'+file)
    # print("Finished loading data")
    output = []

    for day in dc.day_arr:
        start_time = time.time() * 1000
        val,i,j = dc.get_max_sum_arr(day,0,len(day)-1)
        exec_time = (time.time() * 1000) - start_time
        val = "%.2f" % val
        exec_time = "%.2f" % exec_time

        out_str = val #+ ',' + str(i+1) + ',' + str(j+1) + ',' + exec_time
        output.append(out_str)

    dc.save_output(file,output)

    # break

