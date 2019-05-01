#!/usr/bin/env python
# Written by:	Ian Catapano
# Purpose:	To convert 32 bits to bytes change to handle 8 bits at a time

import numpy as np

file = open('bits.txt')			# Open source of bits
binArray = []				# Array to hold string elements

# Split each new line in the file into lines in a list
data = file.read().splitlines()

# Process one line of string input
for line in data:

	# Read in each element of the string input into an array
	for number in line:
		c = int(number)
		binArray.append(number)
	binArray = map(int, binArray)	# Convert array to integer
	
	# 32 bits in correct format, convert from bits to bytes
	intArray = np.packbits(binArray, axis=-1)
	binArray = []			# Empty array
	
	# Output the converted bits to bytes to a file
	outFile = open('int.txt', 'a')
	for item in intArray:
		outFile.write("%d " % item)
	outFile.write("\n")

# Close open files
file.close()
outFile.close()
