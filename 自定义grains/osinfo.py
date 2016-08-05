import commands
def osinfo():
    distributor = commands.getoutput(" lsb_release -a|grep 'Distributor ID'").split(":")
    release  = commands.getoutput(" lsb_release -a|grep Description").split(":")
    data_dic ={
        "os_distribution": distributor[1].strip() if len(distributor)>1 else None,
        "os_release":release[1].strip() if len(release)>1 else None,
        "os_type": "linux",
    }
    return data_dic

