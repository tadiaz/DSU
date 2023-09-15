#!/usr/bin/python3

import sys
import subprocess
import os

def main():
	# define variables for paths and names of things
	plugin_path = '/opt/oledump-files/'
	filename=sys.argv[1]
	plugin_name='plugin_biff'
	plugin_option="-x"
	plugin_option2="-o BOUNDSHEET -a"
	# run our system command to see what oledump tells us about the file
	output = subprocess.Popen("oledump.py -p "+plugin_name+" --plugindir="+plugin_path+" --pluginoptions '"+plugin_option+"' "+filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
	# split up the output of the system command into a string array so we can iterate through it later
	outcome = output.stdout.read().split()
	# set up variables which will help us later for the state of our sheet, the sheet name, whether we have a hidden sheet, etc...
	state=""
	sheet=""
	hidden=False
	sheet_names = []
	
	# run through our str array which has the oledump outcome, if a string in our array is 0085 that means we likely have 
	# sheet info and can find out if its hidden or visible so look at the following appropriate string then print out results
	for i in range(len(outcome)):
		if outcome[i]=='0085':
			state=outcome[i+11]
			sheet = outcome[i+13]
			if state == 'very':
				state=state+" "+outcome[i+12]
				sheet = outcome[i+14]
			if 'hidden' in state and hidden==False:
				hidden=True
			if 'hidden' in state:
				sheet_names.append(sheet)
			print("Sheet name: "+sheet+", Sheet state: "+state)
			
	# run another oledump command this time to see what bytes we need to change by using the option -o BOUNDSHEET -a
	output = subprocess.Popen("oledump.py -p "+plugin_name+" --plugindir="+plugin_path+" --pluginoptions '"+plugin_option2+"' "+filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
	# save our outcome for iterating through later
	outcome = output.stdout.read().split()
	
	# here we look for the bytes that will identify where is the byte we need to change to make the sheet visible
	# if we find a string in our outcome array with 00000000: then we know the byte we need to change is 5 strings later
	# if its a 02 or 01 we have a hidden sheet so we keep track of the bytes leading up to it so we can change it later
	byte_array = []
	for i in range(len(outcome)):
		if outcome[i]=='00000000:':
			if outcome[i+5]=='02' or outcome[i+5]=='01':
				byte_array.append([outcome[i+1],outcome[i+2],outcome[i+3],outcome[i+4]])
	
	# set up our variables to run through our binary file 
	row = 0
	column = 0
	# if we have a hidden file, let's copy the file so the original is left alone
	if hidden:
		os.system("cp "+filename+" copy_of_"+filename)
	
		# we open the binary file, read through one byte at a time, if we get a sequence of bytes that match what oledump
		# gave us earlier then we change the next byte to 00 so the sheet becomes visible
		with open("copy_of_"+filename, "rb+") as file:
			while True:
				byte1 = file.read(1)
				if not byte1:
					break
				if row < len(byte_array):
					if str(byte1)=="b'\\x"+byte_array[row][column+1].lower()+"'":
						byte1 = file.read(1)
						if str(byte1)=="b'\\x"+byte_array[row][column+2].lower()+"'":
							byte1 = file.read(1)
							if str(byte1)=="b'\\x"+byte_array[row][column+3].lower()+"'":
								file.write(b'\x00')
								row+=1
		# since a sheet was hidden, we let the user know that we made a copy of the file and what sheets we made visible
		print("Hidden sheets were detected, a copy of the file has been created and the following sheets were made visible:")
		for sheet in sheet_names:
			print("Sheet: "+sheet, end=". ")
		print()
		
if __name__ == "__main__":
	main()
