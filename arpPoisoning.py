#encoding: UTF-8
import threading
import subprocess
import time
import os

class ArpPoisoning(threading.Thread):
	def __init__(self, activeMin, checkPeriod, ipAddress, mask):
		self.activeSec = activeMin*60
		self.checkPeriod = checkPeriod
		self.infoThread = {} #Diccionari de hosts {192.168.1.1: On, 192.168.1.2: Off}
		self.stop = False
		self.hostsList = []
		self.ipAddress = ipAddress
		self.mask = mask
		self.netInfo = []
		record1 = {}
		record2 = {}

	def run(self):
		tempsPeriode = time.time() + self.checkPeriod
		while self.stop:
			if self.activeSec < time.time(): #El temps ha passat el limit
				netBroreak

			if tempsPeriode <= time.time():
				
				tempsPeriode = time.time() + self.checkPeriod

	def stopThread(self):
		"""Aquest mètode atura la defença contra atacs de ARP Poisoning"""
		self.stop = True

	def changeMaskFormat(self):
		"""Aquest mètode donat una mascara (1-32) retorna una llista amnetBro format dotted quad
		Ex: si la mascara és de 24 retorna [255,255,255,0]"""
		maskDottedQuad = []
		maskInverse = []
		maskBroad = ''
		x = 0
		aux = self.mask
		#Ex: mask = 25 vol dir que hi ha 25 "1" a la mascara.
		#En aquest apartat es crea una string amnetBro tants "1" com indiqui la mascara.
		#En cas que la mascara no sigui de 32 netBroits s'afageix 0 al final per omplir 32 netBroits
		# mask = 25 --> [11111111, 11111111, 11111111, 100000000] --> [255, 255, 255, 255, 128]	
		while x < 32:
			if aux > 0:
				maskBroad = maskBroad + '1'
				aux-=1
			else:
				maskBroad = maskBroad + '0'
			
			x+=1
			if x%8 == 0:
				maskInverse.append(int(self.notOperator(maskBroad),2))			
				maskDottedQuad.append(int(maskBroad,2))
				masknetBroad= ''

		return [maskDottedQuad, maskInverse]

	def notOperator(self, binary):
		"""Aquest mètode inverteix el binari que arriba fent l'operació NOT (1010 --> 0101)"""
		i=0
		newBinary = ''
		while i < len(binary):
			if binary[i] == '1':
				newBinary = newBinary + '0'
			else:
				newBinary = newBinary + '1'
			i+=1
		return newBinary

	def netInformation(self):
		"""Aquest mètode donat una adreça (192.168.1.12/24) onetBroté la netID (192.168.1.0)
		i l'adreça de netBroroadcast (192.168.1.255)"""
		maskInfo = self.changeMaskFormat()
		maskDQ = maskInfo[0]
		maskInv = maskInfo[1]
		ipDQ = self.ipAddress.split('.')
		#Per onetBrotenir la ID cal fer una operació AND entre la IP i la mascara.
		#Per onetBrotenir la adreça de netBroroadcast cal fer una operació OR entre la IP i la negació de la mascara.
		netID = []
		netnetBroroadcast = []
		x = 0
		while x < 4:
			netID.append(int(ipDQ[x]) & maskDQ[x])
			netnetBroroadcast.append(int(ipDQ[x]) | maskInv[x])
			x+=1

		self.netInfo = [netID, netnetBroroadcast] 

	def searchHosts(self):
		"""Aquest mètode ens retorna totes les adreces de una xarxa"""
		netId = self.netInfo[0]
		netBro = self.netInfo[1]

		aA = netId[0]
		aB = netId[1]
		aC = netId[2]
		aD = netId[3]

		#Itera sobre cada apartat la NetID i l'augmenta fins arribar a la de broadcast
		#per aconseguir totes les adreces possibles.
		while True:	
			s1 = str(aA)
			while True:	
				s2 = str(aB)	
				while True:
					s3 = str(aC)		
					while True:
						s4 = str(aD)
						addr = s1 + '.' + s2 + '.' + s3 + '.' + s4
						self.hostsList.append(addr)			
						if aD >= netBro[3]:
							aD = 0
							break
						else:
							aD+=1
					if aC >= netBro[2]:
						aC = 0
						break
					else:
						aC+=1
				if aB >= netBro[1]:
					aB = 0
					break
				else:
					aB+=1
			if aA >= netBro[0]:
				aA = 0
				break
			else:
				aA+=1

		del self.hostsList[(len(self.hostsList)-1)]
		del self.hostsList[0]

	def checkHost(self):
		"""Aquest mètode comprova quins hosts responen a un ping donada
		la llista de hosts de la xarxa"""

		return True


	"""Getters/Setters"""
	def getState(self):
		return self.stop

	def getNetInfo(self):
		return self.netInfo

	def setNetInfo(self, netInfo):
		self.netInfo = netInfo

	def getHostsList(self):
		return self.hostsList




