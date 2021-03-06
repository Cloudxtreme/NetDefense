#encoding: UTF-8
from arpSpoofing import ArpSpoofing

ACTIVE_MIN = 1 #Temps en que s'executa la defença de ARP Spoofing (minuts)
CHECK_PERIOD = 10 #Temps d'espera per comprobar si hi ha un atac (segons)
test = ArpSpoofing(ACTIVE_MIN, CHECK_PERIOD)

def stopThread_test():	
	assert(test.getState() == True)
	test.stopThread()
	assert(test.getState() == False)

#stopThread_test()

def getArpTable_test():	
	test.getArpTable()
	assert('192.168.1.1' in test.getArpRecord())

#getArpTable_test()

def checkArpSpoofing_test():
	arpInfo = {"192.168.1.1":"11:00:00:00:00:00", "192.168.1.2":"12:00:00:00:00:00", "192.168.1.3":"13:00:00:00:00:00",
				"192.168.1.4":"14:00:00:00:00:00","192.168.1.5":"15:00:00:00:00:00"}
	test.setArpRecord(arpInfo)
	result = test.checkArpSpoofing()
	assert(len(result) == 0)

	arpInfo = {"192.168.1.1":"11:00:00:00:00:00", "192.168.1.2":"12:00:00:00:00:00", "192.168.1.3":"13:00:00:00:00:00",
				"192.168.1.4":"14:00:00:00:00:00","192.168.1.5":"11:00:00:00:00:00"}
	test.setArpRecord(arpInfo)
	result = test.checkArpSpoofing()
	assert(len(result) == 2)

#checkArpSpoofing_test()
