# THIS MODULE WILL HOUSE MAIN UI LOGIC


# UI IMPORTS
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
import pyfiglet
console = Console()



# NSM IMPORTS
from nsm_utilities import Utilities, NetTilities
from nsm_logic import Packet_Creation
from nsm_pinger import Module_Controller
from nsm_files import File_Handler


# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import ARP, ICMP, sendp, conf, ICMP, sr1, IP, send, ARP, Ether, srp


# ETC IMPORTS
import threading, requests, time, random



# FILE IMPORTS
from pathlib import Path
import json




class MainUI():
    """This method will be responsible for holding main ui logic"""

    def __init__(self):
        pass
    
    @staticmethod
    def main_title():
        """Create pyfiglet art"""
        
        
        use = False
        

        if use:
            arts = pyfiglet.FigletFont.getFonts()
        

            for art in arts:   
                pic = pyfiglet.figlet_format(text="HEY YOUTUBE", font=art)   
                console.print(f"Font being used: {art}")
                console.print(f"[bold red]{pic}")

                time.sleep(.02)
        

        else:
            title = pyfiglet.figlet_format(text="      Net\n Booter 2.0", font="bloody")

            console.print(f"[bold red]\n\n{title}")
    
    
    @staticmethod
    def main_menu():
        """this method will house programmic logic to traverse other file modules"""



        # SET MAIN MENU OPTIONS
        color_in = "[bold blue]"
        color_out = "[bold red]"
        

        choices = (
            f"   {color_out}[1]{color_in} UDP Flood\n"
            f"   {color_out}[2]{color_in} PING DDOS\n"
            f"   {color_out}[3]{color_in} ARP POison\n\n"
            f"   {color_out}[4]{color_in} Attack Log\n"
            f"   {color_out}[5]{color_in} Settings\n"
            f"   {color_out}[6]{color_in} Help Menu\n"
            f"   {color_out}[7]{color_in} Exit"
        )

        console.print("\n\n\n")
        console.print(choices, "\n\n")
        while True:

            try:
                

                # NOT IN USE
                panel = Panel(
                    title="Attack Methods",
                    renderable= (
                        "1. UDP Flood\n",
                                 "2. PING DDOS\n",
                                 "3. ARP Poison\n",
                                  "4. Attack Log\n"
                                  "5. Settings\n" 
                                  "6. Help Menu\n"
                                  "7. Exit"),

                    style= "bold purpl"
                )

                
                choice = console.input("[bold red]Enter choice here: ")
                

                # USE THIS CONDITION TO CLEAR SCREEN FROM ONE SPOT DYNAMICALLY
                cc = ["1", "2", "4"]
                if choice in cc:
                    Utilities.clear_screen()
                

                #UDP FLOODER
                if choice == "1":
                    Packet_Creation.main()

                    break

                
                # PING SMURFER // DDOS
                elif choice == "2":
                    Module_Controller.main()

                    break
 

                # ARP POISON               
                elif choice == "3":

                    console.print("[yellow]Under construction")
                    
             
                # ATTACK LOG   
                elif choice == "4":
                    File_Handler.show_attack()
                    
                    break
                    
                
                # HELP MENU
                elif choice == "5":

                    console.print("[yellow]Under construction")
                    

                #SETTINGS
                elif choice == "6":

                    console.print("[yellow]Under construction")

                
                # EXIT
                elif choice == "7":

                    console.print("[yellow]Under construction")

                
                else:
                    console.print(f"\n[bold red]Condition Error: [yellow]{choice} is not a valid option")
                    
            
            except Exception as e:
                console.print(e)
    
    

    @staticmethod
    def main():
        """This is where the main ui will begin"""

        net = NetTilities()

        
        
        while True:
            Utilities.clear_screen()
            net.get_conn_status()
            MainUI.main_title()
            MainUI.main_menu()
       




# FOR MODULE TESTING ONLY
if __name__ == "__main__":

    MainUI.main()