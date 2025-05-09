# THIS METHOD WILL BE RESPONSIBLE FOR HANDLING FILE INTERACTIONS


# UI IMPORTS
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
import pyfiglet
console = Console()



# NSM IMPORTS
from nsm_utilities import Utilities, NetTilities
from nsm_pinger import Network_Scanner


# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import ARP, ICMP, sendp, conf



# ETC IMPORTS
import threading, requests, time, random, os
from datetime import datetime
lock = threading.Lock()


# FILE IMPORTS
from pathlib import Path
import json

base_dir = Path.home() / "Documents/nsm tools/.data/NetBooter 2.0"
base_dir.mkdir(parents=True, exist_ok=True)



class File_Handler():
    """This class will be responsible for handling any and all file operations"""


    def __init__(self):
        pass


    @staticmethod
    def save_attack(target_ip, attack_method, attack_duration, total_packets_sent, console=console):
        """This method will be called upon after each attack is complete to save statistics"""


        # STATIC VARIABLES
        file_path = base_dir / "Attack Log"

        
        # LOOP FOR EXCEPETIONS
        while True:
            
            try:
                if base_dir.exists() and file_path.exists() and file_path.is_dir():

                    # CREATE TIMESTAMP AND ALSO GET TIME AND DATE FROM SAID TIMESTAMP TO CREATE A FILE PATH NAME
                    time_stamp = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")


                    stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                    file_name = f"{stamp}.json"
                    
                    data = {
                        "TimeStamp": time_stamp,
                        "Target IP": target_ip,
                        "Attack Method": attack_method,
                        "Attack Duration": attack_duration,
                        "Total Packets Sent": total_packets_sent
                    } 
                     
                    

                    # NEW FILE PATH TO SAVE INFO
                    path = file_path / file_name
                    with open(path, "w") as file:
                        json.dump(data, file, indent=5)

                        console.print("[bold green]Attack Log successfully saved")
                         
                        break
                

                else:
                    
                    # CREATE BASE DIR
                    base_dir.mkdir(exist_ok=True, parents=True)

                    
                    # CREATE THE ATTACK LOG DIR
                    file_path.mkdir(exist_ok=True, parents=True)

                    console.print("\n[bold green]Successfully Recreated Static Directories")
            

            except Exception as e:
                console.print("[bold red]NSM_Files Module Error: [yellow]",e)
                time.sleep(2)
                break


    @staticmethod
    def show_attack() -> str:
        """This method will iterate through the attack log showing any and all saved attacks that we did"""

        
        # STATIC VARIABLES
        file_path = base_dir / "Attack Log"
        view = 1
        LINE = "-" * 30


        # PRINT A NICE WELCOME TITLE
        art = pyfiglet.figlet_format(text="Attack\n    Log", font="bloody")



        
        # LOOP FOR EXCEPTIONS
        while True:
            console.print(art, style="bold purple")
            print("\n")

            
            try:

                if file_path.exists() and base_dir.exists() and file_path.is_dir():


                    for file in file_path.iterdir():

                        
                        # CAPTURE
                        if file:


                            # FOR WINDOWS
                            if os.name == "nt":           

                                # USE THIS TO GET FILE NAME AND DATE ALONG WITH TIME
                                file_name = file.name.split('\\')[0]
                                date = file_name.partition("_")[0]
                                timee = file_name.partition('_')[2].split('.')[0]

                            
                            # FOR POSIX
                            else:
                                file_name = file.name
                                date = "N/A"
                                timee = "N/A"




                            with open(file, "r") as file:
                                content = json.load(file)


                                # TABLE LOGIC
                                table = Table(
                                        title=f"Date: [bold blue]{date}[/bold blue]  Time: [bold blue]{timee}",
                                        style="bold purple",
                                        border_style="bold purple",
                                        header_style="bold red",
                                        title_style="bold red"
                                        )
                                table.add_column("Key", style="bold blue")
                                table.add_column("Value", style="bold green")


                                
                                # LINE FOR JSON
                                if view == 1:
                                    console.print(LINE, "\n")

                                    
                                for key, value in content.items():



                                    # FOR JSON VIEW
                                    if view == 1:
                                        console.print(f"[bold blue]{key}: [bold green]{value}")


                                    elif view == 2 and key == "TimeStamp":

                                        try:
                
                                            table.add_row(f"TimeStamp" ,f"{content["TimeStamp"]}")
                                            table.add_row(f"Target IP" ,f"{content["Target IP"]}")
                                            table.add_row(f"Attack Method" ,f"{content["Attack Method"]}")
                                            table.add_row(f"Attack Duration" ,f"{content["Attack Duration"]}")
                                            table.add_row(f"Total Packets Sent" ,f"{content["Total Packets Sent"]}")

                                        
                                        except Exception as e:
                                            console.print(e)
                                


                                
                            if view == 1:
                                print("")
                                console.print(LINE, "\n")
                            
                            else:
                                console.print(table)
                                print("\n")

                        else:
                            console.print("[bold red]No valid files found")
                        
                    

                        
                    choice = console.input("[bold red]\nPress Enter to Exit: ").strip().lower()
                    
                    if choice == "1" or choice == "json" or choice == "y":
                        view = 1
                        Utilities.clear_screen()

                    elif choice == "2" or choice == "table" or choice == "n":
                        view = 2  
                        Utilities.clear_screen()


                    else:
                        console.print("\n\n[bold red]Laterrrrrrrrrrrrrr")
                        time.sleep(.5)
                        break
                    


                else:
                    
                    # CREATE BASE DIR
                    base_dir.mkdir(exist_ok=True, parents=True)

                    
                    # CREATE THE ATTACK LOG DIR
                    file_path.mkdir(exist_ok=True, parents=True)

                    console.print("\n[bold green]Successfully Recreated Static Directories")

                

                

            

            except Exception as e:
                console.print(e)
                time.sleep(1)
                break
    
     
    @staticmethod
    def background_thread():
        """This method will be responsible for allowing or disallowing a background thread to ping a target until false"""


        file_path = base_dir / "Background Thread"
        file_path.mkdir(exist_ok=True, parents=True)

        
        while True:
            try:

                if file_path.exists() and base_dir.exists() and file_path.is_dir():
                    

                    # CREATE AND OPEN PATH
                    path = file_path / "workers.json"

                    if path.exists():
                        with open(path, "r") as file:
                            content = json.load(file)

                            if content["background_thread"] == True:
                                return True
                            
                            else:
                                return False
                    
                    return False
                

                else:
                        
                        # CREATE BASE DIR
                        base_dir.mkdir(exist_ok=True, parents=True)

                        
                        # CREATE THE ATTACK LOG DIR
                        file_path.mkdir(exist_ok=True, parents=True)

                        console.print("\n[bold green]Successfully Recreated Static Directories")
                

            except Exception as e:
                console.print("[bold red]NSM_Files Module BACKGROUND Error: [yellow]",e)
                time.sleep(2)
                break

    

    @staticmethod
    def background_thread_controller(background_thread_status: bool):
        """This method will be responsible for controlling the background thread on weather its true or false"""

        file_path = base_dir / "Background Thread"
        file_path.mkdir(exist_ok=True, parents=True)

        
        while True:
            try:

                if file_path.exists() and base_dir.exists() and file_path.is_dir():
                    

                    # CREATE AND OPEN PATH
                    path = file_path / "workers.json"

                    with open(path, "w") as file:
                        

                        # SET BACKGROUND THREAD STATUS
                        data = {
                            "background_thread": background_thread_status
                        }

                        json.dump(data, file, indent=2)

                        #console.print("[bold green]Background Thread successfully updated")
                        break



                else:
                        
                        # CREATE BASE DIR
                        base_dir.mkdir(exist_ok=True, parents=True)

                        
                        # CREATE THE ATTACK LOG DIR
                        file_path.mkdir(exist_ok=True, parents=True)

                        console.print("\n[bold green]Successfully Recreated Static Directories")
                

            except Exception as e:
                console.print("[bold red]NSM_Files Module CONTROLLER Error: [yellow]",e)
                time.sleep(2)
                break

    
    
    @staticmethod
    def background_thread_pull_info(json_pull):
        """We will use this method to staticly pull information on json values updated by the background thread"""

        file_path = base_dir / "Background Thread"
        file_path.mkdir(exist_ok=True, parents=True)


        while True:
            try:

                if file_path.exists() and base_dir.exists() and file_path.is_dir():
                    

                    # OPEN PATH
                    path = file_path / "workers_info.json"

                    with open(path, "r") as file:
                        content = json.load(file)
                        value = content[f"{json_pull}"]

                        return value if value else 0
                        
                        
                else:
                        
                        # CREATE BASE DIR
                        base_dir.mkdir(exist_ok=True, parents=True)

                        
                        # CREATE THE ATTACK LOG DIR
                        file_path.mkdir(exist_ok=True, parents=True)

                        console.print("\n[bold green]Successfully Recreated Static Directories")
                

            except Exception as e:
                console.print("[bold red]NSM_Files Module Pull Error: [yellow]",e)
                time.sleep(2)
                break

    

    @staticmethod
    def background_thread_push_info(json_push, console):
        """This method will mainly be used by the background thread to update json values"""

        file_path = base_dir / "Background Thread"
        file_path.mkdir(exist_ok=True, parents=True)

        
        while True:
            try:

                if file_path.exists() and base_dir.exists() and file_path.is_dir():
                    

                    # CREATE AND OPEN PATH
                    path = file_path / "workers_info.json"

                    with open(path, "w") as file:
                        

                        # SET BACKGROUND THREAD STATUS
                        data = {
                            "latency": json_push
                        }

                        json.dump(data, file, indent=2)
                        break



                else:
                        
                        # CREATE BASE DIR
                        base_dir.mkdir(exist_ok=True, parents=True)

                        
                        # CREATE THE ATTACK LOG DIR
                        file_path.mkdir(exist_ok=True, parents=True)

                        console.print("\n[bold green]Successfully Recreated Static Directories")
            

            
            # CATCH JSON ERRORS
            except json.JSONDecodeError as e:
                console.print(f"JSON DECODE Error: {e}")

                # CREATE AND OPEN PATH
                path = file_path / "workers_info.json"

                with open(path, "w") as file:
                    

                    # SET BACKGROUND THREAD STATUS
                    data = {
                        "latency": json_push
                    }

                    json.dump(data, file, indent=2)
                    break


                

            except Exception as e:
                console.print("[bold red]NSM_Files Module Push Error: [yellow]",e)
                time.sleep(2)
                break

# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":

    use = 5

    if use == 1:
        File_Handler.background_thread_controller(background_thread_status=True)
        status = File_Handler.background_thread()

        if status:
            console.print("[bold blue]Background Thread:[bold green] Online")
        

        else:
            console.print("[bold blue]Background Thread:[bold red] Offline")

        
    elif use == 2:

        File_Handler.show_attack()


    elif use == 3:
        

        ips = ["192.168.1.164", "192.168.1.1", "192.168.1.220", "192.168.1.111", "192.168.1.57"]

        ips = Network_Scanner.get_subnet()
        threads = []
        net = NetTilities()
  
        
        for ip in ips:
            ip = str(ip)
            console.print(ip)
            
            t = threading.Thread(target=net.pinger, args=(ip, console, 2, True), daemon=True)
            threads.append(t)

        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            


    elif use == 4:
        NetTilities.pinger(target="192.168.1.1", delay=2, status=File_Handler.background_thread)

    

    elif use == 5:
        console.print("using 5")
        

        from concurrent.futures import ThreadPoolExecutor as executor

        ips = Network_Scanner.get_subnet()
        net = NetTilities()
  
        
        for ip in ips:
            ip = str(ip)
            console.print(ip)
            
            


 
        with executor(max_workers=50, thread_name_prefix="nsm", initializer=net.pinger, initargs=(ips, console, 2, True)) as x:
            executor.submit(fn=net.pinger)
        
        console.print("using y")

