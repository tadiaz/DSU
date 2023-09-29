#!/usr/bin/python3

import sys
import subprocess
import os

def main(path):
	# lets run a command in a shell to list out the files in the given directory from the path variable 
	output = subprocess.Popen("ls "+path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
	# we save the output and split it up into a string list to make it easier to parse
	outcome = output.stdout.read().split()

	# for every file we found in the diretory lets run it against Virus Total and Triage
	for file in outcome:
		# print out the file name
		print('Checking file: '+file)
		# lets run a command in a shell to scan our file against virus total
		output1 = subprocess.Popen("malwoverview.py -v 1 -V "+path+file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
		# we save the output and split it up into a string list to make it easier to parse
		outcome1 = output1.stdout.read().split()

		# if we find the worse SAMPLE then we know the file is new to virus total
		if outcome1[1] == 'SAMPLE':
			print("Sample is new to VirusToal")
		# otherwise we look for the word Label because the next things is what virus total flagged our file as
		else:
			for i in range(len(outcome1)):
				if outcome1[i]=='Label:':
					print('Virus Total: '+outcome1[i+1])

		# lets run a command in a shell to find the md5 hash of our file and save just the hash value
		output2 = subprocess.Popen("md5sum "+(path+file)+" | awk '{print $1}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
		outcome2 = output2.stdout.read()

		# lets use the hash value to scan against triage
		output3 = subprocess.Popen("malwoverview.py -x 1 -X " + outcome2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
		outcome3 = output3.stdout.read().split()
		id=''

		# if our length is greater than 7 let's snag the id that triage has for our file
		if len(outcome3)>7:
			id = outcome3[8]
		# otherwise the file is new to triage
		else:
			id = None
		# if the file is new, print out that it is
		if id == None:
			print("Sample is new to Triage\n")
		# otherwise lets slice the string to leave behind the ansi escape value and grab just the id
		else:
			id = id[4:]
			# lets run a command in a shell to scan our id against traige
			output4 = subprocess.Popen("malwoverview.py -x 2 -X " + id.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
			outcome4 = output4.stdout.read().split()
			# for every word that comes back lets search until we find the signatures section then print out what triage flagged the file as
			for i in range(len(outcome4)):
				if outcome4[i] == 'signatures:':
					print(str(chr(27)+'[0m')+'Triage: ',end='')
					# we will continue printing what triage says the file is until we hit the next ansi escape value or the next section
					while outcome4[i+3] != str(chr(27)+'[93m') and outcome4[i+3] != 'targets:':
						print(outcome4[i+3], end=' ')
						i+=1
					print('\n')
		

if __name__ == "__main__":
	# start the main function and send in the first command line arguement as the path to the directory we want to scan
	path = sys.argv[1]
	main(path)