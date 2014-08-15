#encoding: UTF-8
import threading
import subprocess
import time

class NeighborSpoofing(threading.Thread):
	def __init__(self, activeMin, checkPeriod):
		self.activeSec = activeMin * 60
		self.checkPeriod = checkPeriod
		self.stop = True
		self.neighborRecord = {}
		self.infoThread = []

	def run(self):
		"""Aquest programa arrenca la defença contra atacs de Neighbor Spoofing.
		El mètode s'executa durant el temps que l'usuari ha introduit (activeTime) 
		o fins que el pari."""
		tempsPeriode = time.time() + self.checkPeriod
		while self.stop:
			if self.activeSec < time.time(): #El temps ha passat el limit
				break

			if tempsPeriode <= time.time():
				self.getNeighborTable()
				self.infoThread = self.checkNeighborSpoofing()
				tempsPeriode = time.time() + self.checkPeriod

	def stopThread(self):
		"""Aquest mètode atura la defença contra atacs de Neighbor Spoofing"""
		self.stop = False
	
	def getNeighborTable(self):
		"""Aquest mètode obté la taula de Neighbors"""
		commandInp = subprocess.Popen(["ip", "-6", "n", "s"], stdout=subprocess.PIPE)
		commandOut = commandInp.communicate()[0]

		#Modifiquem el resultat de la comanda per poder introdur en un diccionari, tal com es fa a ARP Spoofing.
		split1 = commandOut.split('\n')
		split1.remove('')

		for line in split1:
			split2 = line.split(' ')
			ip = split2[0]
			mac = split2[4]
			self.neighborRecord[ip] = mac

	def checkNeighborSpoofing(self):
		"""Aquest mètode comprova si hi ha un possible atac de Neighbor Spoofing"""
		hostInfo = []
		for x in self.neighborRecord:
			for y in self.neighborRecord:
				if((y is not x) and (self.neighborRecord[x] == self.neighborRecord[y])):
					info = [x, y, self.neighborRecord[x]]
					hostInfo.append(info)
		
		return hostInfo

	"""Getters/Setters"""
	def getActiveSec(self):
		return self.activeSec

	def setActiveSec(self, activeMin):
		self.activeSec = activeMin * 60

	def getCheckPeriod(self):
		return self.checkPeriod

	def setCheckPeriod(self, checkPeriod):
		self.checkPeriod = checkPeriod

	def getState(self):
		return self.stop

	def getNeighborRecord(self):
		return self.neighborRecord

	def setNeighborRecord(self, record):
		self.neighborRecord = record

	def getInfoThread(self):
		return self.infoThread