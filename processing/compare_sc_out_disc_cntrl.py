#!/usr/bin/env python

"""
File: compare_sc_out_disc_cntrl.py
Project: REASON
Company: Jet Propulsion Laboratory
06-07-2018

Description:
1. Open the output command words file, the response file, the LUT
file and the saved compare result file.
2. Go through the command words file one at a time, look for a match in the
LUT file. 
3. Use the matching index and remember the corresponding expected repsonse from 
the LUT file.
4. Go through the response file and compare to the expected response from 3.
5. If they match, print "pass" and save the result.  If not, print "fail" and 
save the result.
6. Do this for the entire command words file.  When done, print and save
"Pass" if all words match, else print and save "Fail".

""" 
import argparse                      
from conversion_functions import *
                                         
		
parser = argparse.ArgumentParser()
parser.add_argument("-A", "--Aconn", help="Enter -A for spacecraft connector A. Else, connector B.",
										action="store_true")
args = parser.parse_args()
	
if __name__ == '__main__':

	# Check for 'scripts' directory
	verify_directory_exists("sc_results")       
                                                       
	# Open the command words file.                                                                                     
	cmd_wrds_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_cmd/scripts/sc_out_cmd_wrds.txt'  
	#cmd_wrds_file = 'C:/EGSE_Instrument_Control/vasa_cmd/scripts/sc_out_cmd_wrds.txt'    
	
	# Open the response file.                  
	if args.Aconn:          
		# For connector A.                                                                                                                                                             
		resp_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_processing/log/2018-06-04/res_spacecraft_output_discr_cntrl_cycl_test_con_A_20180604_5_packet.txt'
		#resp_file = 'C:/EGSE_Instrument_Control/vasa_processing/log/2018-06-04/res_spacecraft_output_discr_cntrl_cycl_test_con_A_20180604_5_packet.txt'     
		cmd_wrds_strt_indx = 0	# cmd words start index
		resp_row_indx = 3     	# response start index
		LUT_strt_row = 0     		# LUT start index
	else:               
		# For connector B.                                                                                                                                                             
		resp_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_processing/log/2018-06-06/res_spacecraft_output_discr_cntrl_cycl_test_con_B_20180606_3_packet.txt'                                                                                                                                                               
		#resp_file = 'C:/EGSE_Instrument_Control/vasa_processing/log/2018-06-06/res_spacecraft_output_discr_cntrl_cycl_test_con_B_20180606_3_packet.txt'  
		cmd_wrds_strt_indx = 4  # cmd words start index
		resp_row_indx = 15     	# response start index
		LUT_strt_row = 4     		# LUT start index         
	
	# Open the LUT file.                                                                            
	LUT_file = 'C:/Users/vdtruong/Documents/GitHub/EGSE_Instrument_Control/vasa_cmd/scripts/sc_out_in_lut.txt'
	#LUT_file = 'C:/EGSE_Instrument_Control/vasa_cmd/scripts/sc_out_in_lut.txt'                                              
	
	# Open the result file for saving.
	sc_disc_con_A_results_file = 'sc_disc_results_con_A.txt'
	sc_disc_con_B_results_file = 'sc_disc_results_con_B.txt'         
	
	with open(cmd_wrds_file, "r") as cmd_wrds_in_file,\
				open(resp_file, "r") as resp_in_file,\
				open(LUT_file, "r") as LUT_in_file,\
				open(sc_disc_con_A_results_file, "w") as sc_disc_results_con_A_out_file,\
				open(sc_disc_con_B_results_file, "w") as sc_disc_results_con_B_out_file:    
				
		# Open the commands file.
		c = cmd_wrds_in_file.readlines()
		# 2d array of file.
		cmd_wrds_list = [u.split(",") for u in c]
		cmd_wrds_list_len = len(cmd_wrds_list)  
		
		#print(cmd_wrds_list[1][0])	# [row][cmd col]
						
		# Open the LUT file.
		d = LUT_in_file.readlines()
		# 2d array of file.
		LUT_list = [x.split(",") for x in d]
		LUT_list_len = len(LUT_list)
		
		#print(LUT_list[0][0])	# [row][cmd col]
		#print(LUT_list[0][1])	# [row][lvds col]
		
		# Open the response file.
		e = resp_in_file.readlines()
		# 2d array of file.
		resp_list = [y.split(" ") for y in e]
		resp_list_len = len(resp_list)
		resp_col = 4
		resp_row_skip = 3
		#print(resp_list[resp_row_indx][resp_col])				# [row][time col]   
		#print(resp_list[resp_row_indx][resp_col][48:50])	# [row][time col][section]
	
		# Print title of result file.
		if args.Aconn:          
			# For connector A.		                                                    
			sc_disc_results_con_A_out_file.write("Connector A - SC Output Discrete Control Test:\n")
		else:               
			# For connector B.           		                                                    
			sc_disc_results_con_B_out_file.write("Connector B - SC Output Discrete Control Test:\n")   
		
		# If we have four passes, the test passes.
		pass_cnt_crit = 4
		pass_cnt = 0
		
		# Look up the sc output discrete control command in the LUT file.
		for i in range(cmd_wrds_list_len - 5):
			#print(i)
			# Compare the command words from two files.
			# Need to strip off extra characters at the end.
			#print(cmd_wrds_list[i + cmd_wrds_strt_indx][0].strip())
			#print(LUT_list[i][0])
			#print(LUT_list[i + LUT_strt_row][0])
			if cmd_wrds_list[i + cmd_wrds_strt_indx][0].strip() == LUT_list[i + LUT_strt_row][0]:
				#print('found matching sc input discrete status')   
				# Need to convert to int for comparision to work.                                        
				# Check to see if resp from LUT and sc input discrete status match.
				#print(resp_row_indx)        
				#print(LUT_list[i + LUT_strt_row][1].strip())
				#print(int(LUT_list[i + LUT_strt_row][1],8))
				#print(resp_list[resp_row_indx][resp_col][48:50])
				if int(LUT_list[i + LUT_strt_row][1],8) == int(resp_list[resp_row_indx][resp_col][48:50],8):
					#print("%d. Pass" %(i+1))    
					if args.Aconn:          
						# For connector A.		                                                    
						sc_disc_results_con_A_out_file.write("%d. Pass\n" %(i+1))
						pass_cnt = pass_cnt +1
					else:               
						# For connector B.           		                                                    
						sc_disc_results_con_B_out_file.write("%d. Pass\n" %(i+1))
						pass_cnt = pass_cnt +1
				else:                          
					if args.Aconn:          
						# For connector A.		                                                    
						sc_disc_results_con_A_out_file.write("%d. Fail\n" %(i+1))
					else:               
						# For connector B.           		                                                    
						sc_disc_results_con_B_out_file.write("%d. Fail\n" %(i+1))
			
			# Increment response row index.			
			resp_row_indx = resp_row_indx + resp_row_skip
						
		# Check if all responses are correct.
		if pass_cnt >= pass_cnt_crit:
			if args.Aconn:          
				# For connector A.		                                                    
				sc_disc_results_con_A_out_file.write("Test Pass")
			else:               
				# For connector B.           		                                                    
				sc_disc_results_con_B_out_file.write("Test Pass")
		else: 
			if args.Aconn:          
				# For connector A.		                                                    
				sc_disc_results_con_A_out_file.write("Test Fail")
			else:               
				# For connector B.           		                                                    
				sc_disc_results_con_B_out_file.write("Test Fail")