import requests
from datetime import datetime
import surrogates
import ping3
import time
from devices import devices
from concurrent.futures import ThreadPoolExecutor
import csv

# Constants
TIMEOUT_INITIAL = 8
TIMEOUT_RETRY = 6
MAX_WORKERS = 10
TOKEN = "PAST_YOUR_TOKEN_HERE" # your Telegram Bot token
chat_id = "PAST_YOUR_CHAT_ID_HERE" # your chat id

# Unicode emojis
online = surrogates.decode('\U0001f7e2') # green circle icon (online)
offline = surrogates.decode('\U0001f534') # red circle icon (offline)

# Device status tracking
ip_devices = devices # device dictionary (key - ip, values - built-in dictionary with names and locations)
active_ips = [] # list of available IP addresses
inactive_ips = [] # list of unavailable IP addresses


def ping(ip):
    counter = 0
    device_info = ip_devices[ip]
    name = device_info["name"]
    location = device_info["location"]
    
    while counter < 3:  # Retry 2 times to avoid false results
        response_time = ping3.ping(ip, timeout=TIMEOUT_INITIAL if counter == 0 else TIMEOUT_RETRY, size=32)
        if response_time is not None:
            status = "up"
            break
        counter += 1
    else:
        status = "down"

    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return current_date, current_time, name, location, ip, status

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        requests.get(url).json()
    except Exception as e:
        print(f"Error while sending message: {e}")

def log_to_csv(data):
    filename = "ping_log.csv"
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        # recording of headers, if they were missing
        if file.tell() == 0:
            writer.writerow(["Date", "Time", "Device name", "Location", "IP address", "Status"])
        # ping result recording
        writer.writerow(list(data))

def update_status(ip, status, current_date, current_time, name, location):
    if status == "down" and ip not in inactive_ips:
        inactive_ips.append(ip)
        if ip in active_ips:
            active_ips.remove(ip)
        message = f"{offline} {name} {location} ({ip}) offline \n{current_date} {current_time}"
        log_to_csv((current_date, current_time, name, location, ip, status))
        send_message(message)
    elif status == "up" and ip not in active_ips:
        active_ips.append(ip)
        if ip in inactive_ips:
            inactive_ips.remove(ip)
        message = f"{online} {name} {location} ({ip}) online \n{current_date} {current_time}"
        log_to_csv((current_date, current_time, name, location, ip, status))
        send_message(message)

def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(ping, ip_devices.keys())

    for data in results:
        current_date, current_time, name, location, ip, status = data
        update_status(ip, status, current_date, current_time, name, location)

    time.sleep(10)  # Delay between device pings, adjust as needed


# Pre-scan to append the list of online and offline devices
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
	results = executor.map(ping, ip_devices.keys())

for data in results:
	current_date, current_time, name, location, ip, status = data
	if status == "down":
		inactive_ips.append(ip)
	else:
		active_ips.append(ip)
print(f'{online} Online devices at the time of program start: {active_ips}')
print()
print(f'{offline} Offline devices at the moment of program start: {inactive_ips}')


if __name__ == "__main__":
    while True:
        main()
