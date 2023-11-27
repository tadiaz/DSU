#Complete Assignment for CSC 846 Lab10
#@author Tony Diaz
#@category Functions

#def getString(address, size):
	# retrieve the encrypted string from memory


def decryptString(key, cipher, size):
	# implement the decryption logic from the DLL sample here

    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(cipher, key))



print("Decrypting all strings just like 0x10001210 would:")
decryptFunc = toAddr(0x10001210)
# find all of the Xrefs to 0x10001210 (decryptFunc) and iterate through them
refs = getReferencesTo(decryptFunc)
for r in refs:
    refFrom = r.getFromAddress()
    previous1 = getInstructionBefore(refFrom)
    previous2 = getInstructionBefore(previous1)
    previous3 = getInstructionBefore(previous2)
    # get the instruction before, and extract address of the obfuscated string 
    obfuscatedString = ''
    if str(previous1.getInputObjects()[0]) != 'ESP' and str(previous1.getInputObjects()[0]) != '0x4':
        obfuscatedString = str(getDataAt(toAddr(str(previous1.getInputObjects()[0]))))[4:-1]
    elif str(previous1.getInputObjects()[1]) != 'ESP' and str(previous1.getInputObjects()[1]) != '0x4':
        obfuscatedString = str(getDataAt(toAddr(str(previous1.getInputObjects()[1]))))[4:-1]
        if str(getDataAt(toAddr(str(previous1.getInputObjects()[1]))))=='None':
            current = toAddr(str(previous1.getInputObjects()[1]))
            while str(getUndefinedDataAt(current))[-3:] != '00h':
                obfuscatedString += str(getUndefinedDataAt(current))[3:5]
                current = current.next()
            result = ''
            for i in range(0,len(obfuscatedString),2):
                hex_pair = obfuscatedString[i:i+2]
                dec = int(hex_pair, 16)
                char = chr(dec)
                result += char
            obfuscatedString = result
    else:
        obfuscatedString = str(getDataAt(toAddr(str(previous1.getInputObjects()[2]))))[4:-1]
        if str(getDataAt(toAddr(str(previous1.getInputObjects()[2]))))=='None':
            current = toAddr(str(previous1.getInputObjects()[2]))
            while str(getUndefinedDataAt(current))[-3:] != '00h':
                obfuscatedString += str(getUndefinedDataAt(current))[-1:]
                current = current.next()
    
	# get the instruction before, and extract the address of the key
    key = ''
    if str(previous2.getInputObjects()[0]) != 'ESP' and str(previous2.getInputObjects()[0]) != '0x4':
        key = str(getDataAt(toAddr(str(previous2.getInputObjects()[0]))))[4:-1] #str(getDataAt(toAddr(str(previous2.getInputObjects()))))
    elif str(previous2.getInputObjects()[1]) != 'ESP' and str(previous2.getInputObjects()[1]) != '0x4':
        key = str(getDataAt(toAddr(str(previous2.getInputObjects()[1]))))[4:-1]
    else:
        key = str(getDataAt(toAddr(str(previous2.getInputObjects()[2]))))[4:-1]
        if str(getDataAt(toAddr(str(previous2.getInputObjects()[2]))))=='None':
            current = toAddr(str(previous2.getInputObjects()[2]))
            while str(getUndefinedDataAt(current))[-3:] != '00h':
                key += str(getUndefinedDataAt(current))[-1:]
                current = current.next()

	# get the instruction before, and exract the size
    size = ''
    if str(previous3.getInputObjects()[0]) != 'ESP' and str(previous3.getInputObjects()[0]) != '0x4':
        size = str(previous3.getInputObjects()[0]) 
    elif str(previous3.getInputObjects()[1]) != 'ESP' and str(previous3.getInputObjects()[1]) != '0x4':
        size = str(previous3.getInputObjects()[1])
    else:
        size = str(previous3.getInputObjects()[2])

	# get the actual values based off of the addresses and decrypt them
    #decryptString(getString(obfuscatedString, size), getString(key, size), size)
    result = decryptString(obfuscatedString, key, size)
    

	# set a comment at the end of the line with the decrypted string value
    print("Found string: %s - %s" % (result, refFrom))