import explorer as EXP
import sys
import argparse


parser = argparse.ArgumentParser()
   
parser.add_argument('-n', '--network', metavar = 'Matrix_filename', help="Input network file", default=None, required = True)
parser.add_argument('-c', '--create', action='store_true', help="create network", default=None)
parser.add_argument('-p', '--password', action='store_true', help="change pasword", default=None)
parser.add_argument('-m', '--ssh_config', action='store_true', help="configure ssh access", default=None)
parser.add_argument('-l', '--login', action='store_true', help="Login using default passwd", default=None)
parser.add_argument('-d', '--dhclient', action='store_true', help="run dhclient on ma1", default=None)
parser.add_argument('-r', '--commands', metavar = "'comands'", help="run command on linux", default=None)
parser.add_argument('-f', '--flush', action='store_true', help="flush all interfaces", default=None)
parser.add_argument('-s', '--show', action='store_true', help="show ip address of ma1", default=None)

args = parser.parse_args()
vms, networks = EXP.setup(args.network)

if args.create is not None:
    EXP.create_networks(vms, networks)

if args.commands is not None:
    # commands= ['spyder start bgp']
    EXP.run_commands(vms, args.commands)

if args.password is not None:
    EXP.change_password(vms)

if args.ssh_config is not None:
    EXP.config_ssh(vms)

if args.login is not None:
    EXP.login(vms)

if args.dhclient is not None:
    EXP.dhclient_mgmt_intf(vms)

if args.flush is not None:
    EXP.flush_interfaces(vms, networks)

if args.show is not None:
    EXP.show_ip_mgmt(vms)
