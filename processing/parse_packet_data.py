#!/usr/bin/env python

"""
File: parse_packet_data.py
Project: REASON
Company: Jet Propulsion Laboratory

Description:
Reads delimited metadata and packet data generated from convert_vasa_data_to_packet_data.py, 
and performs the following:
	- For ACK and NACK packet types, write ACKs and NACK packets each to 
	separate .txt files, and deconstructs the packets into fields according 
	to the REASON DES AXI Address Map and Registers. The .txt files are titled 
	after the base name of the original packet data.
	- For AXI Read Response packet types, identifies the AXI register from 
	the read response starting address, and writes the metadata and packet 
	data to separate .txt files according to the AXI register type. The .txt 
	files are titled after the base name of the original packet data.
	- All generated files are .txt and d
Args:
	1. packet data (generated from convert_vasa_data_to_packet_data.py)
	2. There are four flavors to the outputs of the AXI Response.
	  -o 	One file without breakout of the register bits
	  -op One file with breakout of the register bits
		-p  Multiple files for multiple registers with breakout
		 		of the register bits
		 		No argument means multiple files for multiple registers but no breakout

Usage:
	./parse_packet_data.py <packet data filename>_packet.txt

Notes:
Packet data can be located outside the local directory where the script is 
located. The generated files are saved in the same directory as the original 
packet data file.
"""

import argparse                   
import ext_mod	# This is for the map register break out dictionary.
from conversion_functions import *

# Main 
if __name__ == '__main__':

	# Assign packet data filename (generated from parse_vasa_data.py) as 
	# command-line arguments to script
	parser = argparse.ArgumentParser(description="Parse packet data.")
	parser.add_argument("-o", "--OneFile", help="Enter -o for one file containg all registers.",
										action="store_true")                                                   
	parser.add_argument("-op", "--OneFileParse", help="Enter -op for one file containg all registers with parsing.",
										action="store_true")
	parser.add_argument("-p", "--ParRegBit", help="Enter -p for register parsing.",
										action="store_true")
	parser.add_argument("packet_data_filename", help="packet data filename", 
						type=str)
	args = parser.parse_args()

	# Open packet data
	with open(args.packet_data_filename, "r") as packet_data_infile:
		lines = packet_data_infile.readlines()
		data = []
		for index, line in enumerate(lines):
			data.append(line.split(","))
		# Deconstruct parameters (columns) or lines (rows) into separate lists
		rcv_time = [data[index][0].strip() for index, value in enumerate(data)]
		msg_type = [data[index][1].strip() for index, value in enumerate(data)]
		packet = [data[index][2].strip() for index, value in enumerate(data)]
		#print(index)
		#print(rcv_time)
		#print(len(rcv_time))
		
	# Create separate lists for ACK/NACK/AXI read response metadata and fields
	ack_rcv_time = []
	ack_ccsds_ver = []
	ack_packet_type = []
	ack_data_header_flag = []
	ack_apid = []
	ack_seq_flag = []
	ack_seq_count = []
	ack_packet_len = []
	ack_secondary_header_flag = []
	ack_pus_version_no = []
	ack_header_spare = []
	ack_service_type = []
	ack_service_subtype = []
	ack_time = []
	ack_packet_error_ctrl = []

	nack_rcv_time = []
	nack_ccsds_ver = []
	nack_packet_type = []
	nack_data_header_flag = []
	nack_apid = []
	nack_seq_flag = []
	nack_seq_count = []
	nack_packet_len = []
	nack_secondary_header_flag = []
	nack_pus_version_no = []
	nack_header_spare = []
	nack_service_type = []
	nack_service_subtype = []
	nack_time = []
	nack_busy_status = []
	nack_reason_code = []
	nack_error_flag = []
	nack_spare = []
	nack_packet_error_ctrl = []

	rres_rcv_time = []
	rres_reg_type = []
	rres_reg_type_hex = []	# contains the hex addresses
	rres_ccsds_ver = []
	rres_packet_type = []
	rres_data_header_flag = []
	rres_apid = []
	rres_seq_flag = []
	rres_seq_count = []
	rres_packet_len = []
	rres_secondary_header_flag = []
	rres_pus_version_no = []
	rres_header_spare = []
	rres_service_type = []
	rres_service_subtype = []
	rres_time = []
	rres_read_start_addr = []
	rres_read_start_addr_hex = []
	rres_axi_read_len = []      
	rres_axi_read_len_hex = []	# leaves as hex
	rres_axi_read_data = []
	rres_spare = []
	rres_packet_error_ctrl = []

	axi_read_index = []	# Index array of where axi read occurs.
  		 
	i = 0 # axi_read_index array index                                              
	                                                                                             	
	for index, value in enumerate(msg_type):
		#print(index)
		if value == "ACK":
			# Deconstruct fields for ACK packet type                                          
			# But for valid registers only.       
			# Search the axi_reg_map array for valid registers.
			# Have not checked this for loop for ACK.
			for axi_reg_map_indx in range(0, len(ext_mod.axi_reg_map)):
				if packet[index][30:38] == ext_mod.axi_reg_map[axi_reg_map_indx][0]: 
					ack_rcv_time.append(rcv_time[index])
					ack_ccsds_ver.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[0:3])
					ack_packet_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[3])
					ack_data_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[4])
					ack_apid.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[5:16])
					ack_seq_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[16:18])
					ack_seq_count.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[18:32])
					ack_packet_len.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[32:48])
					ack_secondary_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[48])
					ack_pus_version_no.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[49:52])
					ack_header_spare.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[52:56])
					ack_service_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[56:64])
					ack_service_subtype.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[64:72])
					ack_time.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[72:120])
					ack_packet_error_ctrl.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[120:136])
		elif value == "NACK":
			# Deconstruct fields for NACK packet type                                                        
			# But for valid registers only.                                  
			# Search the axi_reg_map array for valid registers.
			# Have not checked this for loop for NACK.
			for axi_reg_map_indx in range(0, len(ext_mod.axi_reg_map)):
				if packet[index][30:38] == ext_mod.axi_reg_map[axi_reg_map_indx][0]: 
					nack_rcv_time.append(rcv_time[index])
					nack_ccsds_ver.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[0:3])
					nack_packet_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[3])
					nack_data_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[4])
					nack_apid.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[5:16])
					nack_seq_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[16:18])
					nack_seq_count.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[18:32])
					nack_packet_len.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[32:48])
					nack_secondary_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[48])
					nack_pus_version_no.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[49:52])
					nack_header_spare.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[52:56])
					nack_service_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[56:64])
					nack_service_subtype.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[64:72])
					nack_time.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[72:120])
					nack_busy_status.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[120:128])
					nack_reason_code.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[128:136])
					nack_error_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[136:144])
					nack_spare.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[144:152])
					nack_packet_error_ctrl.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[152:168])
		elif value == "AXI Read Response":              
			#print(index)       
			#print(packet[index][30:38])
			axi_read_index.append(index)
			#print(index)
			#print(axi_read_index)
			# Deconstruct fields for AXI Read Response packet type.                                          
			# But for valid registers only.
			# Search the axi_reg_map array for valid registers.
			for axi_reg_map_indx in range(0, len(ext_mod.axi_reg_map)):
				if packet[index][30:38] == ext_mod.axi_reg_map[axi_reg_map_indx][0]: 
					rres_rcv_time.append(rcv_time[index])
					rres_ccsds_ver.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[0:3])
					rres_packet_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[3])
					rres_data_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[4])
					rres_apid.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[5:16])
					rres_seq_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[16:18])
					rres_seq_count.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[18:32])
					rres_packet_len.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[32:48])
					rres_secondary_header_flag.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[48])
					rres_pus_version_no.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[49:52])
					rres_header_spare.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[52:56])
					rres_service_type.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[56:64])
					rres_service_subtype.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[64:72])
					rres_time.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[72:120])
					rres_read_start_addr.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[120:152])
					rres_axi_read_len.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[152:168])   
					rres_axi_read_len_hex.append(packet[index][38:42]) # leaves as hex
					tmp = (int(rres_axi_read_len[-1], 2) + 1)*8                                                    
					#rres_axi_read_data.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[168:168+tmp])
					# Leave read data as hex.
					rres_axi_read_data.append(packet[index])
					rres_spare.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[168+tmp:168+tmp+16])
					rres_packet_error_ctrl.append(convert_hex_to_bin(packet[index], len(packet[index]*4))[168+tmp+16:168+tmp+16+16])
					# Need this to write data to file.
					rres_reg_type.append(ext_mod.axi_reg_map[axi_reg_map_indx][1])                             
					rres_reg_type_hex.append(ext_mod.axi_reg_map[axi_reg_map_indx][0])                        
					#print("Register %s Found in Register Map" % (packet[index][30:38]))
				#else:
				#	print("Register %s not Found in Register Map" % (packet[index][30:38]))
	    	
			"""
			# Identify AXI register based on read start address from axi_reg_map definition.
			# Search through the axi_map_reg list and build up the registers received array.
			for index in range(len(axi_reg_map)):
				# Search a section of the axi_reg_map until we find the corresponding
				# register we are looking for.
				#print(index)
				start_addr = convert_hex_to_int(axi_reg_map[index][0])
				start_addr_hex = (axi_reg_map[index][0])
				#print(start_addr_hex)                                  # length of data
				end_addr = convert_hex_to_int(axi_reg_map[index][0]) + axi_reg_map[index][2]
				end_addr_hex = convert_int_to_hex(end_addr, 8)
				#print(end_addr_hex)
				addr_srch_for =  convert_bin_to_hex(rres_read_start_addr[-1],8)
				#print(addr_srch_for)
				#print(convert_bin_to_hex(rres_read_start_addr[-1],8))
				if start_addr <= int(rres_read_start_addr[-1], 2) < end_addr:
					# If address is part of the axi_reg_map, append to the list.          
					rres_reg_type_hex.append(axi_reg_map[index][0])
					#print(rres_reg_type_hex)
					rres_reg_type.append(axi_reg_map[index][1])    
					#print(rres_reg_type)
					break
				else:
					# If at the end of the axi_map_reg array.
					# Mark as not found.
					if index == 74:
						print("Register %s not Found in Register Map" % (addr_srch_for))
			"""	
			
	#print(rres_read_start_addr_hex)		
	#print(rres_reg_type_hex)
	#print(len(rres_reg_type_hex))
	#print(rres_reg_type)         
	#print(len(rres_reg_type))
	
	# Find directory structure (to save files) and base filename for output files
	directory_hierarchy = args.packet_data_filename.split("/")
	base_name = directory_hierarchy[-1].replace("_packet.txt", "")

	# Change directory to location of packet data (relative path from where script
	# is executed)
	if len(directory_hierarchy) > 1:
		directory_destination = "".join(directory_hierarchy[index] for index in range(0, len(directory_hierarchy)-1))
		os.chdir(directory_destination)

	ack_filename = base_name + "_ack_data.txt"
	nack_filename = base_name + "_nack_data.txt"

	# Print deconstructed ACK packets to separate file
	with open(ack_filename, "w") as outfile:
		# Header to identify columns
		outfile.write("rcv_time, ccsds_ver, packet_type, data_header_flag, " \
						+ "apid, seq_flag, seq_count, packet_len, " 
						+ "secondary_header_flag, pus_ver_no, header_spare, " \
						+ "service_type, service_subtype, time, " \
						+ "packet_error_ctrl\n")
		for index in range(len(ack_rcv_time)):
			outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
							ack_rcv_time[index], 
							ack_ccsds_ver[index],
							ack_packet_type[index],
							ack_data_header_flag[index],
							ack_apid[index],
							ack_seq_flag[index],
							ack_seq_count[index],
							ack_packet_len[index],
							ack_secondary_header_flag[index],
							ack_pus_version_no[index],
							ack_header_spare[index],
							ack_service_type[index],
							ack_service_subtype[index],
							ack_time[index],
							ack_packet_error_ctrl[index]))
  	#print(ack_rcv_time)
	
	# Print deconstructed NACK packets to separate file
	with open(nack_filename, "w") as outfile:
		# Header to identify columns
		outfile.write("rcv_time, ccsds_ver, packet_type, data_header_flag, " \
						+ "apid, seq_flag, seq_count, packet_len, " 
						+ "secondary_header_flag, pus_ver_no, header_spare, " \
						+ "service_type, service_subtype, time, busy_status, " \
						+ "reason_code, error_flag, spare, packet_error_ctrl\n")
		for index in range(len(nack_rcv_time)):
			outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
							nack_rcv_time[index], 
							nack_ccsds_ver[index],
							nack_packet_type[index],
							nack_data_header_flag[index],
							nack_apid[index],
							nack_seq_flag[index],
							nack_seq_count[index],
							nack_packet_len[index],
							nack_secondary_header_flag[index],
							nack_pus_version_no[index],
							nack_header_spare[index],
							nack_service_type[index],
							nack_service_subtype[index],
							nack_time[index],
							nack_busy_status[index],
							nack_reason_code[index],
							nack_error_flag[index],
							nack_spare[index],
							nack_packet_error_ctrl[index]))
	 	#print(nack_rcv_time)
	
	# Check to see if one file is used for all registers without parsing. 	                                                                          
	if args.OneFile:                                                                          
		with open(base_name  + "_data.txt", "w") as outfile:            
			for i in range(0, len(rres_reg_type)):
				#print(rres_reg_type[i])                                    
				#print(rres_reg_type_hex[i])                                                        
				#print(rres_axi_read_data[i][30:38])
				# Check to see if address of this data line is part of the register map.
				# If not, do not save the data.
				#if rres_reg_type_hex[i] == rres_axi_read_data[i][30:38]:  
				outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
									rres_rcv_time[i], 
									rres_ccsds_ver[i],
									rres_packet_type[i],
									rres_data_header_flag[i],
									rres_apid[i],
									rres_seq_flag[i],
									rres_seq_count[i],
									rres_packet_len[i],
									rres_secondary_header_flag[i],
									rres_pus_version_no[i],
									rres_header_spare[i],
									rres_service_type[i],
									rres_service_subtype[i],
									rres_time[i],
									rres_read_start_addr[i],
									rres_axi_read_len[i],
									rres_axi_read_data[i],
									rres_spare[i],
									rres_packet_error_ctrl[i]))
	
	# Check to see if one file is used for all registers with parsing. 	                                                                          
	elif args.OneFileParse:                                                                   
		with open(base_name  + "_parse_data.txt", "w") as outfile:            
			for i in range(0, len(rres_reg_type)):
				#print(rres_reg_type[i])                                    
				#print(rres_reg_type_hex[i])                                                        
				#print(rres_axi_read_data[i][30:38])
				axi_addr_val = rres_axi_read_data[i][42:50]      
				#print(rres_axi_read_len)
				#print(axi_addr_val)
				axi_addr_val_bin = convert_hex_to_bin(axi_addr_val, 32)
				#print(axi_addr_val_bin)
				# Extract the 32 bits status data.
						                                  
				# If parse reg. bit is requested, break out all 32 bits of the data.            
				outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
									rres_rcv_time[i], 
									rres_ccsds_ver[i],
									rres_packet_type[i],
									rres_data_header_flag[i],
									rres_apid[i],
									rres_seq_flag[i],
									rres_seq_count[i],
									rres_packet_len[i],
									rres_secondary_header_flag[i],
									rres_pus_version_no[i],
									rres_header_spare[i],
									rres_service_type[i],
									rres_service_subtype[i],
									rres_time[i],
									rres_read_start_addr[i],
									rres_axi_read_len[i],
									rres_axi_read_data[i],
									rres_spare[i],
									rres_packet_error_ctrl[i]))
				# But only break out the bits if the data length is 4 bytes.
				if rres_axi_read_len_hex[i] == '0004':          
					for j in range(0, 32):		
						outfile.write(ext_mod.map_reg[rres_reg_type_hex[i]][j] + axi_addr_val_bin[j] + '\n')
	
	# If parse reg. bit is requested, break out all 32 bits of the data.
	# Each register will have its own file.
	elif args.ParRegBit:            	
		# Print deconstructed AXI Read Response packets to separate file according to 
		# read register address.
		# Identify all unique AXI register types as a starting point for the total 
		# number of output files.
		#print(rres_reg_type)      
		#print(rres_reg_type_hex)
		#print(axi_read_index)
		#print(rres_rcv_time)
		#print(rres_axi_read_data)
		#print(len(rres_rcv_time))
		unique_rres_reg_type = list(set(rres_reg_type))
		unique_rres_reg_type_hex = list(set(rres_reg_type_hex))
		#print(unique_rres_reg_type)                             
		#print(unique_rres_reg_type_hex)
		# Create files for current_unique_rres_reg_type.
		for current_unique_rres_reg_type in unique_rres_reg_type:
			#print(current_unique_rres_reg_type)
			with open(base_name + "_" + current_unique_rres_reg_type + "_parse_data.txt", "w") as outfile:
				#for index, current_rres_reg_type in enumerate(rres_reg_type):
				for i in range(0, len(rres_reg_type)):
					#print(i)
					# If rres_reg_type matches the file register name,
					# save the data for that entire data line.
					if rres_reg_type[i] == current_unique_rres_reg_type: 
						#print(i)
						#print(rres_reg_type[i])                        
						#print(rres_reg_type_hex[i]) 
						#axi_rd_len = rres_axi_read_data[i][38:42]
						axi_addr_val = rres_axi_read_data[i][42:50]      
						#print(rres_axi_read_len)
						#print(axi_addr_val)
						#print(convert_hex_to_bin(axi_addr_val, 32))
						axi_addr_val_bin = convert_hex_to_bin(axi_addr_val, 32)
						#print(axi_addr_val_bin)
						# Extract the 32 bits status data.
						                                  
						# If parse reg. bit is requested, break out all 32 bits of the data.            
						outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
									rres_rcv_time[i], 
									rres_ccsds_ver[i],
									rres_packet_type[i],
									rres_data_header_flag[i],
									rres_apid[i],
									rres_seq_flag[i],
									rres_seq_count[i],
									rres_packet_len[i],
									rres_secondary_header_flag[i],
									rres_pus_version_no[i],
									rres_header_spare[i],
									rres_service_type[i],
									rres_service_subtype[i],
									rres_time[i],
									rres_read_start_addr[i],
									rres_axi_read_len[i],
									rres_axi_read_data[i],
									rres_spare[i],
									rres_packet_error_ctrl[i]))
						# But only break out the bits if the data length is 4 bytes.
						if rres_axi_read_len_hex[i] == '0004':          
							for j in range(0, 32):		
								outfile.write(ext_mod.map_reg[rres_reg_type_hex[i]][j] + axi_addr_val_bin[j] + '\n')
					
	# For multiple files without parsing.
	else:            
		unique_rres_reg_type = list(set(rres_reg_type))
		unique_rres_reg_type_hex = list(set(rres_reg_type_hex))
		#print(unique_rres_reg_type)                             
		#print(unique_rres_reg_type_hex)
		# Create files for current_unique_rres_reg_type.
		for current_unique_rres_reg_type in unique_rres_reg_type:
			#print(current_unique_rres_reg_type)
			with open(base_name + "_" + current_unique_rres_reg_type + "_data.txt", "w") as outfile:
				#for index, current_rres_reg_type in enumerate(rres_reg_type):
				for i in range(0, len(rres_reg_type)):
					#print(i)
					# If rres_reg_type matches the file register name,
					# save the data for that entire data line.
					if rres_reg_type[i] == current_unique_rres_reg_type:
						                                  
						# If parse reg. bit is requested, break out all 32 bits of the data.            
						outfile.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
									rres_rcv_time[i], 
									rres_ccsds_ver[i],
									rres_packet_type[i],
									rres_data_header_flag[i],
									rres_apid[i],
									rres_seq_flag[i],
									rres_seq_count[i],
									rres_packet_len[i],
									rres_secondary_header_flag[i],
									rres_pus_version_no[i],
									rres_header_spare[i],
									rres_service_type[i],
									rres_service_subtype[i],
									rres_time[i],
									rres_read_start_addr[i],
									rres_axi_read_len[i],
									rres_axi_read_data[i],
									rres_spare[i],
									rres_packet_error_ctrl[i]))

# EOF