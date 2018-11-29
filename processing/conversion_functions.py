#!/usr/bin/env python

"""
File: conversion_functions.py
Project: REASON
Company: Jet Propulsion Laboratory

Description:
Collection of common functions used across all VASA command scripts.
"""

import os
import binascii
import argparse
import struct

# zfill zero-pads MSB of string with 0s up to the length (argument); if 
# original length is greater than argument length, then the original string 
# is returned

def reverse_bits(num_byte):
	'''Performs bit reversal on byte.

	Args:
		num_byte: byte

	Returns:
		num_byte_reverse: byte with bits reversed
	'''
	num_int = int("0x" + num_byte, 0)
	num_int_reverse = int("{:08b}".format(num_int)[::-1], 2)
	num_byte_reverse = hex(num_int_reverse)[2:].zfill(2)
	return num_byte_reverse

def get_byte_seq_from_bin(bin_data, byte_len, byte_start_no):
	byte_seq = ''
	for byte_no in range(byte_start_no, byte_start_no + byte_len):
		byte_int = struct.unpack_from('B', bin_data, byte_no)
		byte_hex = convert_int_to_hex(byte_int[0], 2)
		byte_seq = byte_seq + byte_hex
	return byte_seq



def convert_int_to_bin(num_int, bit_width):
	"""Converts int to binary

	Args:
		num_int: number as an integer
		bit_width: number of bits to represent number in binary after 
				   conversion
	Returns:
		num_bin: number in binary
	"""
	num_bin = bin(num_int)[2:].zfill(bit_width)
	return num_bin

def convert_hex_to_bin(num_hex, bit_width):
	"""Converts hex to binary -> convert back to int first with base	

	Args:
		num_int: number in hex
		bit_width: number of bits to represent number in binary after 
				   conversion
	Returns:
		num_bin: number in binary
	"""
	num_int = convert_hex_to_int(num_hex)
	num_bin = convert_int_to_bin(num_int, bit_width)
	return num_bin

def convert_bin_to_hex(num_bin, char_width):
	"""Converts bin to hex -> convert back to int first with base

	Args:
		num_bin: number in binary
		char_width: number of characters to represent number in hex after 
					conversion
	Returns:
		num_bin: number in binary
	"""
	base_bin = 2
	num_int = int(num_bin, 2)
	num_hex = hex(num_int)[2:].zfill(char_width)
	return num_hex

def convert_int_to_hex(num_int, char_width):
	"""Converts int to hex

	Args:
		num_int: number as an integer
		char_width: number of characters to represent number in hex after 
					conversion
	Returns:
		num_hex: number in hex
	"""
	num_hex = hex(int(num_int))[2:].zfill(char_width)
	return num_hex

def convert_hex_to_int(num_hex):
	"""Converts hex to int

	Args:
		num_int: number in hex
	Returns:
		num_hex: number as an integer
	"""
	base_hex = 16
	num_int = int(num_hex, base_hex)
	return num_int

# Obsoleted
def stitch_params(*params):
	"""Concatenates indefinite list of parameters (bits) into full 32-bit word
	
	Args:
		params: list of strings to concatenate
	Returns:
		word: single string of concatenated strings in params list
	"""
	word = ''
	for param in params:
		word = word + param
	return word

def export_list_to_file(list, filename):
	"""Prints list to file

	Args:
		list: list to print(to file)
		filename: filename of file where list is printed to
	"""
	with open(filename, "w") as file:
		for item in list:
			file.write("%s\n" % item)
	print("Saved file as %s" % filename)

def verify_directory_exists(directory):
	"""Checks if selected directory exists

	Args:
		directory: directory name
	"""
	if not os.path.exists("./" + directory):
		os.makedirs(directory)
	os.chdir(directory)

def extend_to_word_boundary(cycle_event):
	"""Extends collection of cycle event definitions (24-bit) to word boundary 
	(32-bits)
	
	Args:
		cycle_event: single hex string or list of hex strings; 6 characters 
					 wide each
	Returns:
		word: single hex string or list of hex strings; 8 characters wide 
			  each
	"""
	packet_length_hex = 8	# 8 bytes in 32-bit words
	if type(cycle_event) is list:
		# 1. Concatenate cycle event bytes together
		# 2. Zero-fill lower-side bytes of concatenated cycle event bytes 
		# such that it is divivisible by 8 bytes (32-bit word boundary)
		# 3. Split concatenated bytes up to 8 byte segments (one 32-bit word).
		# The final product should be a list with elements each 32-bits wide 
		# up to the word boundary.
		cycle_event_concat = ''
		cycle_event_concat = cycle_event_concat.join(cycle_event)
		zero_fill = 8 - (len(cycle_event_concat) % 8)
		cycle_event_concat_extend = cycle_event_concat.ljust(
			(len(cycle_event_concat) + zero_fill), '0')
		word = [cycle_event_concat_extend[index:index + 
			packet_length_hex] for index in range(0, 
				len(cycle_event_concat_extend), packet_length_hex)]
		return word
	else:
		# ljust is similar to zfill but suffix instead of prefix. If length 
		# is original length is less than argument length, then the original 
		# string is returned
		word = cycle_event.ljust(packet_length_hex, '0')
		return word

def generate_crc32(data):
	"""Calculates 32-bit CRC of data using 0x00000000 initial value. Note: 
	binascii.crc32 2nd argument is the initial value, but 0xFFFFFFFF generates 
	the correct CRC 0x00000000 initial value, which does not make sense.

	Example online calculator:
	http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
	- CRC32, Custom, polynomial 0x4C11DB7, initial value 0x00000000, final xor 
	value 0xFFFFFFFF, result is byte swapped

	Args:
		data (hex byte string)

	Returns:
		crc_byte_swap: 32-bit CRC (hex byte string)
	"""
	# & 0xFFFFFFF is needed to generate the same output for positive and 
	# negative results from binascii.crc32 (some unsigned/signed artifact)
	crc_int = binascii.crc32(binascii.a2b_hex(data), 0xFFFFFFFF) & 0xFFFFFFFF
	crc_byte = '%x' % crc_int
	crc_byte_swap = ""
	# swap the byte order of crc_byte (LSByte = MSByte)
	for index in range(len(crc_byte)-2, -2, -2):
		crc_byte_swap = crc_byte_swap + crc_byte[index:index+2]
	return crc_byte_swap
	
# Function to convert binary index to rfes txrx mapping bit.
# Switcher is dictionary data type here
def index_to_map_bit(argument):
	switcher = {        
							3: "RFES VHF TX Power Level Bit 2		x6000_1004_12 - ",
							4: "RFES VHF TX Power Level Bit 1		x6000_1004_10 - ",
							5: "RFES VHF TX Power Level Bit 0		x6000_1004_08 - ",
							6: "RFES VHF RX Gate			x6000_1004_14 - ",
							7: "RFES VHF PA Gate 2			x6000_1004_16 - ",
							8: "RFES VHF Driver Gate 1			x6000_1004_18 - ",
							9: "RFES VHF RX-S RST			x6000_1000_02 - ",
							10: "RFES VHF RX-S Gain Control Data		x6000_1000_04 - ",
							11: "RFES VHF RX-S Gain Control Clock	x6000_1000_06 - ",
							12: "RFES VHF RX-S Enable			x6000_1000_08 - ",
							13: "RFES VHF RX-S Cal Switch		x6000_1000_10 - ",
							14: "RFES VHF RX-P RST			x6000_1000_12 - ",
							15: "RFES VHF RX-P Gain Control Data		x6000_1000_14 - ",
							16: "RFES VHF RX-P Gain Control Clock	x6000_1000_16 - ",
							17: "RFES VHF RX-P Enable			x6000_1000_18 - ",
							18: "RFES VHF RX-P Cal Switch		x6000_1000_20 - ",
							19: "RFES HF TX Power Level - Bit 2		x6000_1004_24 - ",
							20: "RFES HF TX Power Level - Bit 1		x6000_1004_22 - ",
							21: "RFES HF TX Power Level - Bit 0		x6000_1004_20 - ",  
							22: "RFES HF RX Gate				x6000_1004_26 - ",
							23: "RFES HF PA Gate				x6000_1004_28 - ",
							24: "RFES HF Driver Gate			x6000_1004_30 - ",
							25: "RFES HF RX RST				x6000_1000_22 - ",
							26: "RFES HF RX Enable			x6000_1000_24 - ",
							27: "RFES HF RX Cal Switch			x6000_1000_26 - ",
							28: "RFES HF Gain Control Data		x6000_1000_28 - ",
							29: "RFES HF Gain Control Clock		x6000_1000_30 - ",
	}

	# get() method of dictionary data type returns 
	# value of passed argument if it is present 
	# in dictionary otherwise second argument will
	# be assigned as default value of passed argument
	return switcher.get(argument, "Not a rfes txrx mapping bit")
	
# EOF