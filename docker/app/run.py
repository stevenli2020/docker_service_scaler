#!/usr/bin/python
import os, string, random, time, socket, thread, sys, commands, json
from bottle import route, run, template

LEADER_ONLINE = True

def UDP_ECHO():
	while 1:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			server = ('0.0.0.0', 733)
			sock.bind(server)
			print("Echo service started on 0.0.0.0:733")
			while True:
				payload, client_address = sock.recvfrom(8)
				print("Echoing data back to " + str(client_address))
				sent = sock.sendto(payload, client_address)
		except:
			print("Service stopped")
			time.sleep(2)

def API_SERVER():
	global CONF
	while 1:
		try:
			@route('/hello')
			@route('/hello/')
			def hello():
				return 'Yes?\n'					
			@route('/scale/<svc>/<n>')
			def scale(svc,n):
				try:
					EXEC("docker service scale "+svc+"="+str(n))
					return 'OK\n'			
				except:
					return 'NAK\n'
			@route('/scale/<svc>')
			@route('/scale/<svc>/')
			def get_scale(svc):
				try:
					return EXEC("docker service ps "+svc+" --format '{{.Name}}' | wc -l")+"\n"		
				except:
					return "NAK\n"
			@route('/scaleup/<svc>/<n>/')
			@route('/scaleup/<svc>/<n>')
			def scaleup(svc, n):
				try:      
					N = int(n)+int(EXEC("docker service ps "+svc+" --format '{{.Name}}' | wc -l"))
					EXEC("docker service scale "+svc+"="+str(N))
					return str(N)+"\n"
				except:
					return "NAK\n"
			@route('/scaledn/<svc>/<n>/')
			@route('/scaledn/<svc>/<n>')
			def scaledn(svc, n):
				try:
					N = int(EXEC("docker service ps "+svc+" --format '{{.Name}}' | wc -l")) - int(n)
					if N < int(CONF['BASE_REPLICATION']):
						return "Smaller than minimum number of replications\n"
					EXEC("docker service scale "+svc+"="+str(N))
					return str(N)+"\n"
				except:
					return "NAK\n"					
					
			print("API service started on 0.0.0.0:733")
			run(host='0.0.0.0', port=733)

			
		except:
			print("API service stopped")
			time.sleep(2)			
			
def EXEC(CMD):
	ERR_SUCCESS,OUTPUT = commands.getstatusoutput(CMD)
	return OUTPUT

def CHECK_LEADER():
	global LEADER_ONLINE, CONF
	while 1: 
		print "Check if leader node is online"
		if EXEC("curl -s "+CONF['LEADER_NODE']+":733/hello").strip() == "Yes?":
			LEADER_ONLINE = True
			print "- leader node is online"
		else: 
			LEADER_ONLINE = False
			print "- leader node is offline"
		time.sleep(30)
	pass
#=====================================================

with open("/conf/config", 'r') as f:
	CONF = json.loads(f.read())
# print CONF
# thread.start_new_thread(UDP_ECHO,())
thread.start_new_thread(API_SERVER,())

if CONF['MODE'] != "LEADER":
	thread.start_new_thread(CHECK_LEADER,())
	
REPLICATION = int(EXEC("docker service ps "+CONF['SERVICE']+" --format '{{.Name}}' | wc -l"))
# REPLICATION = REPLICATION + 2
# EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
# exit()
PORTS = ""
for P in CONF['PORTS']:
	PORTS = PORTS+":"+str(P)+" |"
PORTS = PORTS[:-1]
# print PORTS
T0 = time.time()-int(CONF['STABLIZATION'])
while 1:
	time.sleep(CONF['INTERVAL'])
	if CONF['MODE'] != "LEADER": 
		if LEADER_ONLINE == True:
			print "Leader node is online, skip"
			continue
	if CONF['AUTOSCALE'] != True:
		continue
	T1 = time.time()
	CONNECTIONS = int(EXEC("docker exec $(docker ps -f NAME=$(docker service ps -f NODE="+CONF['NODE']+" "+CONF['SERVICE']+" --format '{{.Name}}' | head -1) --format '{{.Names}}') netstat -tan | grep -E '"+PORTS+"' | wc -l"))
	print "Current number of containers: "+str(REPLICATION)+", connections on each: "+str(CONNECTIONS)
	if T1 - T0 > int(CONF['STABLIZATION']):
		if CONNECTIONS > CONF['CONN_THRESHOLD_H']:
			REPLICATION = REPLICATION + 2
			print "Scale up service '"+CONF['SERVICE']+"' by 2, REPLICATION="+str(REPLICATION)
			EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
			print "Wait 30s for connection to be stablized..."
			T0 = time.time()			
		elif CONNECTIONS < CONF['CONN_THRESHOLD_L'] and REPLICATION != CONF['BASE_REPLICATION']:
			REPLICATION = REPLICATION - 2
			print "Scale down service '"+CONF['SERVICE']+"' by 2, REPLICATION="+str(REPLICATION)
			EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
			print "Wait 30s for connection to be stablized..."
			T0 = time.time()
	
	
	
	
	
	
	