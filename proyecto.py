#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Librerias requeridas para correr aplicaciones basadas en Flask
from flask import Flask, jsonify, make_response, request
import subprocess


app = Flask(__name__)

# Web service que se invoca al momento de ejecutar el comando
# curl http://localhost:5000
@app.route('/',methods = ['GET'])
def index():
	return "Hola Univalle"

# Este metodo retorna la lista de sistemas operativos soportados por VirtualBox
# Los tipos de sistemas operativos soportados deben ser mostrados al ejecutar 
# el comando
# curl http://localhost:5000/vms/ostypes
# Este es el codigo del item 1
@app.route('/vms/ostypes',methods = ['GET'])
def ostypes():
	output = subprocess.check_output(['VBoxManage','list','ostypes'])
	return output

# Este metodo retorna la lista de maquinas asociadas con un usuario al ejecutar
# el comando
# curl http://localhost:5000/vms
# Este es el codigo del item 2a
@app.route('/vms',methods = ['GET'])
def listvms():
	output = subprocess.check_output(['VBoxManage','list','vms'])
	return output

# Este metodo retorna aquellas maquinas que se encuentran en ejecucion al 
# ejecutar el comando
# curl http://localhost:5000/vms/running
# Este es el codigo del item 2b
@app.route('/vms/running',methods = ['GET'])
def runninglistvms():
	output = subprocess.check_output(['VBoxManage','list','runningvms'])
	return output

# Este metodo retorna las caracteristica de una maquina virtual cuyo nombre es
# vmname 3.
@app.route('/vms/info/<vmname>', methods = ['GET'])
def vminfo(vmname):	
	info = subprocess.Popen(['VBoxManage','showvminfo',vmname],stdout = subprocess.PIPE)
	grep = subprocess.check_output(['grep','-e','NIC','-e','Number','-e','Memory'],stdin = info.stdout)
	return grep


@app.errorhandler(404)
def not_found(error):
 return make_response("No se encontro ninguna maquina con el nombre indicado\n")

# Usted deberá realizar además los items 4 y 5 del enunciado del proyecto 
# considerando que:
# - El item 4 deberá usar el método POST del protocolo HTTP

@app.route('/vms/create', methods=['POST'])
def createvms():
	nombre = request.form['Nombre']
	nucleos = request.form['Nucleos']
	ram = request.form['Ram']
	mensaje = subprocess.check_output(['./scriptCrear',nombre,nucleos,ram])

	return mensaje	

# - El item 5 deberá usar el método DELETE del protocolo HTTP
@app.route('/vms/delete', methods=['DELETE'])
def deletevms():
	nombre = request.form['Nombre']

	mensaje = subprocess.check_output(['VBoxManage','unregistervm',nombre,'--delete'])

	return mensaje	

if __name__ == '__main__':
        app.run(debug = True, host='0.0.0.0')
