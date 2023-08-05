# NDSN (Network Device Status Notifier)

NDSN is an application designed to monitor the status of devices on the network. When the device status changes, you can be notified via your Telegram bot. In addition, NDSN logs events to a csv file, which allows you to analyze past events using tools such as: pandas, MS Excel, LibreOffice Calc and others.

## ? How it works

1. You need to create a Telegram Bot. Link to official Telegram documentation [How Do I Create a Bot?](https://core.telegram.org/bots#how-do-i-create-a-bot).
In the [main.py](https://github.com/Lightmourne/NDSN/blob/main/main.py) you need to insert your unique telegram bot token (line 14) and your chat id (line 15).
This is necessary for the application to be able to send a message to the Telegram bot and this message will be displayed only to the unique user with the specified chat id.

2. You need to make changes to the [devices.py](https://github.com/Lightmourne/NDSN/blob/main/devices.py). This file consists of a dictionary whose key is the device's IP address and whose value is another dictionary that contains information about the device's name and location.
   >Each time after adding a new device to the [devices.py](https://github.com/Lightmourne/NDSN/blob/main/devices.py) you need to restart the program if it is currently running.

3. For the application to work correctly you need to install dependencies from the file [requirements.txt](https://github.com/Lightmourne/NDSN/blob/main/requirements.txt)
   >To do this, you need to execute the command:
   ```bash
    python3 -m pip install -r requirements.txt
    ```

After starting the application you will see in the terminal a list of online and a list of offline ip-addresses of devices from the [devices.py](https://github.com/Lightmourne/NDSN/blob/main/devices.py) at the moment of program start.
![start_app](https://github.com/Lightmourne/NDSN/blob/main/img/start_app.png)

In the future, you will receive a notification from the Telegram Bot when the status of your device changes.

![[telegram_scr](https://github.com/Lightmourne/NDSN/assets/72374407/29b46274-da36-4577-a0d0-1b239d6135d1)](https://github.com/Lightmourne/NDSN/blob/main/img/telegram_scr.PNG)

## Viewing logs
Now the [ping_log.csv](https://github.com/Lightmourne/NDSN/blob/main/ping_log.csv) file has appeared in the root folder of the project. We can look at the changes that were added to this file using python and pandas. 

![logs](https://github.com/Lightmourne/NDSN/blob/main/img/log.png)

## What's New
### 2023-08-05 Added the option to visualize logs as an html document.
By default, events for the last 5 days from the current date are displayed. You can specify your own value "days", to do this you need to execute:
```bash
    python3 log_list_to_html.py --days=n
```
>Where n - is the count of days from the current date for which you want to receive the report.

Example:

![log_list_to_html.png](https://github.com/Lightmourne/NDSN/blob/main/img/log_list_to_html.png)



