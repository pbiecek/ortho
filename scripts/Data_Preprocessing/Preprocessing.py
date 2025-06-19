import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
import math
from sklearn import preprocessing
from PIL import Image, ImageDraw
from collections import Counter
import statistics

def determine_relationship(age1, age2):
    if age1 <= 12 and age2 <= 12:
        return "Child"
    elif (age1 >age2 and age2 <= 12 and age1 >= 18) or \
         (age2 >age1 and age1 <= 12 and age2 >= 18):
        return "Child&Adult"
    elif age1 >= 18 and age2 >= 18:
        return "Adult"
    else:
        return -1
        
def remove_begin(datax,datay):
    rowsx_to_remove = 0
    rowsy_to_remove = 0
    for i in datax:
        if i != 0:
            break
        if i == 0:
            rowsx_to_remove += 1
    for j in datay:
        if j != 0:
            break
        if j == 0:
            rowsy_to_remove += 1
    rows_to_remove = min([rowsx_to_remove,rowsy_to_remove])
    datax_new = datax[rows_to_remove-1:]
    datay_new = datay[rows_to_remove-1:]
    return datax_new,datay_new

def interpolate(x,time):
    new_x = []
    for i in range(len(x)-1):
        diff = parse_time(time[i],time[i+1])
        num_interpolate = take_integer(diff / 16.67)
        if num_interpolate > 1 :
            new_x = new_x + [x[i]] * (num_interpolate)    
        if num_interpolate <=1 :
            new_x.append(x[i])
        if i == len(x)-2:
            new_x.append(x[i+1])
    return new_x


def take_integer(num):
    dit = num-int(num)
    if dit >= 0.5:
        ans = math.ceil(num)
    if dit < 0.5:
        ans = int(num)
    return ans

def parse_time(time_str_1,time_str_2):
    second = (datetime.strptime(time_str_2, '%H:%M:%S:%f') - datetime.strptime(time_str_1, '%H:%M:%S:%f')).total_seconds()
    return second*1000

def calculate_total_distance(x_list, y_list):
    x_arr = np.array(x_list)
    y_arr = np.array(y_list)
    dx = np.diff(x_arr)
    dy = np.diff(y_arr)
    distances = np.sqrt(dx ** 2 + dy ** 2)
    return distances.sum()

def calculate_initial_still_time(x_coords, y_coords, interval=16.67):
    still_frames = -1
    for x, y in zip(x_coords, y_coords):
        if x == 0 and y == 0:
            still_frames += 1
        if x != 0 or y != 0:
            return still_frames * interval
    
