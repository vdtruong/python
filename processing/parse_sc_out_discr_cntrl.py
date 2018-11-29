#!/usr/bin/env python

"""
File: parse_sc_out_discr_cntrl.py
Project: REASON
Company: Jet Propulsion Laboratory
06-15-2018

Description:
1. Open the response file.
2. Go through each line and break out all
   the bits from the output, input and mram registers.

""" 

import argparse                      
from conversion_functions import *                   

# Assign packet data filename as 
# command-line arguments to script
parser = argparse.ArgumentParser(description="Parse SC Out Disc Cntrl Data.")
parser.add_argument("packet_data_filename", help="packet data filename", 
					type=str)
args = parser.parse_args()                                  
		
if __name__ == '__main__':           

	# Check for 'scripts' directory
	verify_directory_exists("sc_results")                                                 
	
	# Open the result file for saving.
	sc_disc_resp_parse_file = 'sc_disc_resp_parse.txt'

	# Open packet data
	with open(args.packet_data_filename, "r") as packet_data_infile,\
			open(sc_disc_resp_parse_file, "w") as sc_disc_resp_parse_wr_file:
			
		lines = packet_data_infile.readlines()
		data = []
		
		for index, line in enumerate(lines):
			data.append(line.split(","))
		
		# Deconstruct parameters (columns) or lines (rows) into separate lists
		rcv_time = [data[index][0].strip() for index, value in enumerate(data)]
		msg_type = [data[index][1].strip() for index, value in enumerate(data)]
		packet = [data[index][2].strip() for index, value in enumerate(data)]
		
		#print(rcv_time)
		#print(msg_type)
		#print(packet)
		data_len = len(rcv_time)
		#print(data_len)         
	
		for i in range(0, data_len):
			# Search for the msg_type of each line.
			# If it is an AXI Read Resp then parse out
			# the data accordingly.
			#print(i)
			if msg_type[i] == 'AXI Read Response':
				#print(msg_type[i])
				#print(packet[i])   
				#print(packet[i][30:38])  	# register address
				#print(packet[i][48:50]) 	# relevant data
				if packet[i][30:38] == '10003008':        
					#print(bin(int("a", 16))[2:])
					#print(bin(int('77', 16))[2:].zfill(8))
					print(packet[i])                            
					print(packet[i][48:50]) 	# relevant data
					#print(bin(int(packet[i][48:50], 16))[2:])              
					print(bin(int(packet[i][48:50], 16))[2:].zfill(8))
					byte_val = bin(int(packet[i][48:50], 16))[2:].zfill(8)
					#byte_val = (bin(int(packet[i][48:50], 16))[2:])   
					sc_disc_resp_parse_wr_file.write("Time %s: SC Out Disc Cntrl (0x1000_3008), value: %s\n" %(rcv_time[i], packet[i][48:50]))                 
					sc_disc_resp_parse_wr_file.write("Bit 7: SC Intf A Out Disc 3: Drv Out  %s\n" %(byte_val[0]))                   
					sc_disc_resp_parse_wr_file.write("Bit 6: SC Intf A Out Disc 2: Drv Out  %s\n" %(byte_val[1]))                 
					sc_disc_resp_parse_wr_file.write("Bit 5: SC Intf A Out Disc 1: Drv Out  %s\n" %(byte_val[2]))                 
					sc_disc_resp_parse_wr_file.write("Bit 4: SC Intf A Out Disc 0: Drv Out  %s\n" %(byte_val[3]))                 
					sc_disc_resp_parse_wr_file.write("Bit 3: SC Intf B Out Disc 3: Drv Out  %s\n" %(byte_val[4]))                 
					sc_disc_resp_parse_wr_file.write("Bit 2: SC Intf B Out Disc 2: Drv Out  %s\n" %(byte_val[5]))                 
					sc_disc_resp_parse_wr_file.write("Bit 1: SC Intf B Out Disc 1: Drv Out  %s\n" %(byte_val[6]))                 
					sc_disc_resp_parse_wr_file.write("Bit 0: SC Intf B Out Disc 0: Drv Out  %s\n" %(byte_val[7]))
				if packet[i][30:38] == '1000a004':        
					#print(bin(int("a", 16))[2:])
					#print(bin(int('77', 16))[2:].zfill(8))
					print(packet[i])                            
					print(packet[i][48:50]) 	# relevant data
					#print(bin(int(packet[i][48:50], 16))[2:])              
					print(bin(int(packet[i][48:50], 16))[2:].zfill(8))
					byte_val = bin(int(packet[i][48:50], 16))[2:].zfill(8)
					#byte_val = (bin(int(packet[i][48:50], 16))[2:])   
					sc_disc_resp_parse_wr_file.write("Time %s: SC Input Disc Status (0x1000_A004), value: %s\n" %(rcv_time[i], packet[i][48:50]))                 
					sc_disc_resp_parse_wr_file.write("Bit 7: Reserved:                 %s\n" %(byte_val[0]))                   
					sc_disc_resp_parse_wr_file.write("Bit 6: SC Intf A In Disc 2 Stat:  %s\n" %(byte_val[1]))                 
					sc_disc_resp_parse_wr_file.write("Bit 5: SC Intf A In Disc 1 Stat:  %s\n" %(byte_val[2]))                 
					sc_disc_resp_parse_wr_file.write("Bit 4: SC Intf A In Disc 0 Stat:  %s\n" %(byte_val[3]))                 
					sc_disc_resp_parse_wr_file.write("Bit 3: Reserved:                 %s\n" %(byte_val[4]))                 
					sc_disc_resp_parse_wr_file.write("Bit 2: SC Intf B In Disc 2 Stat:  %s\n" %(byte_val[5]))                 
					sc_disc_resp_parse_wr_file.write("Bit 1: SC Intf B In Disc 1 Stat:  %s\n" %(byte_val[6]))                 
					sc_disc_resp_parse_wr_file.write("Bit 0: SC Intf B In Disc 0 Stat:  %s\n" %(byte_val[7]))         
				if packet[i][30:38] == '1000b010':        
					#print(bin(int("a", 16))[2:])
					#print(bin(int('77', 16))[2:].zfill(8))
					print(packet[i])                            
					print(packet[i][48:50]) 	# relevant data
					#print(bin(int(packet[i][48:50], 16))[2:])              
					print(bin(int(packet[i][48:50], 16))[2:].zfill(8))
					byte_val = bin(int(packet[i][48:50], 16))[2:].zfill(8)
					#byte_val = (bin(int(packet[i][48:50], 16))[2:])   
					sc_disc_resp_parse_wr_file.write("Time %s: MRAM Disc Status (0x1000_B010), value: %s\n" %(rcv_time[i], packet[i][48:50]))                
					sc_disc_resp_parse_wr_file.write("Bit 4: MRAM 0 Write Enable Stat:  %s\n" %(byte_val[3]))                 
					sc_disc_resp_parse_wr_file.write("Bit 3: MRAM 1 Write Enable Stat:  %s\n" %(byte_val[4]))                 
					sc_disc_resp_parse_wr_file.write("Bit 2: SC A MRAM Select Stat:     %s\n" %(byte_val[5]))                 
					sc_disc_resp_parse_wr_file.write("Bit 1: SC B MRAM Select Stat:     %s\n" %(byte_val[6]))                 
					sc_disc_resp_parse_wr_file.write("Bit 0: MRAM Select Discrete Stat: %s\n" %(byte_val[7]))