import os
import socket
import threading
import time



class IPList:
	def __init__(self):
		self.IP_LIST=[]
		self.MAX_THREAD=500
		self._r_th=0
		self._slt=[]
		self._ipl=[]
		for i in range(1,255):
			self.IP_LIST+=[f"192.168.178.{i}"]



	def _check_one(self):
		if (len(self._slt)==0):
			return
		try:
			self._r_th+=1
			ip=self._slt[0]
			del self._slt[0]
			o=os.popen(f"@echo off&&cd C:\\Windows\\System32\\&&ping {ip} -n 1 -w 100 -l 1").read()
			if (o.split("\n")[2]!="Request timed out." and "Destination host unreachable." not in o.split("\n")[2]):
				self._ipl+=[ip]
			thr=threading.Thread(target=self._check_one,args=(),kwargs={})
			thr.start()
			self._r_th-=1
		except:
			self._r_th-=1



	def check_all(self):
		self._slt=self.IP_LIST[:]
		self._ipl=[]
		for i in range(1,self.MAX_THREAD):
			thr=threading.Thread(target=self._check_one,args=(),kwargs={})
			thr.start()
		while (len(self._slt)>0 or self._r_th>0):
			pass
		return self._ipl



	def check_loop(self):
		while (True):
			ipl=self.check_all()
			ipl.sort()
			os.system("cls")
			print("Active IP's:\n\n"+"\n".join(ipl))



IPList().check_loop()
