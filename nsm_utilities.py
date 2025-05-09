# THIS MODULE IS RESPONSIBLE FOR HOUSING REUSUABLE CODE ALSO KNOW AS THE UTILITIES MODULE


# UI IMPORTS
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
import pyfiglet
monsole = Console()


stream_on_twitch = "software and game development"


# NSM MODULE IMPORTS



# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import ARP, ICMP, sendp, conf,  IP, sr1, Ether


# ETC IMPORTS
import threading, requests, time, random, os, pyttsx3
from plyer import notification
LOCK = threading.Lock()



# FILE IMPORTS
from pathlib import Path
import json




class Utilities():
    """This will be responsible for holding reusuable logic"""

    def __init__(self):
        pass


    @staticmethod
    def clear_screen():
        """This will be used to clear the users screen"""
        

        try:

            # WINDOWS
            if os.name == "nt":
                os.system("cls")
            
            # UNIX / LINUX
            elif os.name == "posix":
                os.system("clear")

            
            else:
                console.print("[yellow]Invalid platform for the use of clear or cls")
    

        except Exception as e:
            console.print(e)
    

    @staticmethod
    def notify(msg, timeout: int = 10) -> str:
        """This will be responsible for giving user notifications pop up"""


        # DO A OS CHECK SINCE UNIX SOMETIMES ISNT SUPPORTED

        try:

            notification.notify(
                title = "NetBooter 2.0",
                app_name = "NetBooter 2.0",
                message = msg,
                timeout = timeout
            )


        except Exception as e:
            console.print(e)
    

    
    @staticmethod
    def tts(tts, voice_rate = 20, thread = False):
        """This method will be responsible for outputing voice through user speakers"""


        try:

            engine = pyttsx3.init()

            rate = engine.getProperty('rate')
            voices = engine.getProperty('voices')


            # SET VOICE RATE
            engine.setProperty('rate', rate - voice_rate)
            
            
            # THIS WILL AUTOMATICALLY CHOOSE THE SECOND VOICE IF NOT THE FIRST
            if len(voices) > 0:
                engine.setProperty('voice', voices[1].id)
            
            else:
                engine.setProperty('voice', voices[0].id)

            
            # USE THE THREADER IF UR USING MULTIPLE THREADS
            if thread:
                
                with thread:
                    engine.say(tts)
                    engine.runAndWait()
            
            # IF THERE IS NO THREAD DEFINED
            else:
                engine.say(tts)
                engine.runAndWait()

        
        except Exception as e:
            console.print(e)



class NetTilities():
    """Network specific utilities"""

    def __init__(self):
        self.use_voice = True
        self.lock = LOCK
  
    



    # @staticmethod
    def pinger(self, target:str, console=monsole, delay = 0, status = bool):
        """This method will be responsible for constantly pining the target and reporting back its latency"""
        

        # IMPORT DYNAMIC JSON FILE
        from nsm_files import File_Handler


        # BEGIN         
        while File_Handler.background_thread():
        
            # SEND AND RECIEVE THE ICMP PACKET
            with self.lock:
                ping = IP(dst=target) / ICMP() 

            
                if File_Handler.background_thread():            
                    
                    # CATCH ERRORS
                    try:

                        # START TIMER

                        time_start = time.time()

                        
                        latency = sr1(ping, verbose=False)
                        

                        # COUNT THE TIME IT TOOK TO RECIEVE BACK A PACKET
                        time_total =  time.time() - time_start



                        # UPDATE JSON VALUE
                        File_Handler.background_thread_push_info(json_push=str(time_total), console=console)   
                        
                        use = False

                        if use:
                            # PRINT OUTPUT
                            console.print(f"Latency: {time_total:.3f}  -->  {latency}")
                        
                        time.sleep(delay)
                    
                    except Exception as e:
                        console.print(e)
                        time.sleep(3)

        
    

    
    def get_conn_status(self):
        """This method is used to see if the user is online or not"""

        
        while True:
            
            url = "https://www.google.com"
            

            try:
                response = requests.get(url=url, timeout=5)
                

                # IF THE USRE IS ONLINE
                if response.status_code == 200:
                    

                    # NOTIFICATION AND VOICE NOTY
                    if self.use_voice:
                        Utilities.notify(msg="Connection Status: Online")
                        threading.Thread(target=Utilities.tts, args=("Connection Status online, Welcome to NetBooter 2.0", ), daemon=True).start()
                        self.use_voice = False
                    break

                
                # IF WE GET A ELSE MOST LIKELY ERROR INSTEAD THOUGH
                else:

                    # CONNECTION OFFLINE PANEL
                    panel_off = Panel("[bold red]Connection Status: [yellow]Offline", style="bold red", border_style="bold red")
                    monsole.print(panel_off)


                    monsole.input("\n\nPress [bold green]Enter to Re-Try or [yellow]Ctrl + C to [bold red]exit: ")
            


            except (requests.ConnectionError, requests.JSONDecodeError ) as e:
                    panel_off = Panel("[bold red]Connection Status: [yellow]Offline", style="bold red", border_style="bold red")
                    monsole.print(panel_off)


                    monsole.input("\n\nPress [bold green]Enter to Re-Try or [yellow]Ctrl + C to [bold red]exit: ")

            
            except Exception as e:
                monsole.print(f"[bold red]Exception Error:[yellow] {e}")


        
t = 0

# THIS IS STRICTLY FOR MODULE TESTING ONLY
if __name__ == "__main__":
    
    while t < 4:

        NetTilities.pinger(target=socket.gethostbyname("google.com"))
        t += 1


