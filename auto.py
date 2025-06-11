import websocket
from threading import Thread
import threading
import json
import random
import sys
import time
import os
import requests
from datetime import datetime
import colorama
from colorama import Fore, Style
import ctypes

y = Fore.YELLOW
m = Fore.CYAN
r = Fore.RED
g = Fore.GREEN
re = Style.RESET_ALL
dim = Style.DIM

config_id = ""
config_setting = ""
version = "2.10"

with open("data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)



def update_banner():
    global banner
    banner = f'''{m}
                _                      _                _   _               
     /\        | |            /\      | |              | | (_)              
    /  \  _   _| |_ ___      /  \   __| |_   _____ _ __| |_ _ ___  ___ _ __ 
   / /\ \| | | | __/ _ \    / /\ \ / _` \ \ / / _ \ '__| __| / __|/ _ \ '__|
  / ____ \ |_| | || (_) |  / ____ \ (_| |\ V /  __/ |  | |_| \__ \  __/ |   
 /_/    \_\__,_|\__\___/  /_/    \_\__,_| \_/ \___|_|   \__|_|___/\___|_|   

License Expiry: {r} Failed to fetch   {m}
Version: {re} {version}   {m}
Config Selected: {re}{config_id} {m}                   
'''

def set_console_title():
    ctypes.windll.kernel32.SetConsoleTitleW("Auto Advertiser v2 | Discord.gg/E13")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    set_console_title()
   
    global config_setting
    clear_screen()
    print(banner)
    print(f"""{m}
1 {re}| Start Advertiser {m}
2 {re}| Change Config {m}
3 {re}| Settings {m}

""")
    
    option = input(f"{m}INPUT {re}| Select An Option: ")
    if option == "2":
        change_config()
    elif option == "1":
        Auto_Advertise()
    elif option == "3":
        settings()
    else:
        print("Invalid option.")
        menu()

def change_config():
    global config_id
    global config_setting
    clear_screen()
    print(banner)
    config = input(f"{m}INPUT {re}| Enter your config name: ")
    config_setting = f"configs/{config}.json"
    if os.path.isfile(config_setting):
        config_id = config
        update_banner()
        print(f"{m}INFO  {re}| {g}Selected config: {config}{re}")
        time.sleep(2)
        menu()
    else:
        print(f"{m}INFO  {re}| {r}Invalid config: {config}{re}")
        time.sleep(2)
        change_config()

def settings():
    clear_screen()
    print(banner)
    print(f"{m}INFO  {re}| Settings menu not yet implemented{re}")
    time.sleep(2)
    menu()

def send_message(channel_id, slowmode, content, Token):
    while True:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        headers = {'Authorization': f'{Token}'}
        data = {"content": content}

        keep_length = len(Token) // 2
        hidden_Token = Token[:keep_length] + "*" * 8

        response = requests.post(url, headers=headers, json=data)                       
        current_time = datetime.now()

        if response.status_code == 200:
            print(f"{m}SENT {re}| Successfully sent message | [Token: {m}{hidden_Token}{re}]")
        else:
            print(f"{r}FAILED {re}| Failed to send message | [Token: {m}{hidden_Token}{re}]")

        time.sleep(slowmode)

def Auto_Advertise():
    global config_setting
    threads = []

    with open("data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(config_setting, 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    content = data2["message"]
    Token = data["Token"]
    for channel_id, slowmode in data2["Channel_Ids"].items():
        if isinstance(channel_id, str) and channel_id.isdigit():
            thread = threading.Thread(target=send_message, args=(channel_id, slowmode, content, Token))
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()





update_banner()
menu()