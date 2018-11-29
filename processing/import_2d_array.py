#!/usr/bin/env python

'''
File: import_2d_array.py
Project: REASON
Company: Jet Propulsion Laboratory
'''

import matplotlib.pyplot as plt
import os     

# This script will print the telemetry ADC values
# versus time as each ADC value is cycled from 0 to 3.0 V.


#from os import path
#file_path = path.relpath("log/")
#with open(file_path) as f:
f = open(r'C:\Users\vdtruong\Documents\GitHub\EGSE_Instrument_Control\vasa_processing\log\20180502\res_des_tlm_adc_vrefsim_cmd_comprehensive_2018_05_02_2_packet_adc_tlm_out.txt')
#f = open(abs_file_path)
d = f.readlines()
#print[x.split(",") for x in d]
# This the 2d array of the data file.
data_list = [x.split(",") for x in d]
#print big_list

# This is the time row (list in python).
time_list = data_list[0]
#print first_list

# pop out the time label
pop_label_of_time_list = time_list.pop(0)

# convert time string to float
# This is the x-axis.
float_time_list = [float(x) for x in time_list]
#print float_time_list

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
	#print y_val_label
	#print y_val
	# convert string to float
	float_y_val = [float(y) for y in y_val]
	#print float_y_val
	# plot y versus x	 
	# Scatter plots of individual telemetry ADC    
	#fig = plt.scatter(float_time_list, float_y_val)
	# plt.plot will connect the dots
	#fig = plt.plot(float_time_list, float_y_val)
	plt.scatter(float_time_list, float_y_val)
	plt.title("Voltage Telemetry ADC vs Time")
	plt.xlabel(pop_label_of_time_list)
	plt.ylabel(y_val_label)
	#plt.show()
	plot_file_name = "%s.png" % y_val_label 
	#print plot_file_name
	#plt.savefig(r'\Users\vdtruong\Documents\GitHub\EGSE_Instrument_Control\vasa_processing\log\20180502\plot_file_name')
	plt.savefig(plot_file_name)
	# need to clear the plot for the next set of data
	plt.clf()
f.close()