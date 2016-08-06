# import commands

a= '''
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
          RX packets:1531 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2369 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:129006 (125.9 KiB)  TX bytes:184104 (179.7 KiB)
          Interrupt:160

eth1      Link encap:Ethernet  HWaddr 00:16:3E:00:3D:6E
          inet addr:115.29.51.8  Bcast:115.29.51.255  Mask:255.255.252.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:65866 errors:0 dropped:0 overruns:0 frame:0
          TX packets:49775 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:52401128 (49.9 MiB)  TX bytes:4967933 (4.7 MiB)
          Interrupt:159

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:435 errors:0 dropped:0 overruns:0 frame:0
          TX packets:435 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:48190 (47.0 KiB)  TX bytes:48190 (47.0 KiB)
'''
b = '''
docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.240.0  broadcast 0.0.0.0
        ether 02:42:c4:18:a8:74  txqueuelen 0  (Ethernet)
        RX packets 74632  bytes 10339870 (9.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 91846  bytes 85242802 (81.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.169.101.36  netmask 255.255.248.0  broadcast 10.169.103.255
        ether 00:16:3e:02:2b:88  txqueuelen 1000  (Ethernet)
        RX packets 139117  bytes 194083227 (185.0 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 33536  bytes 2313579 (2.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 120.24.78.206  netmask 255.255.252.0  broadcast 120.24.79.255
        ether 00:16:3e:02:1b:e6  txqueuelen 1000  (Ethernet)
        RX packets 304105  bytes 367273658 (350.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 136589  bytes 19922812 (18.9 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 0  (Local Loopback)
        RX packets 1524  bytes 191691 (187.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1524  bytes 191691 (187.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

veth1b24be0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether e2:e9:d6:86:23:09  txqueuelen 0  (Ethernet)
        RX packets 8  bytes 648 (648.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 17  bytes 1262 (1.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

veth2b69db2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether ee:7b:2e:61:13:9d  txqueuelen 0  (Ethernet)
        RX packets 8  bytes 648 (648.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 22  bytes 1680 (1.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

veth7a5a7cd: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether 96:c4:79:9a:32:fd  txqueuelen 0  (Ethernet)
        RX packets 10454  bytes 1263447 (1.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 16606  bytes 17945262 (17.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vethc311504: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether c6:50:0a:6b:b8:92  txqueuelen 0  (Ethernet)
        RX packets 17168  bytes 1613373 (1.5 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 22969  bytes 18615272 (17.7 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vethd3ce2a1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        ether 3a:7f:2e:64:80:19  txqueuelen 0  (Ethernet)
        RX packets 38377  bytes 7920052 (7.5 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 32392  bytes 19027080 (18.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
'''
def nicinfo():
    # raw_data = commands.getoutput("ifconfig -a")
    raw_data = a
    raw_data= raw_data.split("\n")
    nic_dic = {}
    next_ip_line = False
    last_mac_addr = None
    for line in raw_data:
        if next_ip_line:
            next_ip_line = False
            nic_name = last_mac_addr.split()[0]
            mac_addr = last_mac_addr.split("HWaddr")[1].strip()
            raw_ip_addr = line.split("inet addr:")
            raw_bcast = line.split("Bcast:")
            raw_netmask = line.split("Mask:")
            if len(raw_ip_addr) > 1:
                ip_addr = raw_ip_addr[1].split()[0]
                network = raw_bcast[1].split()[0]
                netmask =raw_netmask[1].split()[0]
            else:
                ip_addr = None
                network = None
                netmask = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {'name': nic_name,
                                     'macaddress': mac_addr,
                                     'netmask': netmask,
                                     'network': network,
                                     'bonding': 0,
                                     'model': 'unknown',
                                     'ipaddress': ip_addr,
                                     }
            else:
                if '%s_bonding_addr' %(mac_addr) not in nic_dic:
                    random_mac_addr = '%s_bonding_addr' %(mac_addr)
                else:
                    random_mac_addr = '%s_bonding_addr2' %(mac_addr)

                nic_dic[random_mac_addr] = {'name': nic_name,
                                     'macaddress':random_mac_addr,
                                     'netmask': netmask,
                                     'network': network,
                                     'bonding': 1,
                                     'model': 'unknown',
                                     'ipaddress': ip_addr,
                                     }
        if "HWaddr" in line:
            next_ip_line = True
            last_mac_addr = line
        nic_list= []
        for k,v in nic_dic.items():
            nic_list.append(v)
        return {'nic':nic_list}
print (nicinfo())