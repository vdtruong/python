#!/usr/bin/env python

'''
Filename: plot_tel_ADC_data.py
Project: REASON
Company: Jet Propulsion Laboratory
'''

import matplotlib.pyplot as plt
import os                     
import sys
#import math

file_to_be_plot = sys.argv[-1]

# 05-07-2018 This script will plot the voltage telemetry ADC values
# versus time as each ADC value is cycled from 0 to 3.0 V.
# The plot for each signal will be saved.

f = open(file_to_be_plot)
d = f.readlines()
# This is the 2d array of the data file.
data_list = [x.split(",") for x in d]

# This is the time row (list in python).
time_list = data_list[0]

# pop out the time label
# Remeber after popping the first element
# of the list, the time_list has one less
# element. In this case, the label.
pop_label_of_time_list = time_list.pop(0)

# Starting time on x-axis
x_axis_strt = int(float(time_list[0]))
print(x_axis_strt)
time_list_lngth = len(time_list)
print(time_list_lngth)
time_res = float(time_list[1]) - float(time_list[0])
print(time_res)
# We find the end point of the x-axis.  We add 10% for some room.
x_axis_end = int(x_axis_strt + time_list_lngth*(time_res + 0.1*time_res))
print(x_axis_end)

# convert time string to float
# This is the x-axis.
float_time_list = [float(x) for x in time_list]
#print(float_time_list)

# The length of the data_list
# Should be the number of rows of the data file.
data_list_length = len(data_list)

# We will do a for loop to go through the data_list to graph the
# y values.  The length of the data_list will be 53, this includes the time
# row (list).  So we will actually do the for loop after the time row.

# This is the data_list row index after we extracted the time row.
# So we start at 1 instead of 0.
strt_row_index = 1

# may need to check on the range
for x in range(strt_row_index, data_list_length): 
	# Pick the next row
	y_val = data_list[x]
	
	# Pop the label
	y_val_label = y_val.pop(0)
	
	# convert string to float
	float_y_val = [float(y) for y in y_val]
	
	# plot y versus x	     
	plt.plot(float_time_list, float_y_val, linewidth = 2)
	
	# Use this for scatter plot, no connecting lines.
	#plt.scatter(float_time_list, float_y_val, s = 5)
	
	plt.title("Telemetry ADC vs Time")
	plt.xlabel(pop_label_of_time_list)
	plt.ylabel(y_val_label)
	plt.axis([x_axis_strt, x_axis_end, 0, 65535])
	#plt.show()
	
	save_results_to = '/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_processing/log/'
	plot_file_name = "%s.png" % y_val_label 
	#print(plot_file_name)
	# This works.
	plt.savefig(save_results_to + plot_file_name)
	
	# need to clear the plot for the next set of data
	plt.clf()
f.close()
