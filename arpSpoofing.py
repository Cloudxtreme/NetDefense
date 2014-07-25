#encoding: UTF-8
import threading
import subprocess
import time

class ArpSpoofing(threading.Thread):
	def __init__(self, activeMin, checkPeriod):
		self.activeSec = activeMin*60 #Es multiplica per 60 per passar de minuts a segons.
		self.checkPeriod = checkPeriod
		self.stop = False
		self.arpRecord = {}

	def run(self):
		"""Aquest mètode arrenca la defença contra atacs de ARP Spoofing. 
		El mètode s'executa durant el temps que l'usuari ha introduit (activeTime) o fins que el pari."""
		atac = False
		tempsPeriode = time.time() + self.checkPeriod
		while self.stop:
			if self.activeSec < time.time(): #El temps ha passat el limit
				break

			if tempsPeriode <= time.time():
				self.getArpTable()
				atac = self.checkArpSpoofing()
				tempsPeriode = time.time() + self.checkPeriod

	def stopThread(self):
		"""Aquest mètode atura la defença contra atacs de ARP Spoofing"""
		self.stop = True

	def getArpTable(self):
		"""Aquest mètode s'utilitza per obtenir la taula ARP"""
		commandInp = subprocess.Popen(["ip", "n", "s"], stdout=subprocess.PIPE)
		commandOut = commandInp.communicate()[0]

		#Modifiquem el resultat de la comanda per poder introdur en un diccionari.
		split1 = commandOut.split('\n')
		split1.remove('')

		for line in split1:
			split2 = line.split(' ')
			ip = split2[0]
			mac = split2[4]
			self.arpRecord[ip] = mac

	def checkArpSpoofing(self):
		"""Aquest mètode comproba si hi ha un possible atac utilitzant el diccionari"""
		trobat = False
		for x in self.arpRecord:
			for y in self.arpRecord:
				if((y is not x) and (self.arpRecord[x] == self.arpRecord[y])):
					trobat = True
		
		return trobat

	"""Getters/Setters"""
	def setArpRecord(self, arpRecord):
		self.arpRecord = arpRecord

	def getArpRecord(self):
		return self.arpRecord

	def setActiveSec(self, activeMin):
		self.activeSec = activeMin * 60

	def getActiveSec(self):
		return self.activeSec

	def setCheckPeriod(self, checkPeriod):
		self.checkPeriod = checkPeriod

	def getCheckPeriod(self):
		return self.checkPeriod

	def getState(self):
		return self.stop

