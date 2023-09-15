#!/usr/bin/python3

import sys
import subprocess
import os

def main():
	plugin_path = '/opt/oledump-files/'
	filename=sys.argv[1]
	plugin_name='plugin_biff'
	plugin_option="-x"
	plugin_option2="-o BOUNDSHEET -a"
	output = subprocess.Popen("oledump.py -p "+plugin_name+" --plugindir="+plugin_path+" --pluginoptions '"+plugin_option+"' "+filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
	outcome = output.stdout.read().split()
	state=""
	sheet=""
	hidden=False
	sheet_names = []
	
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
			
	output = subprocess.Popen("oledump.py -p "+plugin_name+" --plugindir="+plugin_path+" --pluginoptions '"+plugin_option2+"' "+filename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
	outcome = output.stdout.read().split()
	
	byte_array = []
	for i in range(len(outcome)):
		if outcome[i]=='00000000:':
			if outcome[i+5]=='02' or outcome[i+5]=='01':
				byte_array.append([outcome[i+1],outcome[i+2],outcome[i+3],outcome[i+4]])
	
	file_bytes = b""
	with open(filename, "rb") as f:
		while(byte := f.read(1)):
			file_bytes += byte
	file_str_array = (str(file_bytes)+"").split('\\x')
	row = 0
	column = 0
	location = 0
	if hidden:
		os.system("cp "+filename+" copy_of_"+filename)
	
		with open("copy_of_"+filename, "rb+") as file:
			while True:
				byte1 = file.read(1)
				location+=1
				if not byte1:
					break
				if row < len(byte_array):
					if str(byte1)=="b'\\x"+byte_array[row][column+1].lower()+"'":
						byte1 = file.read(1)
						location+=1
						if str(byte1)=="b'\\x"+byte_array[row][column+2].lower()+"'":
							byte1 = file.read(1)
							location+=1
							if str(byte1)=="b'\\x"+byte_array[row][column+3].lower()+"'":
								file.write(b'\x00')
								row+=1
		print("Hidden sheets were detected, a copy of the file has been created and the following sheets were made visible:")
		for sheet in sheet_names:
			print("Sheet: "+sheet, end=". ")
		print()
		
if __name__ == "__main__":
	main()