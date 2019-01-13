#!/usr/bin/python
# coding:utf8

from err import *


class Constraint:
	def __init__(self,func):
		self.constraint = func
	
	def violated(self,vmhost,vm):
		return self.constraint(vmhost,vm)
	
class Constraints:
	def __init__(self):
		self.constraints = {}

	def add(self,name,constraint):
		self.constraints[name] = constraint

	def get(self,names):
		c = Constraints()
		for name in names:
			c.add(name,self.constraints[name])
		return c

	def keys(self):
		return self.constraints.keys()

	def violated(self,vmhost,vm):
		for n,c in self.constraints.items():
			if c.violated(vmhost,vm) :
				return True
			else:
				continue
		return False
			
# true -> 選択されない
# false -> 選択される可能性あり
def constraintFailoverhost():
	def _constraintFailoverhost(vmhost,vm):
		return True
	return _constraintFailoverhost

def constraintWindowsLimit(oslimit):
	def _constraintWindowsLimit(vmhost,vm):
		os = "windows2016"
		if vm.os != os:
			return False
		c = vmhost.countOS(os)	
		if oslimit < c + 1:
			return True
		return False
	return _constraintWindowsLimit

