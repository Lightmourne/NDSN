# importing required libraries

import requests
from requests.exceptions import *
from datetime import datetime
import surrogates
import ping3
import time
from devices import devices
from concurrent.futures import ThreadPoolExecutor
import csv

online = surrogates.decode('\U0001f7e2') # green circle icon (online)
offline = surrogates.decode('\U0001f534') # red circle icon (offline)

ip_devices = devices # device dictionary (key - ip, values - built-in dictionary with names and locations)
active_ips = []  # list of available IP addresses
inactive_ips = []  # list of unavailable IP addresses

TOKEN = "PAST_YOUR_TOKEN_HERE" # your Telegram Bot token
chat_id = "PAST_YOUR_CHAT_ID_HERE" # your chat id

def ping(ip):
    counter = 0 # failure counter
    device_info = ip_devices[ip]
    name = device_info["name"]
    location = device_info["location"]
    response_time = ping3.ping(ip, timeout=8, size=32)
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')
    if response_time is not None:
        return current_date, current_time, name, location, ip, "up"
    elif response_time is None:        
        while counter < 2:
            counter += 1
            response_time = ping3.ping(ip, timeout=6, size=32)
            if response_time is not None:
                return current_date, current_time, name, location, ip, "up"
        return current_date, current_time, name, location, ip, "down"

with ThreadPoolExecutor(max_workers=10) as executor: # number of threads - 10, can be changed at your discretion
    results = executor.map(ping, ip_devices.keys())
    
for i in results:
    if i[5] == "down": #i[5] - device status
        inactive_ips.append(i[4]) #i[4] - device ip
    else:
        active_ips.append(i[4])
        
print(f'Online devices at the time of program start: {active_ips}')
print()
print(f'Offline devices at the moment of program start: {inactive_ips}')

while True:
    with ThreadPoolExecutor(max_workers=10) as executor: # number of threads - 10, can be changed at your discretion
        results = executor.map(ping, ip_devices.keys())
    for i in results:
        if i[5] == "down" and i[4] not in inactive_ips:
            inactive_ips.append(i[4])
            if i[4] in active_ips:
                active_ips.remove(i[4])
            message = f"{offline} {i[2]} {i[3]} ({i[4]}) offline \n{i[0]} {i[1]}"
            filename = "ping_log.csv"
            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                # recording of headers, if they were missing
                if file.tell() == 0:
                    writer.writerow(["Date", "Time", "Device name", "Location", "IP address", "Status"])
                # ping result recording
                writer.writerow(list(i))
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            try:
                requests.get(url).json()
            except ConnectionError:
                print('connection error', ':', message)
            except socket.gaierror:
                print('socket.gaierror')
            except urllib3.exceptions.NewConnectionError:
                print('urllib3.exceptions.NewConnectionError')
            except urllib3.exceptions.MaxRetryError:
                print('urllib3.exceptions.MaxRetryError')
                
        elif i[5] == "up" and i[4] not in active_ips:
            active_ips.append(i[4])
            if i[4] in inactive_ips:
                inactive_ips.remove(i[4])
            message = f"{online} {i[2]} {i[3]} ({i[4]}) online \n{i[0]} {i[1]}"
            filename = "ping_log.csv"
            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                # recording of headers, if they were missing
                if file.tell() == 0:
                    writer.writerow(["Date", "Time", "Device name", "Location", "IP address", "Status"])
                # ping result recording
                writer.writerow(list(i))
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
            try:
                requests.get(url).json()
            except ConnectionError:
                print('connection error', ':', message)
            except socket.gaierror:
                print('socket.gaierror')
            except urllib3.exceptions.NewConnectionError:
                 print('urllib3.exceptions.NewConnectionError')
            except urllib3.exceptions.MaxRetryError:
                print('urllib3.exceptions.MaxRetryError')

    time.sleep(10)  # delay between device pings, it allows you to keep the network load down
