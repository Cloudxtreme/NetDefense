#encoding: UTF-8
from arpPoisoning import ArpPoisoning

ACTIVE_MIN = 1 #Temps en que s'executa la defença de ARP Spoofing (minuts)
CHECK_PERIOD = 10 #Temps d'espera per comprobar si hi ha un atac (segons)
IP_ADDRESS = '192.168.1.1'
MASK = 24
test = ArpPoisoning(ACTIVE_MIN, CHECK_PERIOD, IP_ADDRESS, MASK)

def stopThread_test():	
	assert(test.getState() == False)
	test.stopThread()
	assert(test.getState() == True)

#stopThread_test()

def changeMaskFormat_test():	
	test_maskDQ = [255, 255, 255, 0]
	test_inverse = [0, 0, 0 , 255]
	result = test.changeMaskFormat()
	assert(result[0] == test_maskDQ)
	assert(result[1] == test_inverse)

#changeMaskFormat_test()

def notOperator_test(binary):
	assert(test.notOperator(binary) == '0101')

#notOperator_test('1010')

def netInfo_test():
	test.netInformation()
	result = test.getNetInfo()
	assert(result[0] == [192, 168, 1, 0])
	assert(result[1] == [192, 168, 1, 255])

#netInfo_test()

def searchHosts_test():
	test.netInformation()
	test.searchHosts()
	print test.getHostsList()
	assert(len(test.getHostsList()) == 254)

#searchHosts_test()

def getArpRecord_test():
	result = test.getArpRecord()
	print result
	assert('192.168.1.1' in result)

#getArpRecord_test()

def getPingRecord_test():
	hostsList = ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5']
	test.setHostsList(hostsList)
	result = test.getPingRecord()
	assert(result['192.168.1.1'] == "ON")

#getPingRecord_test()

def checkArpPoisoning_test():
	#No hi ha cap atac i les dades no es modifiquen
	rp1 = {'192.168.1.5': 'ON', '192.168.1.4': 'ON', '192.168.1.3': 'OFF', '192.168.1.2': 'ON', '192.168.1.1': 'ON'}
	rp2 = {'192.168.1.5': 'ON', '192.168.1.4': 'ON', '192.168.1.3': 'OFF', '192.168.1.2': 'ON', '192.168.1.1': 'ON'}
	ra1 = {'192.168.1.5': '18:00:2d:bb:cf:10', '192.168.1.4': '30:39:26:4f:37:5f', '192.168.1.3': 'FAILED', '192.168.1.2': '54:04:a6:a5:91:85', '192.168.1.1': 'f8:8e:85:0d:8e:33'}
	ra2 = {'192.168.1.5': '18:00:2d:bb:cf:10', '192.168.1.4': '30:39:26:4f:37:5f', '192.168.1.3': 'FAILED', '192.168.1.2': '54:04:a6:a5:91:85', '192.168.1.1': 'f8:8e:85:0d:8e:33'}
	test.setRecordPing1(rp1)
	test.setRecordPing2(rp2)
	test.setRecordArp1(ra1)
	test.setRecordArp2(ra2)
	result = test.checkArpPoisoning()
	assert(len(result) == 0)

	#Hi ha un atac de DoS a l'adreça 192.168.1.4 i 192.168.1.1
	rp1 = {'192.168.1.5': 'ON', '192.168.1.4': 'ON', '192.168.1.3': 'OFF', '192.168.1.2': 'ON', '192.168.1.1': 'ON'}
	rp2 = {'192.168.1.5': 'ON', '192.168.1.4': 'OFF', '192.168.1.3': 'OFF', '192.168.1.2': 'ON', '192.168.1.1': 'OFF'}
	ra1 = {'192.168.1.5': '18:00:2d:bb:cf:10', '192.168.1.4': '30:39:26:4f:37:5f', '192.168.1.3': 'FAILED', '192.168.1.2': '54:04:a6:a5:91:85', '192.168.1.1': 'f8:8e:85:0d:8e:33'}
	ra2 = {'192.168.1.5': '18:00:2d:bb:cf:10', '192.168.1.4': '11:22:33:44:55:66', '192.168.1.3': 'FAILED', '192.168.1.2': '54:04:a6:a5:91:85', '192.168.1.1': '66:55:44:33:22:11'}
	test.setRecordPing1(rp1)
	test.setRecordPing2(rp2)
	test.setRecordArp1(ra1)
	test.setRecordArp2(ra2)
	result = test.checkArpPoisoning()
	assert(len(result) == 2)

#checkArpPoisoning_test()

