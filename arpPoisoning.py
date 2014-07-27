#encoding: UTF-8
import threading
import subprocess
import time
import os

class ArpPoisoning(threading.Thread):
	def __init__(self, activeMin, checkPeriod, ipAddress, mask):
		self.activeSec = activeMin*60
		self.checkPeriod = checkPeriod
		self.infoThread = None #Diccionari de hosts {192.168.1.1: On, 192.168.1.2: Off}
		self.stop = False
		self.hostsList = []
		self.ipAddress = ipAddress
		self.mask = mask

	def run(self):
		tempsPeriode = time.time() + self.checkPeriod
		while self.stop:
			if self.activeSec < time.time(): #El temps ha passat el limit
				break

			if tempsPeriode <= time.time():
				
				tempsPeriode = time.time() + self.checkPeriod

	def stopThread(self):
		"""Aquest mètode atura la defença contra atacs de ARP Poisoning"""
		self.stop = True

	def changeMaskFormat(mask):
		"""Aquest mètode donat una mascara (1-32) retorna una llista amb format dotted quad
		Ex: si la mascara és de 24 retorna [255,255,255,0]"""
		maskDottedQuad = []
		maskBin = ''
		x = 0
		#Ex: mask = 25 vol dir que hi ha 25 "1" a la mascara.
		#En aquest apartat es crea una string amb tants "1" com indiqui la mascara.
		#En cas que la mascara no sigui de 32 bits s'afageix 0 al final per omplir 32 bits
		# mask = 25 --> [11111111, 11111111, 11111111, 100000000] --> [255, 255, 255, 255, 128]	
		while x < 32:
			if mask > 0:
				maskBin = maskBin + '1'
				mask-=1
			else:
				maskBin = maskBin + '0'
			
			x+=1
			if x%8 == 0:
				maskInt = int(maskBin,2)
				maskBin = ''
				maskDottedQuad.append(maskInt)

		return maskDottedQuad

	

	def getHostsList(self):
		rangHosts = 32 - self.mask
		


