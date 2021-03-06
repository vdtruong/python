#!/usr/bin/env python

'''
File: parse_telemetry_adc_bkup.py
Project: REASON
Company: Jet Propulsion Laboratory
'''

#import matplotlib.pyplot as plt
from conversion_functions import *
import math

parser = argparse.ArgumentParser(
			description="Parse packet file for telemetry ADC data.")
parser.add_argument("infile_filename", help="packet filename.txt", 
					type=str)
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
	packet_list_length = len(packet_list)
	print packet_list_length
	
	# the time list of every AXI Read Response 
	#print(time_list)                          
	# the data list of every AXI Read Response
	#print(packet_list)

# Extract read_data from packet from each AXI read response
# Here the packet_list only contains 341 axi reads.
# That is one complete run.
# Everything that is done from here on is only for one
# run of test.  That is for 341 axi reads.
read_data_list = []
for idx, packet in enumerate(packet_list):
	# Take current packet and divide it into list of bytes
	packet_bytes = [packet[idy:idy+2] for idy in range(0,len(packet),2)]

	# Extract read data length (in number of bytes) from current packet
	read_data_nbytes = int("".join(packet_bytes[19:21]), 16)	# bytes 19 and 20 of read response (shouldn't this be n-1. why is it 256?)
	
	# Extract read data from current packet baesd on read data length
	read_data_list.append(packet_bytes[21:21+read_data_nbytes])
	read_data_list_length = len(read_data_list)

# This is the number of axi read responses for each run.
# Should be 341.	
#print read_data_list_length
	
# For now, each telemetry ADC test sequence only performs a single telemetry 
# ADC capture
# Default telemetry ADC measurement plan ADC channel address assignment
# First axi read response.
telem_adc_data = read_data_list[0]
#print telem_adc_data

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

fmt_pot = '{:<20} {:} ADC val {:>20} ohm'
fmt_dac = '{:<20} {:} ADC val {:>20} V'
v_supply = 5
nbit = 12
nlevel = math.pow(2, nbit)
v_per_level = v_supply/nlevel
i_src = 0.001

for telem_adc_data in read_data_list:
	for list_no, channel in enumerate(default_meas_plan):
		# Extract ADC channel measurements from start and end indexes specified 
		# in listing, and append
		channel_name = default_meas_plan[list_no][0]
		start_idx = default_meas_plan[list_no][1]
		end_idx = default_meas_plan[list_no][2] + 1
		meas = convert_hex_to_int(''.join(telem_adc_data[start_idx:end_idx]))	
		meas_avg = meas/16	# Only if average count is factor of 2 and > 16
		v_avg = meas_avg*v_per_level
		# If using scaled.
		if not args.raw:
			# If finding temperature.
			if 'temp' in channel_name or 'resistor' in channel_name:
				temp_avg = v_avg/i_src	# Potentially additional factor of 2 due to missing resistor
				default_meas_plan[list_no].append(temp_avg)
			# If finding vref.
			else:
				default_meas_plan[list_no].append(v_avg)
		# If not using scaled.
		else:
			default_meas_plan[list_no].append(meas)

outfile_filename = args.infile_filename.split('/')[-1].replace('.txt', '_adc_tlm_out.txt')
with open(args.infile_filename.replace('.txt', '_adc_tlm_out.txt'), 'w') as outfile:
	print('\nPrinting telemetry ADC data to file %s.\n' % outfile_filename)
	outfile.write('time, %s\n' % ', '.join(map(str, time_list)))
	for list_no, channel in enumerate(default_meas_plan):
		channel_name = default_meas_plan[list_no][0]
		telem_adc_data_list = default_meas_plan[list_no][3:]	# Indexes 1 and 2 are packet byte indexes
		outfile.write('%s, %s\n' % (channel_name, ', '.join(map(str, telem_adc_data_list))))

# EOF