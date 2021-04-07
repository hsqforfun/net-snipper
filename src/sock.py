# -*- coding: utf-8 -*-
import socket
import os
import sys


def get_smth():
    routingGateway = netifaces.gateways()["default"][netifaces.AF_INET][0]
    routingNicName = netifaces.gateways()["default"][netifaces.AF_INET][1]

    for interface in netifaces.interfaces():
        if interface == routingNicName:
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0][
                "addr"
            ]
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0][
                    "addr"
                ]
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][
                    0
                ]["netmask"]
            except KeyError:
                pass

    display_format = "%-30s %-20s"
    print(display_format % ("Routing Gateway:", routingGateway))
    print(display_format % ("Routing NIC Name:", routingNicName))
    print(display_format % ("Routing NIC MAC Address:", routingNicMacAddr))
    print(display_format % ("Routing IP Address:", routingIPAddr))
    print(display_format % ("Routing IP Netmask:", routingIPNetmask))
    return routingIPAddr


def sniffing(host, winORlinux, socket_proto):
    while 1:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_proto)
        port = 0
        sniffer.bind((host, port))

        # include the IP headers in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if winORlinux == 1:
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # read in a single packet
        print("Listening ...")
        print(sniffer.recvfrom(65565))
        print("Done.")


def main(host):
    if os.name == "nt":  # windows
        sniffing(host, 1, socket.IPPROTO_IP)  # 0
    else:
        print("Linux : " + host)
        sniffing(host, 0, socket.IPPROTO_ICMP)  # 1


if __name__ == "__main__":
    try:
        import netifaces
    except ImportError:
        try:
            command_to_execute = "pip install netifaces || easy_install netifaces"
            os.system(command_to_execute)
        except OSError:
            print("Can NOT install netifaces, Aborted!")
            sys.exit(1)
        import netifaces
    # host to listen
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)

    ipAddr = get_smth()

    main(ipAddr)
