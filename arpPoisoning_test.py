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
	assert(len(test.getHostsList()) == 254)

#searchHosts_test()

