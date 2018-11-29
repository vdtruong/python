#!/usr/bin/env python

"""
File: parse_rfes_test_txrx_discr_cntrl.py
Project: REASON
Company: Jet Propulsion Laboratory
06-20-2018

Description:
1. Open the response file.
2. Go through each line and break out all
   the bits from the tx and rx responses.
3. Use a *.lvdsdata file as input,
   Enter the script as follow: parse_rfes_test_txrx_disc_cntrl.py some_lvds_data_file.lvdsdata

""" 

import argparse
from conversion_functions import *

# Assign packet data filename as 
# command-line arguments to script
parser = argparse.ArgumentParser(description="Parse RFES Test TXRX Disc Cntrl Reg.")
parser.add_argument("packet_data_filename", help="packet data filename", 
					type=str)
args = parser.parse_args()
		
if __name__ == '__main__':

	# Check for 'scripts' directory
	verify_directory_exists("lvds_results")
	
	# Open the result file for saving.
	rfes_test_txrx_disc_cntrl_parse_file = 'rfes_test_txrx_disc_cntrl_parse.txt'

	# Open packet data
	with open(args.packet_data_filename, "r") as packet_data_infile,\
			open(rfes_test_txrx_disc_cntrl_parse_file, "w") as rfes_test_txrx_disc_cntrl_parse_wr_file:
			
		lines = packet_data_infile.readlines()
		data = []
		
		for index, line in enumerate(lines):
			data.append(line.split(","))
		
		# Deconstruct parameters (columns) or lines (rows) into separate lists
		rcv_time = [data[index][0].strip() for index, value in enumerate(data)]
	##############################################################################
	
	##############################################################################
	
		conc_str_time = "" 	# concatenate string for the time
		conc_str_dat = "" 	# concatenate string for the hex value
	
		for i in range(1, len(rcv_time)):			# go through each line of data
		
			# Parse out the time.
			for j in range(0, 15):
				conc_str_time = conc_str_time + rcv_time[i][j]
		
			# check the time	
			#print(conc_str_time)
		                                                          				
			for j in range(16, 24):   # reconstruct the data char by char to get hex val
				#print(rcv_time[i][j])
				conc_str_dat = conc_str_dat + rcv_time[i][j]
		
			# check the hex data word	
			#print(conc_str_dat) 
			
			# Print time and hex data word.
			rfes_test_txrx_disc_cntrl_parse_wr_file.write("Time %s - %s: \n" %(conc_str_time, conc_str_dat))  
	
			# convert hex value to binary value
			conc_str_bin = convert_hex_to_bin(conc_str_dat, 30)      
			#print(conc_str_bin)
		
			# Break out each bit of the hex data word.  But not including the first
			# 3 msb bits of the word.
			for k in range(3, 30):     
				# k is the bit of the binary word.
				# The index of k tells us whether it is tx or rx data.                        
				#print (index_to_map_bit(k) + "value: " + conc_str_bin[k])                  
				rfes_test_txrx_disc_cntrl_parse_wr_file.write("%s value: %s\n" %(index_to_map_bit(k), conc_str_bin[k]))
		              
			conc_str_time = ""	# clear string
			conc_str_dat = "" 	# clear string