import sys
import time
import socket

def getLines_(inputFile, linesNumber, period, repeat, mode):
	with open(inputFile, mode) as file:
		actualLines = 0
		startTime = time.time()
		while(float(time.time() - startTime) < float(period)):
			line = file.readline()
			# 'repeat' mode or finish, also adds \n if line hasn't it
			if not line:
				if repeat == "True":
					file.seek(0,0)
				else:
					print("    [*] End of file -> lines:", actualLines)
					break
				continue
			else:
				if mode == "r" and not line.endswith('\n'):
					line = line + '\n'
				actualLines += 1
			# do we ship all required lines?, if so please wait until the period is met
			if actualLines == int(linesNumber):
				print("    [*] Elapsed time in secs:",round(time.time() - startTime, 6), "-> lines:", actualLines)
				time.sleep(float(period) - float(time.time() - startTime))
				actualLines = 0
				startTime = time.time()
			yield line
		else:
			print("    [*] We can't send", linesNumber, "lines in", period, "secs, we just send", actualLines)

def getLines(inputFile, linesNumber, period, repeat, mode):
	print("    [*] Sending a single line each", float(period)/float(linesNumber), "secs")
	with open(inputFile, mode) as file:
		actualLines = 0
		while(True):
			line = file.readline()
			if not line:
				if repeat == "True":
					file.seek(0,0)
				else:
					print("    [*] End of file -> lines:", actualLines)
					break
				continue
			else:
				if mode == "r" and not line.endswith('\n'):
					line = line + '\n'
				actualLines += 1
			time.sleep(float(period)/float(linesNumber))
			yield line

def writeDataToFile(filename,line):
	with open(filename, "a") as file:
		file.write(line)

def sendDataViaSocket(sc,line):
	sc.send(line)

def mainFile(typeProces, filename, inputFile, linesNumber, period, repeat):
	print("[+] Process type:",typeProces)
	lines = getLines(inputFile, linesNumber, period, repeat, "r")
	for line in lines:
		writeDataToFile(filename,line)

def mainSocket(typeProces, IP, port, inputFile, linesNumber, period, repeat):
	print("[+] Process type:",typeProces)
	#sckt = socket.socket()
	#sckt.connect((IP, int(port)))
	sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sckt.bind((IP, int(port)))
	sckt.listen(1)
	sc, addr = sckt.accept()
	lines = getLines(inputFile, linesNumber, period, repeat, "rb")
	for line in lines:
		sendDataViaSocket(sc,line)
	else:
		print('Closing socket')
		sckt.close()


def printUsage():
	print("Usage: python sendDataFromFile.py [<socket> IP PORT | <file> FILENAME] filename number_lines period(secs) repeat")
	print("Example for socket: python sendDataFromFile.py socket localhost 12345 input.txt 100 3 True")
	print("Example for file: python sendDataFromFile.py file outputFIle.txt input.txt 500 2 False")


if __name__ == '__main__':
	if len(sys.argv) > 1:
		args = sys.argv[1:]
		if args[0] == "socket" and len(args) == 7:
			mainSocket(*args)
		elif args[0] == "file" and len(args) == 6:
			mainFile(*args)
		else:
			printUsage()
	else:
		printUsage()