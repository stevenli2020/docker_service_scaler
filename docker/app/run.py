#!/usr/bin/python
import os, string, random, time, socket, thread, sys, commands, json
from bottle import route, post, run, template

LEADER_ONLINE = True		
			
def EXEC(CMD):
	ERR_SUCCESS,OUTPUT = commands.getstatusoutput(CMD)
	return OUTPUT

	
@route('/hello')
@route('/hello/')
def hello():
	return '{"result":"OK","Message":"Yes?"}\n'

@route('/service/ls')
@route('/service/ls/')
@route('/service/ls/')
@route('/service/ls/')
def list_services():
	try:
		RESP = []
		SVC = EXEC("docker service ls --format '{{.ID}}-+++-{{.Name}}-+++-{{.Mode}}-+++-{{.Replicas}}-+++-{{.Image}}-+++-{{.Ports}}'").split("\n")
		
		for line in SVC:
			i = line.split("-+++-")
			# print i
			service = {
				"ID":i[0],
				"Name":i[1],
				"Mode":i[2],
				"Replicas":i[3],
				"Image":i[4],
				"Ports":i[5]
			}
			# print service
			RESP.append(service)
		return json.dumps(RESP)
	except:
		return '{"result":"failed"}\n'

@route('/service/ps/<svc>')
@route('/service/ps/<svc>/')
@post('/service/ps/<svc>/')
@post('/service/ps/<svc>/')
def service_ps(svc):
	try:
		RESP = []
		TASK = EXEC('docker service ps web --format "{{.ID}}-+++-{{.Name}}-+++-{{.Image}}-+++-{{.Node}}-+++-{{.DesiredState}}-+++-{{.CurrentState}}-+++-{{.Error}}-+++-{{.Ports}}"').split("\n")
		
		for line in TASK:
			i = line.split("-+++-")
			print i
			task = {
				"ID":i[0],
				"Name":i[1],
				"Image":i[2],
				"Node":i[3],
				"DesiredState":i[4],
				"CurrentState":i[5],
				"Error":i[6],
				"Ports":i[7]
			}
			RESP.append(task)
		return json.dumps(RESP)		
	except:
		return '{"result":"failed"}\n'
		
@route('/service/scale/<svc>/<n:int>')
@route('/service/scale/<svc>/<n:int>/')
@post('/service/scale/<svc>/<n:int>/')
@post('/service/scale/<svc>/<n:int>/')
def scale(svc,n):
	try:
		EXEC("docker service scale "+svc+"="+str(n))
		return '{"result":"OK"}\n'
	except:
		return '{"result":"failed"}\n'
		
@route('/service/scale/<svc>')
@route('/service/scale/<svc>/')
@post('/service/scale/<svc>/')
@post('/service/scale/<svc>/')
def get_scale(svc):
	try:
		return EXEC("docker service ps "+svc+" --format '{{.Name}}' | wc -l")+"\n"		
	except:
		return '{"result":"failed"}\n'
		
@route('/service/scaleup/<svc>/<n:int>/')
@route('/service/scaleup/<svc>/<n:int>')
@post('/service/scaleup/<svc>/<n:int>')
@post('/service/scaleup/<svc>/<n:int>')
def scaleup(svc, n):
	try:      
		N = int(n)+int(EXEC("docker service ps "+svc+" --format '{{.Name}}' | wc -l"))
		EXEC("docker service scale "+svc+"="+str(N))
		return '{"result":"OK","replicas":'+str(N)+'}\n'
	except:
		return '{"result":"failed"}\n'
		
@route('/service/scaledown/<svc>/<n:int>/')
@route('/service/scaledown/<svc>/<n:int>')
@post('/service/scaledown/<svc>/<n:int>')
@post('/service/scaledown/<svc>/<n:int>')
def scaledn(svc, n):
	try:
		N = int(EXEC("docker service ps "+svc+" --format '{{.ID}}' | wc -l")) - int(n)
		if N < 2:
			return '{"result":"error","message":"Targeted replicas smaller than 2"}\n'
		EXEC("docker service scale "+svc+"="+str(N))
		return '{"result":"OK","replicas":'+str(N)+'}\n'
	except:
		return '{"result":"failed"}\n'				

@route('/service/inspect/<svc>')
@route('/service/inspect/<svc>/')
@post('/service/inspect/<svc>')
@post('/service/inspect/<svc>/')
def inspect(svc):
	try:
		N = int(EXEC("docker service ps "+svc+" --format '{{.ID}}' | wc -l")) - int(n)
		if N < 2:
			return '{"result":"error","message":"Targeted replicas smaller than 2"}\n'
		EXEC("docker service scale "+svc+"="+str(N))
		return '{"result":"OK","replicas":'+str(N)+'}\n'
	except:
		return '{"result":"failed"}\n'
		
print("API service started on 0.0.0.0:80")
run(host='0.0.0.0', port=80)
	
	
	
	
	
	