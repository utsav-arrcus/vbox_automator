import virtualbox
from virtualbox.library import NetworkAttachmentType
import re, sys, time


def fetch_topology(filename):
    with open(filename, 'r') as filedata:
        topology = filedata.read()
    header = topology.split('\n')[0].split(',')[1]
    m = re.search('(.*)_(\d+)$', header)
    header = m.group(1)
    return topology, header

def fetch_networks(topology):
	networks = {}
	rows = topology.split('\n')
	header = rows[0]
	header = header.split(',')
	rows = rows[1:]
	for row in rows:
		vals = row.split(',')
		
		networks[vals[0]] = []
		for i, val in enumerate(vals[1:]):
			for j in range(0, int(val)):
				vms = sorted([vals[0], header[i+1]])
				networks[vals[0]].append(vms[0]+'_'+vms[1])
	return networks

def fetch_req_vms(header, all_machines):
	interested_vms = []
	for machine in all_machines:
		m = re.match(header+'_\d+', machine.name)
		if m is not None:
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
    topology, header = fetch_topology(network_matrix)
    vms = fetch_req_vms(header, all_machines)
    networks = fetch_networks(topology)
    return vms, networks
