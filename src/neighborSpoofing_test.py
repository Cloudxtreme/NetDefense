#encoding: UTF-8
from neighborSpoofing import NeighborSpoofing

ACTIVE_MIN = 1 #Temps en que s'executa la defença de ARP Spoofing (minuts)
CHECK_PERIOD = 10 #Temps d'espera per comprobar si hi ha un atac (segons)
test = NeighborSpoofing(ACTIVE_MIN, CHECK_PERIOD)

def stopThread_test():	
	assert(test.getState() == True)
	test.stopThread()
	assert(test.getState() == False)

#stopThread_test()

def getNeighborTable_test():
	#TODO
	x = 0

#getNeighborTable_test()

def checkNeighborSpoofing_test():
	record = {'fe80::201:23ff:fe45:6789':'00:01:02:03:04:05:06', 
			'fe80::201:22fc:fe45:6798':'00:01:02:03:04:05:07',
			'fe80::201:22fc:fe45:5358':'00:01:02:03:04:05:08',
			'fe80::201:22fc:fe45:631':'00:01:02:03:04:05:09'}
	test.setNeighborRecord(record)
	result = test.checkNeighborSpoofing()
	assert(len(result) == 0)

	record = {'fe80::201:23ff:fe45:6789':'00:01:02:03:04:05:06', 
			'fe80::201:22fc:fe45:6798':'00:01:02:03:04:05:07',
			'fe80::201:22fc:fe45:5358':'00:01:02:03:04:05:08',
			'fe80::201:22fc:fe45:631':'00:01:02:03:04:05:06'}
	test.setNeighborRecord(record)
	result = test.checkNeighborSpoofing()
	assert(len(result) == 2)

#checkNeighborSpoofing_test()