#!/usr/bin/env python3
#coding:utf8
def diskinfo():
    result = {'physical_disk_driver':[]}
    try:
        script_path = os.path.dirname(os.path.abspath(__file__))
        shell_command = "%s/MegaCli  -PDList -aALL" % script_path
        output = commands.getstatusoutput(shell_command)
        if 'Exit Code: 0x00' in  output[1]:
            '''
            '''
            capacity = commands.getstatusoutput("xvda 40G")[1]
            disk_info = []
            capacity = capacity.split('\n')
            for i in capacity:
                disk_info.append({'slot':i.split()[0]})
                tmp_size = i.split()[1]
                if 'G' in tmp_size:
                    disk_info[capacity.index(i)]['capacity'] = int(tmp_size[0:-1])
                elif 'M' in tmp_size:
                    tmp_GB_size = "%.2f" %(int(tmp_size[0:-1])/1000.0)
                    print(tmp_GB_size)
                    disk_info[capacity.index(i)]['capacity'] = float(tmp_GB_size)
                elif 'T' in tmp_size:
                    disk_info[capacity.index(i)]['capacity'] = float(tmp_size[0:-1])*1000
            result['physical_disk_driver'] = disk_info
        else:
            result['physical_disk_driver'] = self.parse(output[1])
    except Exception as e:
        result['error'] = e
    print('result',result['physical_disk_driver'])
    return result
print (diskinfo())