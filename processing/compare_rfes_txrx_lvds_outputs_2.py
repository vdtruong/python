#!/usr/bin/env python

"""
File: compare_rfes_txrx_lvds_outputs_2.py
Project: REASON
Company: Jet Propulsion Laboratory
05-25-2018

Description:
1. Open the txrx command words file, the lvds output file, the matching list
file and the saved compare result file.
2. Go through the command words file one at a time, look for a match in the
matching list file. 
3. Use the matching index and remember the corresponding lvds repsonse from the
matching list file.
4. Go through the lvds output file and compare to the lvds response from 3.
5. If they match, print "pass" and save the result.  If not, print "fail" and 
save the result.
6. Do this for the entire txrx command words file.  When done, print and save
"Pass" if all words match, else print and save "Fail".

"""

from conversion_functions import *

if __name__ == '__main__':

	# Check for 'scripts' directory
	verify_directory_exists("lvds_results")
                                                       
	# Open the rx and tx command words file.
	cmd_wrds_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_cmd/scripts/rfes_txrx_cmd_wrds.txt'    
	# Open the lvds outputs file.
	lvds_outputs_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_processing/log/20180523/res_rfes_txrx_output_cycle_test_20180523_7.lvdsdata'
	# Open the matching list file.
	cmd_match_list_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_cmd/scripts/rfes_txrx_cmd_wrds_match_list.txt'               
	# Open the result file for saving.
	lvds_results_file = 'rfes_txrx_results.txt'
	
	with open(cmd_wrds_file, "r") as cmd_wrds_in_file,\
				open(lvds_outputs_file, "r") as lvds_outputs_in_file,\
				open(cmd_match_list_file, "r") as cmd_match_list_in_file,\
				open(lvds_results_file, "w") as lvds_results_file_out_file:    
				
		# Open the cmd_match_list_file file.
		d = cmd_match_list_in_file.readlines()
		# 2d array of file.
		cmd_match_list = [x.split(",") for x in d]
		cmd_match_list_len = len(cmd_match_list)
		
		#print(cmd_match_list[0][0])	# [row][cmd col]
		#print(cmd_match_list[0][1])	# [row][lvds col]
		
		# Open the lvds_outputs_file file.
		e = lvds_outputs_in_file.readlines()
		# 2d array of file.
		lvds_outputs_list = [y.split(" ") for y in e]
		lvds_outputs_list_len = len(lvds_outputs_list)
		
		#print(lvds_outputs_list[1][1])		# [row][time col]     
		#print(lvds_outputs_list[1][3])  	# [row][lvds col]
		
		pass_cnt_crit = 29
		pass_cnt = 0
				
		# Read the first line of the sent command word file.
		cmd_wrd_in_line = cmd_wrds_in_file.readline()
		#print(cmd_wrd_in_line)
		
		# If the file is not empty keep reading line one at a time
		# until the file is empty.
		while cmd_wrd_in_line:
						
			# Look up cmd_wrd_in_line in the matching list.
			for i in range(cmd_match_list_len):
				# Need to strip off the space at the end.
				if cmd_wrd_in_line.rstrip() == cmd_match_list[i][0]:
					#print('found matching lvds_resp')   
					# Need to convert to int for comparision to work.                                        
					# Check to see if lvds resp from matching list and lvds output match.
					if int(cmd_match_list[i][1],32) == int(lvds_outputs_list[i+1][3],32):
						print("%d. Pass" %i)
						lvds_results_file_out_file.write("%d. Pass\n" %i)
						pass_cnt = pass_cnt +1
					else:                                                      
						print("%d. Fail" %i)
						lvds_results_file_out_file.write("%d. Fail\n" %i)
								
			# Move to next line of the input file.   
			cmd_wrd_in_line = cmd_wrds_in_file.readline() 
						
		# Check if all lvds responses are correct.
		if pass_cnt >= pass_cnt_crit:
			lvds_results_file_out_file.write("Test Pass")
		else: 
			lvds_results_file_out_file.write("Test Fail")