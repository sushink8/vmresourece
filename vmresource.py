#!/usr/bin/python
# coding:utf8

# vmhost
# vm

from vmhosts import *
from constraints import *
from vms import *
from err import *
import argparse

def main():
	args = option()
	c = Constraints()
	c.add("failoverhosts",Constraint(constraintFailoverhost()))
	c.add("windowsLimit",Constraint(constraintWindowsLimit(2)))
	vmhosts = VmHosts(c)
	vmhosts.fromCSV(args.host)

	vms = Vms()
	vms.fromCSV(args.machine)
	vms.sortByCPU()
	

	for vm in vms.vms:
		err( "-" * 20 )
		err( "add:" , vm.name )
		err( vmhosts.dump() )
		ret = vmhosts.addVm(vm,"mem")
		if ret == False:
			sys.stderr.write("### {0} error !\n".format(vm.name) )
		else:
			err( "put:",ret.name )
	vmhosts.sortByName()
	print vmhosts.showVmHosts()
	print "-----------------------------------------"
	print vmhosts.showVms()
	return

def option():
	parser = argparse.ArgumentParser(description="virtual machine resource palnning mini tool")
	parser.add_argument("-m" , "--machine" , type=str , help="virtual machine csv file path" )
	parser.add_argument("-H" , "--host" , type=str , help="host csv file path")
	return parser.parse_args()

main()
