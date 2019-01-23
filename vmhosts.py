#!/usr/bin/python
# coding:utf8

import csv
from err import *


class VmHost:
	def __init__(self,name,numCPU,memMB,constraints):
		self.name = name
		self.numCPU = int(numCPU)
		self.memMB = int(memMB)
		self.constraints = constraints

		self.vms = []
	
	def addVm(self,vm):
		if self.freeNumCPU() < vm.numCPU:
			return False
		if self.freeMemMB() < vm.memMB:
			return False
		self.vms.append(vm)
		return self
	
	def sumNumCPU(self):
		acc = 0
		for vm in self.vms:
			acc += vm.numCPU
		return acc

	def freeNumCPU(self):
		return self.numCPU - self.sumNumCPU()

	def sumMemMB(self):
		acc = 0
		for vm in self.vms:
			acc += vm.memMB
		return acc
	
	def freeMemMB(self):
		return self.memMB - self.sumMemMB()

	def countOS(self,os):
		acc = 0
		for vm in self.vms:
			if vm.os == os:
				acc += 1
		return acc

	def dump(self):
		s = ""
		s += "{0}: {1},{2},{3}\n".format(self.name,self.freeNumCPU(),self.freeMemMB(),",".join(self.constraints.keys()))
		s += "".join( map( lambda x: "\t"+x.dump() , self.vms)) + "\n"
		return s
	
	def showVmHosts(self):
		return "{0},{1}/{2},{3}/{4}\n".format(self.name, self.sumNumCPU() , self.numCPU , self.sumMemMB(), self.memMB )

	def showVms(self):
		return "".join(map(lambda x: x.show(self.name) , self.vms) )

class VmHosts:
	def __init__(self,constraints):
		self.vmhosts = []
		self.constraints = constraints

	def fromCSV(self,path):
		with open(path,"r") as fh:
			reader = csv.reader(fh)
			_ = next(reader) # skip CSV Header
			for row in reader:
				self.vmhosts.append(VmHost(row[0],row[1],row[2],self.constraints.get(row[3:])))
		return self

	def choiceLargestFreeCPUVmHost(self):
		freeCPU = 0
		returnVMhost = None
		for i,vmhost in enumerate(self.vmhosts):
			f = vmhost.freeNumCPU()
			if freeCPU < f:
				freeCPU = f
				returnVMhost = vmhost
				continue
		return returnVMhost

	def choiceLargestFreeMemVmHost(self):
		freeMem = 0
		returnVMhost = None
		for i,vmhost in enumerate(self.vmhosts):
			m = vmhost.freeMemMB()
			if freeMem < m:
				freeMem = m
				returnVMhost = vmhost
				continue
		return returnVMhost

	def sortByFreeCPU(self):
		self.vmhosts.sort(key=lambda x: x.freeNumCPU(),reverse=True)
		return self

	def sortByFreeMem(self):
		self.vmhosts.sort(key=lambda x: x.freeMemMB(),reverse=True)
		return self
	
	def sortByName(self):
		self.vmhosts.sort(key=lambda x: x.name)
		return self
		
	def addVm(self,vm,sortKey):
		if sortKey == "cpu":
			self.sortByFreeCPU()
		elif sortKey == "mem":
			self.sortByFreeMem()

		# check affinity
		for vmhost in self.vmhosts:
			if vm.vmhost == vmhost.name:
				return vmhost.addVm(vm)

		# check constraints / resource
		for i,vmhost in enumerate(self.vmhosts):
			if vmhost.constraints.violated(vmhost,vm) :
				continue
			else:
				ret = vmhost.addVm(vm)
				if ret == False:
					continue
				return ret
		return False

	def dump(self):
		return "".join( map( lambda x: x.dump() , self.vmhosts ) ) 

	def showVmHosts(self):
		return "".join(map(lambda x: x.showVmHosts() , self.vmhosts ) )

	def showVms(self):
		return "".join(map(lambda x: x.showVms() , self.vmhosts) )
	
