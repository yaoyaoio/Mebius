import commands
def collect():
    grains = {}
    filter_keys = ['Manufacturer','Serial Number','Product Name','UUID','Wake-up Type']
    raw_data = {}
    for key in filter_keys:
        try:
            cmd_res = commands.getoutput("sudo dmidecode -t system|grep '%s'" %key)
            cmd_res = cmd_res.strip()

            res_to_list = cmd_res.split(':')
            if len(res_to_list)> 1:
                raw_data[key] = res_to_list[1].strip()
            else:

                raw_data[key] = -1
        except Exception as e:
            print(e)
            raw_data[key] = -2

    grains['asset_type'] = 'server'
    grains['manufactory'] = raw_data['Manufacturer']
    grains['sn'] = raw_data['Serial Number']
    grains['model'] = raw_data['Product Name']
    grains['uuid'] = raw_data['UUID']
    grains['wake_up_type'] = raw_data['Wake-up Type']
    return grains
