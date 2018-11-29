#!/usr/bin/env python

'''
Filename: convert_vasa_data_to_packet_data.py
Project: REASON
Company: Jet Propulsion Laboratory

Description:
Reads and parses VASA SpaceWire metadata to extract packet data from binary 
VASA SpaceWire data. Generates .txt file containing delimited 
metadata and packet data to same directory where VASA metadata and data are 
located.

Args:
	VASA spwmetadata/spwdata base filename

Usage:
	./parse_vasa_data_to_packet.py <spwmetadata/spwdata base filename>

Notes:
'''

from conversion_functions import *

if __name__ == '__main__':

	# Assign SpW base filename as command-line argument to script; assumes 
	# metadata and data share the same base filename
	parser = argparse.ArgumentParser(
				description="Parse SpW metadata and data.")
	parser.add_argument("base_filename", help="SpW base filename", 
						type=str)
	args = parser.parse_args()
	metadata_filename = args.base_filename + ".spwmetadata"
	data_filename = args.base_filename + ".spwdata"

	#### Open SpW metadata ####
	with open(metadata_filename, "r") as metadata_infile:
		lines = metadata_infile.readlines()		# Put all lines (rows) in list
		lines = lines[2:]						# Remove header
		
		#### Commands ####
		# Find all cmd lines by the character string "==> and put" into list
		cmd_line = [line for line in lines if "==>" in line]
		
		# For each cmd line in list, decompose each parameter column into a 
		# separate list
		cmd_exe_time_idx = 1
		cmd_script_idx = 2
		cmd_time_idx = 3
		cmd_type_idx = 4
		cmd_addr_idx = 5
		cmd_byte_len_idx = 6 

		cmd_exe_time = [line.split()[cmd_time_idx] for line in cmd_line]
		cmd_script = [line.split()[cmd_script_idx] for line in cmd_line]
		cmd_time = [line.split()[cmd_time_idx] for line in cmd_line]
		cmd_type = [line.split()[cmd_type_idx] for line in cmd_line]
		cmd_addr = [line.split()[cmd_addr_idx] for line in cmd_line]
		cmd_byte_len = [line.split()[cmd_byte_len_idx] for line in cmd_line]

		# Unused, only for reference
		cmd_time_col = [line.split() for line in cmd_line]
		##################

		#### Responses ####
		# Find all responses and put into list
		res_line = [line for line in lines if "==>" not in line]

		# Since msg type column has a variable string length, parameters 
		# cannot be extracted from a fixed column number index across all msg 
		# types; need to first identify the message type , then infer column 
		# numbers of relevant parameters.

		res_rcv_time = []
		res_msg_type = []
		res_service_type = []
		res_crc_stat = []
		res_crc_rcv = []
		res_crc_calc = []
		res_msg_byte_len = []
		res_msg_byte_start_no = []	# All byte start numbers need to be offset by the first element
		
		msg_types = ["Msg Success (ACK)", "Msg Failure (NACK)", "AXI Read Response", "AXI Read", "AXI Write", "Unknown Msg"]

		# Find all responses with known message types and put into list
		res_line_valid = [line for line in res_line if any(type in line for type in msg_types)]

		# Find all responses that don't have a known message type in msg_types (if Alan updated formatting without changes being incorporated)
		res_line_invalid = [line for line in res_line if not any(type in line for type in msg_types)]
		
		for line in res_line_valid:
			# Uknown msg is the only response that has different column number 
			# indexes for parameters
			res_rcv_time_idx = 0
			res_msg_type_idx = [1, 2, 3]
			res_service_type_idx = 4
			res_crc_stat_idx = 6
			res_crc_rcv_idx = 7
			res_crc_calc_idx = 8
			res_msg_byte_len_idx = 9
			res_msg_byte_start_no_idx = 10	# All byte start numbers need to be offset by the first element

			ukn_res_rcv_time_idx = 0
			ukn_res_msg_type_idx = [1, 2]
			ukn_res_service_type_idx = 3
			ukn_res_crc_stat_idx = 5
			ukn_res_crc_rcv_idx = 6
			ukn_res_crc_calc_idx = 7
			ukn_res_msg_byte_len_idx = 8
			ukn_res_msg_byte_start_no_idx = 9	# All byte start numbers need to be offset by the first element

			# Use one set of column number indexes for ACK, NACK and AXI RRs
			if any(type in line for type in msg_types[0:3]):
				line_col = line.split()
				res_rcv_time.append(line_col[res_rcv_time_idx])
				res_msg_type.append(" ".join(line_col[1:4]))	# This is manually done since don't know how to keep index ranges in variables
				res_service_type.append(line_col[res_service_type_idx])
				res_crc_stat.append(line_col[res_crc_stat_idx])
				res_crc_rcv.append(line_col[res_crc_rcv_idx])
				res_crc_calc.append(line_col[res_crc_calc_idx])
				res_msg_byte_len.append(int(line_col[res_msg_byte_len_idx]))
				res_msg_byte_start_no.append(int(line_col[res_msg_byte_start_no_idx]))
			# Use another set of column number indexes for Uknown Msg
			else:
				line_col = line.split()
				res_rcv_time.append(line_col[ukn_res_rcv_time_idx])
				res_msg_type.append(" ".join(line_col[1:3]))	# This is manually done since don't know how to keep index ranges in variables
				res_service_type.append(line_col[ukn_res_service_type_idx])
				res_crc_stat.append(line_col[ukn_res_crc_stat_idx])
				res_crc_rcv.append(line_col[ukn_res_crc_rcv_idx])
				res_crc_calc.append(line_col[res_crc_calc_idx])
				res_msg_byte_len.append(int(line_col[ukn_res_msg_byte_len_idx]))
				res_msg_byte_start_no.append(int(line_col[ukn_res_msg_byte_start_no_idx]))

		# Perform offset on the byte start number
		byte_start_no_offset = res_msg_byte_start_no[0]
		res_msg_byte_start_no = [(num - byte_start_no_offset) for num in res_msg_byte_start_no]
		###################

	###########################

	#### Open SpW data ####
	with open(data_filename, "rb") as data_infile:
		bin_data = data_infile.read()			# length is in number of bytes
		packet_data = [get_byte_seq_from_bin(bin_data, res_msg_byte_len[idx], res_msg_byte_start_no[idx]) for idx in range(len(res_line_valid))]
	#######################

	#### Print packet data to file ####
	outfile_filename = args.base_filename.split('/')[-1] + "_packet.txt"	# If input file contains a path, remove the path

	with open(args.base_filename + "_packet.txt", "w") as data_outfile:
		print("\nPrinting packet data to file %s.\n" % outfile_filename)
		for index in range(len(packet_data)):
			data_outfile.write("%s, %s, %s\n" % (res_rcv_time[index], res_msg_type[index], packet_data[index]))
	###################################

# EOF