#!/usr/bin/python
# coding:utf8

# vmhost
# vm

from vmhosts import *
from constraints import *
from vms import *
from err import *

def main():
	c = Constraints()
	c.add("failoverhosts",Constraint(constraintFailoverhost()))
	c.add("windowsLimit",Constraint(constraintWindowsLimit(2)))
	vmhosts = VmHosts(c)
	vmhosts.fromCSV("data/vmhosts.csv")

	vms = Vms()
	vms.fromCSV("data/vms.csv")
	

	for vm in vms.vms:
		err( "-" * 20 )
		err( "add:" , vm.name )
		err( vmhosts.dump() )
		ret = vmhosts.addVm(vm,"mem")
		if ret == False:
			err("**************** error **************** ")
		else:
			err( "put:",ret.name )
	vmhosts.sortByName()
	print vmhosts.showVmHosts()
	print "-----------------------------------------"
	print vmhosts.showVms()
	return


main()

