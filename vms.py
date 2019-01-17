#!/usr/bin/python
# coding:utf8

import csv
from err import *


class Vms:
	def __init__(self):
		self.vms = []

	def fromCSV(self,path):
		with open(path,"r") as fh:
			reader = csv.reader(fh)
			_ = next(reader) # skip CSV Header
			for row in reader:
				self.vms.append(Vm(row[0],row[1],row[2],row[3],row[4]))
			return self
	
	def sortByCPU(self):
		self.vms.sort(key=lambda x: x.numCPU * 10 if x.affinity else 1 ,reverse=True)
		return self
	
	def sortByMem(self):
		self.vms.sort(key=lambda x: x.memMB * 10 if x.affinity else 1 ,reverse=True)
		return self

	def dump(self):
		return "".join(map(lambda x: x.dump(), self.vms ))
	
	def show(self,vmhostname):
		return "".join(map(lambda x: x.show(vmhostname) , self.vms ) )

class Vm:
	def __init__(self,name,numCPU,memMB,os,vmhost):
		self.name = name
		self.numCPU = int(numCPU)
		self.memMB = int(memMB)
		self.os = os
		self.vmhost = vmhost

	def affinity(self):
		return self.vmhost != ""

	def dump(self):
		return "{0}:{1},{2},{3}\n".format(self.name,self.numCPU,self.memMB,self.os)
	
	def show(self,vmhostname):
		return "{0},{1},{2},{3}\n".format(self.name,vmhostname,self.numCPU,self.memMB)
