import sys
import time
import socket

def getLines(inputFile, linesNumber, period, repeat):
	with open(inputFile, "r") as file:
		actualLines = 0
		startTime = time.time()
		while(float(time.time() - startTime) < float(period)):
			line = file.readline()

			if not line:
				if repeat == "True":
					file.seek(0,0)
				else:
					print("    [*] End of file -> lines:", actualLines)
					break
				continue
			else:
				if not line.endswith('\n'):
					line = line + "\n"
				actualLines += 1

			if actualLines == int(linesNumber):
				print("    [*] Elapsed time in secs:",round(time.time() - startTime, 6), "-> lines:", actualLines)
				actualLines = 0
				startTime = time.time()

			yield line
		else:
			print("    [*] We can't send", linesNumber, "lines in", period, "secs, we just send", actualLines)

def writeDataToFile(filename,line):
	with open(filename, "a") as file:
		file.write(line)

def sendDataViaSocket(sckt,text):
	sckt.send(line)

def mainFile(typeProces, filename, inputFile, linesNumber, period, repeat):
	print("[+] Process type:",typeProces)
	lines = getLines(inputFile, linesNumber, period, repeat)
	for line in lines:
		writeDataToFile(filename,line)
	

def mainSocket(typeProces, IP, port, inputFile, linesNumber, period, repeat):
	print("[+] Process type:",typeProces)
	sckt = socket.socket()
	sckt.connect((IP, port))
	lines = getLines(inputFile, linesNumber, period, repeat)
	for line in lines:
		sendDataViaSocket(sckt,line)

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