#!/usr/bin/env python

'''
File: parse_telemetry_adc.py
Project: REASON
Company: Jet Propulsion Laboratory
'''

#import matplotlib.pyplot as plt
from conversion_functions import *
import math

parser = argparse.ArgumentParser(
			description="Parse packet file for telemetry ADC data.")
parser.add_argument("infile_filename", help="packet filename", 
					type=str)                   
parser.add_argument("-s", "--split", help="Enter -s to split into multiple files if exist.",
										action="store_true")
parser.add_argument("--raw", help="return raw ADC value instead of converted voltage/resistance", action="store_true")
args = parser.parse_args()

with open(args.infile_filename, "r") as infile:
	# Read in entire file
	lines = infile.readlines()
	data = []
	for index, line in enumerate(lines):
		data.append(line.split(","))
	time_list = [data[idx][0].strip() for idx, value in enumerate(data)]
	msgtype_list = [data[idx][1].strip() for idx, value in enumerate(data)]
	packet_list = [data[idx][2].strip() for idx, value in enumerate(data)]

	# Preserve only AXI Read Response messages
	time_list = [time_list[idx] for idx, msgtype in enumerate(msgtype_list) if 'AXI Read Response' in msgtype]
	packet_list = [packet_list[idx] for idx, msgtype in enumerate(msgtype_list) if 'AXI Read Response' in msgtype]

	#print(time_list)
	#print(len(time_list))
	#print(packet_list)
	#print(len(packet_list))
	
# Extract read_data from packet from each AXI read response
read_data_list = []
for idx, packet in enumerate(packet_list):
	# Take current packet and divide it into list of bytes
	packet_bytes = [packet[idy:idy+2] for idy in range(0,len(packet),2)]

	# Extract read data length (in number of bytes) from current packet
	read_data_nbytes = int("".join(packet_bytes[19:21]), 16)	# bytes 19 and 20 of read response (shouldn't this be n-1. why is it 256?)
	
	# Extract read data from current packet based on read data length
	read_data_list.append(packet_bytes[21:21+read_data_nbytes])

#print(read_data_list)
#print(read_data_list[340][0:10])	
#print(len(read_data_list))

# Length per file.
len_per_file = 341

if len(read_data_list) > len_per_file:              
	num_of_files = int(len(read_data_list) / len_per_file) + (len(read_data_list) % len_per_file > 0)
	#print(num_of_files)
else:
	num_of_files = 1
	
# For now, each telemetry ADC test sequence only performs a single telemetry 
# ADC capture
# Default telemetry ADC measurement plan ADC channel address assignment
telem_adc_data = read_data_list[0]       
#print(len(telem_adc_data))

# ADC channel name, LSByte index, MSByte index (according to Python indexing)
default_meas_plan = [
						['pcu_temp_1', 0, 1],
						['hfrx_temp_1', 2, 3],
						['synth_10v', 4, 5],
						['pcu_10v_synth_itlm', 6, 7],
						['pcu_temp_2', 16, 17],
						['hfrx_temp_2', 18, 19],
						['hfrx_current', 20, 21],
						['pcu_5v_pol_itlm', 22, 23],
						['synth_temp', 32, 33],
						['hftxea_temp', 34, 35],
						['hf_5v_vtlm', 36, 37],
						['pcu_5v_pol_vtlm', 38, 39],
						['hf_coupler_temp', 48, 49],
						['vhftxea_temp', 50, 51],
						['hf_power_detect', 52, 53],
						['pcu_10v_synth_vtlm', 54, 55],
						['hftx_temp', 64, 65],
						['vhfrxp_temp', 66, 67],
						['vhf_power_detect', 68, 69],
						['pcu_in_vtlm', 70, 71],
						['vhftx_temp', 80, 81],
						['vhfrxs_temp', 82, 83],
						['vhf_5v_vtlm', 84, 85],
						['hfrx_5v', 86, 87],
						['vhftxp_coupler_temp', 96, 97],
						['vhfrxp_current', 100, 101],
						['hfrx_12v', 102, 103],
						['vhftxs_coupler_temp', 112, 113],
						['vhfrxs_current', 116, 117],
						['hftx_current', 118, 119],
						['spare_temp_0', 128, 129],
						['pol_1v_itlm', 132, 133],
						['hftx_voltage', 134, 135],
						['spare_temp_1', 144, 145],
						['pol_1p8v_itlm', 148, 149],
						['vhftx_current', 150, 151],
						['spare_temp_2', 160, 161],
						['pol_2p5v_itlm', 164, 165],
						['vhftx_voltage', 166, 167],
						['spare_temp_3', 176, 177],
						['pol_3p3v_itlm', 180, 181],
						['vhfrxp_5v', 182, 183],
						['pol_1v_vtlm', 196, 197],
						['vhfrxp_12v', 198, 199],
						['pol_1p8v_vtlm', 212, 213],
						['vhfrxs_5v', 214, 215],
						['fpga_diode_temp', 226, 227],
						['pol_2p5v_vtlm', 228, 229],
						['vhfrxs_12v', 230, 231],
						['cal_resistor_0', 240, 241],
						['cal_resistor_1', 242, 243],
						['pol_3p3v_vtlm', 244, 245]
					]

#print (len(default_meas_plan))

fmt_pot = '{:<20} {:} ADC val {:>20} ohm'
fmt_dac = '{:<20} {:} ADC val {:>20} V'
v_supply = 5
nbit = 12
nlevel = math.pow(2, nbit)
v_per_level = v_supply/nlevel
i_src = 0.001
                           
#print(len(read_data_list))
                        
strt_of_sect = 0 # Starting sector of a data set

# If we have more than 1 file to save, we have multiple runs of the data.
if num_of_files > 1:
	# If the num_of_files is greater than 1, do we want to split the data up?
	if args.split:
		# If we split the data up, we need to save each run on a separate file.
		for i in range(num_of_files):
			# If this is the first file, the strt_of_sect is 0, else it is
			# strt_of_sect = strt_of_sect + 340 + 1.
			if i == 0:
				strt_of_sect = 0                     
				end_of_sect = strt_of_sect + (len_per_file - 1)
			else:
				strt_of_sect = strt_of_sect + len_per_file
				end_of_sect = strt_of_sect + (len_per_file - 1)
			
			#print(strt_of_sect)
			#print(end_of_sect)
			
			# The read_data_list[strt_of_sect:end_of_sect] is the length of each run.
			# The default_meas_plan is for each item (adc item) to be saved. In this case,
			# we will have 52 items, each of length read_data_list[strt_of_sect:end_of_sect].
			for telem_adc_data in read_data_list[strt_of_sect:end_of_sect]:
				for list_no, channel in enumerate(default_meas_plan):
					# Extract ADC channel measurements from start and end indexes specified 
					# in listing, and append
					channel_name = default_meas_plan[list_no][0]
					#print(channel_name)
					start_idx = default_meas_plan[list_no][1]
					#print(start_idx)
					end_idx = default_meas_plan[list_no][2] + 1
					#print(end_idx)
					meas = convert_hex_to_int(''.join(telem_adc_data[start_idx:end_idx]))	
					meas_avg = meas/16	# Only if average count is factor of 2 and > 16
					v_avg = meas_avg*v_per_level     
					#print(list_no)
					if not args.raw:
						if 'temp' in channel_name or 'resistor' in channel_name:
							temp_avg = v_avg/i_src	# Potentially additional factor of 2 due to missing resistor
							default_meas_plan[list_no].append(temp_avg)
						else:
							default_meas_plan[list_no].append(v_avg)
					else:
						default_meas_plan[list_no].append(meas)
					#print (default_meas_plan)
			#print(default_meas_plan)
				
			# Now we save the data on a file.
			outfile_filename = args.infile_filename.split('/')[-1].replace('.txt', '_adc_tlm_out_' + str(i) + '.txt')
			with open(args.infile_filename.replace('.txt', '_adc_tlm_out_' + str(i) + '.txt'), 'w') as outfile:
				print('\nPrinting telemetry ADC data to file %s.\n' % outfile_filename)
				outfile.write('time, %s\n' % ', '.join(map(str, time_list[strt_of_sect:end_of_sect])))
				#print(time_list)
				for list_no, channel in enumerate(default_meas_plan):
					channel_name = default_meas_plan[list_no][0]
					telem_adc_data_list = default_meas_plan[list_no][3:]	# Indexes 1 and 2 are packet byte indexes
					#print(telem_adc_data_list)
					outfile.write('%s, %s\n' % (channel_name, ', '.join(map(str, telem_adc_data_list))))
			#print(default_meas_plan)
			
			# Inititialize default_meas_plan before starting on another file.
			default_meas_plan = [
						['pcu_temp_1', 0, 1],
						['hfrx_temp_1', 2, 3],
						['synth_10v', 4, 5],
						['pcu_10v_synth_itlm', 6, 7],
						['pcu_temp_2', 16, 17],
						['hfrx_temp_2', 18, 19],
						['hfrx_current', 20, 21],
						['pcu_5v_pol_itlm', 22, 23],
						['synth_temp', 32, 33],
						['hftxea_temp', 34, 35],
						['hf_5v_vtlm', 36, 37],
						['pcu_5v_pol_vtlm', 38, 39],
						['hf_coupler_temp', 48, 49],
						['vhftxea_temp', 50, 51],
						['hf_power_detect', 52, 53],
						['pcu_10v_synth_vtlm', 54, 55],
						['hftx_temp', 64, 65],
						['vhfrxp_temp', 66, 67],
						['vhf_power_detect', 68, 69],
						['pcu_in_vtlm', 70, 71],
						['vhftx_temp', 80, 81],
						['vhfrxs_temp', 82, 83],
						['vhf_5v_vtlm', 84, 85],
						['hfrx_5v', 86, 87],
						['vhftxp_coupler_temp', 96, 97],
						['vhfrxp_current', 100, 101],
						['hfrx_12v', 102, 103],
						['vhftxs_coupler_temp', 112, 113],
						['vhfrxs_current', 116, 117],
						['hftx_current', 118, 119],
						['spare_temp_0', 128, 129],
						['pol_1v_itlm', 132, 133],
						['hftx_voltage', 134, 135],
						['spare_temp_1', 144, 145],
						['pol_1p8v_itlm', 148, 149],
						['vhftx_current', 150, 151],
						['spare_temp_2', 160, 161],
						['pol_2p5v_itlm', 164, 165],
						['vhftx_voltage', 166, 167],
						['spare_temp_3', 176, 177],
						['pol_3p3v_itlm', 180, 181],
						['vhfrxp_5v', 182, 183],
						['pol_1v_vtlm', 196, 197],
						['vhfrxp_12v', 198, 199],
						['pol_1p8v_vtlm', 212, 213],
						['vhfrxs_5v', 214, 215],
						['fpga_diode_temp', 226, 227],
						['pol_2p5v_vtlm', 228, 229],
						['vhfrxs_12v', 230, 231],
						['cal_resistor_0', 240, 241],
						['cal_resistor_1', 242, 243],
						['pol_3p3v_vtlm', 244, 245]
			]
	else: # if we do not split the file	
		for telem_adc_data in read_data_list:
			for list_no, channel in enumerate(default_meas_plan):
				# Extract ADC channel measurements from start and end indexes specified 
				# in listing, and append
				channel_name = default_meas_plan[list_no][0]
				#print(channel_name)
				start_idx = default_meas_plan[list_no][1]
				#print(start_idx)
				end_idx = default_meas_plan[list_no][2] + 1
				#print(end_idx)
				meas = convert_hex_to_int(''.join(telem_adc_data[start_idx:end_idx]))	
				meas_avg = meas/16	# Only if average count is factor of 2 and > 16
				v_avg = meas_avg*v_per_level     
				#print(list_no)
				if not args.raw:
					if 'temp' in channel_name or 'resistor' in channel_name:
						temp_avg = v_avg/i_src	# Potentially additional factor of 2 due to missing resistor
						default_meas_plan[list_no].append(temp_avg)
					else:
						default_meas_plan[list_no].append(v_avg)
				else:
					default_meas_plan[list_no].append(meas)
					#print (default_meas_plan)
		#print(default_meas_plan[0:2])
		
		# Now we save the data on a file.
		outfile_filename = args.infile_filename.split('/')[-1].replace('.txt', '_adc_tlm_out.txt')
		with open(args.infile_filename.replace('.txt', '_adc_tlm_out.txt'), 'w') as outfile:
			print('\nPrinting telemetry ADC data to file %s.\n' % outfile_filename)
			outfile.write('time, %s\n' % ', '.join(map(str, time_list)))
			#print(time_list)
			for list_no, channel in enumerate(default_meas_plan):
				channel_name = default_meas_plan[list_no][0]
				telem_adc_data_list = default_meas_plan[list_no][3:]	# Indexes 1 and 2 are packet byte indexes
				#print(telem_adc_data_list)
				outfile.write('%s, %s\n' % (channel_name, ', '.join(map(str, telem_adc_data_list))))
else: # If the num_of_files is only one.
	for telem_adc_data in read_data_list:
		for list_no, channel in enumerate(default_meas_plan):
			# Extract ADC channel measurements from start and end indexes specified 
			# in listing, and append
			channel_name = default_meas_plan[list_no][0]
			#print(channel_name)
			start_idx = default_meas_plan[list_no][1]
			#print(start_idx)
			end_idx = default_meas_plan[list_no][2] + 1
			#print(end_idx)
			meas = convert_hex_to_int(''.join(telem_adc_data[start_idx:end_idx]))	
			meas_avg = meas/16	# Only if average count is factor of 2 and > 16
			v_avg = meas_avg*v_per_level     
			#print(list_no)
			if not args.raw:
				if 'temp' in channel_name or 'resistor' in channel_name:
					temp_avg = v_avg/i_src	# Potentially additional factor of 2 due to missing resistor
					default_meas_plan[list_no].append(temp_avg)
				else:
					default_meas_plan[list_no].append(v_avg)
			else:
				default_meas_plan[list_no].append(meas)
				#print (default_meas_plan)
	#print(default_meas_plan[0:2])
		
	# Now we save the data on a file.
	outfile_filename = args.infile_filename.split('/')[-1].replace('.txt', '_adc_tlm_out.txt')
	with open(args.infile_filename.replace('.txt', '_adc_tlm_out.txt'), 'w') as outfile:
		print('\nPrinting telemetry ADC data to file %s.\n' % outfile_filename)
		outfile.write('time, %s\n' % ', '.join(map(str, time_list)))
		#print(time_list)
		for list_no, channel in enumerate(default_meas_plan):
			channel_name = default_meas_plan[list_no][0]
			telem_adc_data_list = default_meas_plan[list_no][3:]	# Indexes 1 and 2 are packet byte indexes
			#print(telem_adc_data_list)
			outfile.write('%s, %s\n' % (channel_name, ', '.join(map(str, telem_adc_data_list))))
# EOF