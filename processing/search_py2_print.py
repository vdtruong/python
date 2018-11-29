#!/usr/bin/env python

"""
File: search_py2_print.py
Project: REASON
Company: Jet Propulsion Laboratory
07-26-2018

Description:
This script searches for "print " on Python 2 scripts and insert () to make
it compatible with Python 3.  If the argument is -conv then it will search for
the function convert_bin_to_hex() within a function that calls it.
Please see the flow chart for the the description of the program.
The following description is only for finding the "print " string.
1. Open a file and search for "print ", that's print with a space after.
2. If found, count the number of ( and ) occurances.
3. If they are the same insert ( after print and ) at end of line.
4. If not, insert ( after print and set insert_eol flag.
5. If "print " is not found but insert_eol flag is set, insert ) at eol
   and clear flag.
6. Do this for the rest of the file.
7. When done with file, print all information about lines that were changed.
8. Reopen the same file and replace file with new or old lines.

Enter srch_py2_print.py name_of_file.*

""" 
import argparse                      
from conversion_functions import *                                                                   
		
parser = argparse.ArgumentParser()    
parser.add_argument("infile_filename", help="any filename", 
					type=str) 
parser.add_argument("-conv", "--conv", help="Enter -conv to search for the convert_bin_to_hex() function",
                    action="store_true")     
args = parser.parse_args()
	
	
str1 = "print "				# String to be searched.
str2 = "print(" 				# Replace str1 with str2.
conv_str = "convert_bin"	# Find convert_bin_to_hex() function
len_str = "len("				# Is the string len( found?
int_str = "int(len("			# Replace len( with int(len(.
eol_str = "\n" 				# Find end of line.
str3 = ")\n"    				# Insert ) before eol.
found_cntr = 0					# Count number of lines edited.
line_chg_num = []				# List of lines that have been edited.
y = 0								# Index for line_chg_num.
lines_chg_list = []			# List lines that were changed.
insert_eol = 0					# Insert ) at eol flag.
another_line_flg = 0 		# String "len(" is found on another line

with open(args.infile_filename, "r") as infile:
	# Read entire file into memory.
	lines = infile.readlines()
	for i in range(0, len(lines)):
		if args.conv:	# If argument conv is set, look for convert_bin... function.
			if lines[i].find(conv_str) > -1:		# If convert_bin... function is found.
				if lines[i].find(len_str) > -1:	# If string "len(" is found.
					lines[i] = lines[i].replace(len_str, int_str)
					lines[i] = lines[i].replace(eol_str, str3)
					found_cntr = found_cntr + 1			# Set found counter
					line_chg_num.insert(y, i + 1)			# Add line changed.
					lines_chg_list.insert(y, lines[i])	# Add lines edited.
					y = y + 1
				else:	# If string "len(" is not found.
					another_line_flg = 1; 	# Set for another line, assume has "len(" on another line.
			else: # If convert_bin... function is not found.
				if another_line_flg == 1:	# If string "len(" is found on another line.
					if lines[i].find(len_str) > -1: 	# If string "len(" is found, if not try again.
						another_line_flg = 0 			# Clear flag if found string "len(".
						lines[i] = lines[i].replace(len_str, int_str)
						lines[i] = lines[i].replace(eol_str, str3)
						found_cntr = found_cntr + 1	
						line_chg_num.insert(y, i + 1)
						lines_chg_list.insert(y, lines[i])		
						y = y + 1
		else: # If argument conv is not set, look for str "print ".		
			#print(i)
			# If str1 is found do something.
			if lines[i].find(str1) > -1:
				op_par_cnt = lines[i].count('(')
				print("Line %d: op_par_cnt %d" % (i+1, op_par_cnt))
				cl_par_cnt = lines[i].count(')')
				print("Line %d: cl_par_cnt %d" % (i+1, cl_par_cnt))
				lines[i] = lines[i].replace(str1, str2)
				found_cntr = found_cntr + 1
				# Have to use insert() to add element in list.
				# Cannot add or remove from list during iteration.
				line_chg_num.insert(y, i + 1)                     
				lines_chg_list.insert(y, lines[i])
				y = y + 1
				if op_par_cnt == cl_par_cnt: # If counts are the same.
					lines[i] = lines[i].replace(eol_str, str3)
				else: # If counts are not the same.
					insert_eol = 1 # For next line.
			else: # If "print " is not found
				if insert_eol == 1:
					# If flag is set, insert closing ) at eol.
					lines[i] = lines[i].replace(eol_str, str3)
					# Clear insert_eol flag after inserting closing ).
					even_cnt = 0

print("Lines edited: %d" % found_cntr)
print("Lines that were changed: %s" % str(line_chg_num))
for j in lines_chg_list:
	print("String that was changed: %s" % j)
  
with open(args.infile_filename, "w") as outfile:
	for list_item in lines:
		outfile.write('%s' % list_item)

#EOF	                   
