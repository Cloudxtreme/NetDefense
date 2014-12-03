#encoding: UTF-8
import subprocess
import time
import os

def changeMaskFormat(mask):
	maskDottedQuad = []
	maskInverse = []
	maskBroad = ''
	x = 0
	# mask = 25 --> [11111111, 11111111, 11111111, 100000000] --> [255, 255, 255, 255, 128]	
	while x < 32:
		if mask > 0:
			maskBroad = maskBroad + '1'
			mask-=1
		else:
			maskBroad = maskBroad + '0'
		
		x+=1
		if x%8 == 0:
			maskInverse.append(int(notOperator(maskBroad),2))			
			maskDottedQuad.append(int(maskBroad,2))
			masknetBroad= ''

	return [maskDottedQuad, maskInverse]

def notOperator(binary):
	# 1010 --> 0101
	i=0
	newBinary = ''
	while i < len(binary):
		if binary[i] == '1':
			newBinary = newBinary + '0'
		else:
			newBinary = newBinary + '1'
		i+=1
	return newBinary

def netInformation(mask, ip):
	# 192.168.1.24, 24 --> 192.168.1.0, 192.168.1.254
	maskInfo = changeMaskFormat(mask)
	maskDQ = maskInfo[0]
	maskInv = maskInfo[1]
	ipDQ = ip.split('.')

	netID = []
	netnetBroroadcast = []
	x = 0
	while x < 4:
		netID.append(int(ipDQ[x]) & maskDQ[x])
		netnetBroroadcast.append(int(ipDQ[x]) | maskInv[x])
		x+=1

	self.netInfo = [netID, netnetBroroadcast]

def searchHosts():
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

def getArpRecord():
	arpTable = {}
	commandInp = subprocess.Popen(["ip", "n", "s"], stdout=subprocess.PIPE)
	commandOut = commandInp.communicate()[0]

	#Modifiquem el resultat de la comanda per poder introdur en un diccionari.
	split1 = commandOut.split('\n')
	split1.remove('')

	for line in split1:
		split2 = line.split(' ')
		ip = split2[0]
		mac = split2[4]
		arpTable[ip] = mac

	return arpTable

def getPingRecord():
	pingTable = {}

	for addr in self.hostsList:
		commandInp = subprocess.Popen(["ping", addr, "-c 1"], stdout=subprocess.PIPE)
		commandOut = commandInp.communicate()[0]
		splitOut = commandOut.split(' ')

		if('100%' in splitOut):
				pingTable[addr] = "OFF"
		else:
				pingTable[addr] = "ON"

	return pingTable

def checkArpPoisoning():
	hostInfo = []

	for rp in self.recordPing1:
		if(self.recordPing1[rp] == "ON" and self.recordPing2[rp] == "OFF"):
			if(self.recordArp1[rp] != self.recordArp2[rp]):
				info = [rp, self.recordArp1[rp], self.recordArp2[rp]]
				hostInfo.append(info)

	return hostInfo

def main():
	recordPing1 = getPingRecord()
	recordArp1 = getArpRecord()

	time_end = time.time() + (duration * 60)
	while(time.time < time_end):
		#Pasos
		recordPing2 =  getPingRecord()
		recordArp2 = getRecordArp()
		checkArpPoisoning()
		time.sleep(frequency)

if __name__ == '__main__':
	main()

"""
class ArpPoisoning(threading.Thread):
    def __init__(self, checkPeriod, ipAddress, mask):
        super(ArpPoisoning, self).__init__()
        self.checkPeriod = checkPeriod
        self.infoThread = []
        self.stop = True
        self.hostsList = []
        self.ipAddress = ipAddress
        self.mask = mask
        self.netInfo = []
        self.recordArp1 = {}
        self.recordArp2 = {}
        self.recordPing1 = {}
        self.recordPing2 = {}

    def run(self):
        self.recordPing1 = self.getPingRecord()  #Recollim la informació inicial de l'estat dels hosts amb el ping
        self.recordArp1 = self.getArpRecord()  #Recollim la informació inciial per comparar adreces MAC amb la taula ARP

        tempsPeriode = time.time() + self.checkPeriod
		while self.stop:
			if tempsPeriode <= time.time():
				self.recordPing2 = self.getPingRecord()
				self.recordArp2 = self.getArpRecord()

				self.infoThread = self.checkArpPoisoning()
				
				tempsPeriode = time.time() + self.checkPeriod

	def stopThread(self):
		#Aquest mètode atura la defença contra atacs de ARP Poisoning
		self.stop = False

	def changeMaskFormat(self):
		#Aquest mètode donat una mascara (1-32) retorna una llista amb format dotted quad
		Ex: si la mascara és de 24 retorna [255,255,255,0]
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
		#Aquest mètode inverteix el binari que arriba fent l'operació NOT (1010 --> 0101)
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
		#Aquest mètode donat una adreça (192.168.1.12/24) obté la netID (192.168.1.0) i l'adreça de netBroroadcast (192.168.1.255)
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
		#Aquest mètode ens retorna totes les adreces de una xarxa
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

	def getArpRecord(self):
		#Aquest mètode retorna la taula ARP
		arpTable = {}
		commandInp = subprocess.Popen(["ip", "n", "s"], stdout=subprocess.PIPE)
		commandOut = commandInp.communicate()[0]

		#Modifiquem el resultat de la comanda per poder introdur en un diccionari.
		split1 = commandOut.split('\n')
		split1.remove('')

		for line in split1:
			split2 = line.split(' ')
			ip = split2[0]
			mac = split2[4]
			arpTable[ip] = mac

		return arpTable

	#ATENCIÓ: Mètode poc eficient, cal millorar la velocitat amb que fer ping.
	def getPingRecord(self):
		#Aquest mètode ping a cada host de la xarxa i retorna un diccionari que 
		indica l'estat de cada host (ON/OFF)
		pingTable = {}

		for addr in self.hostsList:
			commandInp = subprocess.Popen(["ping", addr, "-c 1"], stdout=subprocess.PIPE)
			commandOut = commandInp.communicate()[0]
			splitOut = commandOut.split(' ')

			if('100%' in splitOut):
					pingTable[addr] = "OFF"
			else:
					pingTable[addr] = "ON"

		return pingTable

	def checkArpPoisoning(self):
		#Aquest mètode comprova si hi ha algun host de la subxarxa que no respongui
		#Per a saber si no pot haver communicació amb un host primer es comproba els recordPing (si canvia l'estat de l'anterior record de ON-->OFF)
		#En cas que canvii l'estat es mira si la adreça MAC ha canviat per a saber si s'ha fet l'atac.
		#ATENCIÓ: Aquest atac no es detecta si l'atac ja estava operatiu abans d'activar la protecció.
		hostInfo = []

		for rp in self.recordPing1:
			if(self.recordPing1[rp] == "ON" and self.recordPing2[rp] == "OFF"):
				if(self.recordArp1[rp] != self.recordArp2[rp]):
					info = [rp, self.recordArp1[rp], self.recordArp2[rp]]
					hostInfo.append(info)

		return hostInfo

	#Getters/Setters
	def getState(self):
		return self.stop

	def getNetInfo(self):
		return self.netInfo

	def setNetInfo(self, netInfo):
		self.netInfo = netInfo

	def getHostsList(self):
		return self.hostsList

	def setHostsList(self, hostsList):
		self.hostsList = hostsList

	def getNetInfo(self):
		return self.netInfo

	def setNetInfo(self, netInfo):
		self.netInfo = netInfo

	def getRecordArp1(self):
		return self.recordArp1

	def setRecordArp1(self, arpRecord):
		self.recordArp1 = arpRecord

	def getRecordArp2(self):
		return self.recordArp2

	def setRecordArp2(self, arpRecord):
		self.recordArp2 = arpRecord

	def getRecordPing1(self):
		return self.recordPing1

	def setRecordPing1(self, recordPing):
		self.recordPing1 = recordPing

	def getRecordPing2(self):
		return self.recordPing2

	def setRecordPing2(self, recordPing):
		self.recordPing2 = recordPing

	def getInfoThread(self):
		return self.infoThread
"""