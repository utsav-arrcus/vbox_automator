import virtualbox
from virtualbox.library import NetworkAttachmentType
import re, sys, time, csv


def fetch_topology(filename):
    with open(filename, 'r') as csvfile:
        topology_data = list(csv.reader(csvfile))
        vm_names = topology_data[0][1:]
    return vm_names, topology_data

def fetch_networks(vm_names, topology):
    topo_networks = {}
    for row in topology[1:]:
        for i in range(1, len(row[1:])):
            if int(row[i]) > 0:
                net_name = '_'.join(sorted([row[0], vm_names[i-1]]))
                topo_networks[net_name] = int(row[i])
                net_name
    networks = {}
    for vm in vm_names:
        networks[vm] = []
        for net_name in topo_networks.keys():
            if vm in net_name:
                for i in range(topo_networks[net_name]):
                    networks[vm].append("{}_{}".format(net_name, i))
    return networks

def fetch_req_vms(vm_names, all_machines):
    interested_vms = []
    for machine in all_machines:
        if machine.name in vm_names:
            interested_vms.append(machine)
    return interested_vms

def create_networks(vms, networks):
    for vm_name in networks.keys():
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        for i, network in enumerate(networks[vm_name]):
            adapter = session.machine.get_network_adapter(i+1)
            adapter.attachment_type = NetworkAttachmentType.internal
            adapter.enabled = True
            adapter.internal_network = network
        session.machine.save_settings()

def flush_interfaces(vms, networks):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        for i, interface in enumerate(networks[a]):
        	session.console.keyboard.put_keys("\n ip a flush swp"+str(i+1)+" \n")
        session.console.keyboard.put_keys("\n ip a flush loopback0\n")


def change_password(vms):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        session.console.keyboard.put_keys("\nroot\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("YouReallyNeedToChangeThis\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("passwd\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("arrcus\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("arrcus\n")
        time.sleep(0.2)

def config_ssh(vms):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        session.console.keyboard.put_keys("arcos_cli\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("config\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("system ssh-server enable true\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("system ssh-server permit-root-login true\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("system aaa authentication admin-user admin-password arrcus\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("commit\n")        
        time.sleep(0.2)
        session.console.keyboard.put_keys("exit\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("show running-config system | display xml | save /var/confd/cdb/ztp.xml\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("exit\n")
        time.sleep(0.2)
		
def login(vms):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        session.console.keyboard.put_keys("\nroot\n")
        time.sleep(0.2)
        session.console.keyboard.put_keys("arrcus\n")        
        time.sleep(0.2)


def show_ip_mgmt(vms):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        # session.console.keyboard.put_keys("exit\n")
        session.console.keyboard.put_keys("\n ip a show ma1\n")
        time.sleep(0.2)


def dhclient_mgmt_intf(vms):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        # session.console.keyboard.put_keys("exit\n")
        session.console.keyboard.put_keys("\n sudo dhclient ma1\n")
        time.sleep(0.2)



def run_commands(vms, commands):
    for vm_name in vms:
        a = str(vm_name)
        vbox = virtualbox.VirtualBox()
        machine = vbox.find_machine(a)
        session = machine.create_session()
        # session.console.keyboard.put_keys("exit\n")
        session.console.keyboard.put_keys(commands+'\n')
        time.sleep(0.2)

def setup(network_matrix):
    vbox = virtualbox.VirtualBox()
    all_machines = vbox.machines
    vm_names, topology_matrix = fetch_topology(network_matrix)
    vms = fetch_req_vms(vm_names, all_machines)
    networks = fetch_networks(vm_names, topology_matrix)
    return vms, networks