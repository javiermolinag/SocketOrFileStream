# SocketOrFileStream
Python script to send data via socket, kafka or write in file. Implementation for Spark Streaming tests.

This script reads single file and write it in another file or send it via socket.

## Parameters

  filename: File to read, which is send via socket or write in another file

  number_lines: Numbers of lines to send or write

  period(secs): Time period to send or write the lines given by number_lines

  repeat: If input file (filename) only has 100 lines and you want to send 1000 lines every 10 seconds, when all lines are read (in this case 100), this flag will move the file pointer to the beginning, therefore, there is always data to send

## Usage

python sendDataFromFile.py [<socket> IP PORT | <file> FILENAME | <kafka> IP PORT TOPIC] filename number_lines period(secs) repeat

### Example for socket

python sendDataFromFile.py socket localhost 12345 input.txt 100 3 True

### Example for file

python sendDataFromFile.py file outputFIle.txt input.txt 500 2 False

### Example for kafka

python sendDataFromFile.py kafka localhost 9092 topic-name input.txt 500 3 False