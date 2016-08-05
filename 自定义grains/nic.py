#!/usr/bin/env python3
#coding:utf8
import subprocess
import re
a = '''
docker0   Link encap:Ethernet  HWaddr 4A:A3:0C:97:E9:11
          inet addr:192.168.42.1  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)

eth0      Link encap:Ethernet  HWaddr 00:16:3E:00:3E:B2
          inet addr:10.161.73.26  Bcast:10.161.79.255  Mask:255.255.240.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6038 errors:0 dropped:0 overruns:0 frame:0
          TX packets:10600 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:416081 (406.3 KiB)  TX bytes:785911 (767.4 KiB)
          Interrupt:160

eth1      Link encap:Ethernet  HWaddr 00:16:3E:00:3D:6E
          inet addr:115.29.51.8  Bcast:115.29.51.255  Mask:255.255.252.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:394883 errors:0 dropped:0 overruns:0 frame:0
          TX packets:311868 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:239416825 (228.3 MiB)  TX bytes:59972181 (57.1 MiB)
          Interrupt:159

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:13310 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13310 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1712346 (1.6 MiB)  TX bytes:1712346 (1.6 MiB)
'''
def get_ipinfo(data):
    data = (i for i in data.split('\n\n') if i and not i.startswith('lo'))
    ip_info = []
    ifname = re.compile(r'(eth[\d:]*|wlan[\d:]*|dock[\w:]*)')
    ipaddr = re.compile(r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})(\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]{1,2})){3}')
    macaddr = re.compile(r'[A-F0-9a-f:]{17}')
    netmask = re.compile(r'[A-F0-9a-f:]{17}')
    for i in data:
        x = {}
        if ifname.match(i):
            device = ifname.match(i).group()
            x['Adapter'] = device
        if macaddr.search(i):
            mac = macaddr.search(i).group()
            x['MAC'] = mac
        if ipaddr.search(i):
            ip = ipaddr.search(i).group()
            x['IP'] = ip
        else:
            x['IP'] = None
        ip_info.append(x)
    return ip_info
print(get_ipinfo(a))