import re
from tabulate import tabulate
import sys
import time
import subprocess 

#LogFormat custom "TIME:%t CLIENT:%u IP:%a FILE:%F PATH:%f METHOD:%m CODE:%s"
regDate = r"TIME:(\[.*\])"
regClient = r"CLIENT:(.*?) "
regIP = r"IP:(.*?) "
regFile = r"FILE:(.*?) "
regPath = r"PATH:(.*?) "
regMethod = r"METHOD:(.*?) "
regCode = r"CODE:(\d{1,3}) "
regRESP = r"RESP:(.*)"
regCodeError = r"CODE:5.*"
everything = r".*" #toma todos los caracteres de la línea excepto el salto de linea
regHostname = r"HOSTNAME:(.*)"

def getHostname(log):
	results_list = re.findall(regHostname,log)
	#print(results_list)
	return results_list[0]

def getIpUsers(log,users):
	ips= []
	for user in users:
		argumentoFinal =  everything+user+everything#se concatenan dos strings, el de la fecha específica y el que toma todo lo demas
		regExpresion = re.compile(argumentoFinal)
		results_list = regExpresion.findall(log)#ENCUENTRA TODO LO QUE COINCIDA CON LA EXPRESION REGULAR DEL DÍA INDICADO
		ip = re.findall(regIP,results_list[len(results_list)-1])
		#print(ip)
		ips.append(ip[0])
	return ips

def getUsers(prelista):
	usersOnline = []
	for element in prelista:
		splitter = element.split(' ')#separa todos los argumentos por espacio
		usersOnline.append(splitter[1])#toma el argumento que pertenece al usuario
	return usersOnline

def resumenUsuarios(log):
	
	resultCommand = str(subprocess.check_output('ftpwho'))
	#print(resultCommand)
	#print(type(resultCommand))
	listaTotal = resultCommand.split('\\n')
	#print(listaTotal)
	#print(len(listaTotal))
	prelista = listaTotal[1:len(listaTotal)-2]
	#print(prelista)
	users = getUsers(prelista)
	#print(users)
	hostname = getHostname(log)
	#print(hostname)
	ips = getIpUsers(log,users)
	REGISTROS = []
	for i in range(len(users)):
		REGISTROS.append([users[i],ips[i],hostname])
	print(tabulate(REGISTROS,headers=['User','Ip','Hostname'],tablefmt="fancy_grid"))	

def readLog(path,argumentos):
	try:
		log = reader(path)
		
		if(argumentos[1]=='user' or argumentos[1]=='date' or argumentos[1]=='ip'):
			#print('1')
			regExpresion = prepareReg(argumentos)
			results_list = regExpresion.findall(log)#ENCUENTRA TODO LO QUE COINCIDA CON LA EXPRESION REGULAR DEL DÍA INDICADO
			getTable(results_list)	
		elif(argumentos[1]=='error'):
			#print('2')
			while(True):#queda en bucle y actualiza cada 10 segundos
				argumentoFinal =  everything+regCodeError+everything#se concatenan dos strings, el de la fecha específica y el que toma todo lo demas
				regExpresion = re.compile(argumentoFinal)
				#print(reFinal)
				results_list = regExpresion.findall(log)#ENCUENTRA TODO LO QUE COINCIDA CON LA EXPRESION REGULAR DEL DÍA INDICADO
				#print(results_list)
				get_only_errors(results_list)
				time.sleep(10)
		elif(argumentos[1]=='online'):
			resumenUsuarios(log)


	except Exception as e:
		print('Un error en los argumentos ha ocurrido')
		print("Excepcion: {}".format(e))	

def reader(path):
	with open(path) as file:
		return file.read()

def prepareReg(argumentos):
	everything = r".*" #toma todos los caracteres de la línea excepto el salto de linea
	
	if(len(argumentos)==3): #si solo se hara el filtrado por un parametro
		argumentoFiltro = argumentos[2]#se pasa el argumento del filtro elegido
		argumentoFinal =  everything+argumentoFiltro+everything#se concatenan dos strings, el de la fecha específica y el que toma todo lo demas			
	elif(argumentos[1]=='Date' and argumentos[3]=='Hour'):#si se hará el filtrado por dos argumentos(fecha y hora)	
		
		digito = r"\d{2}"
		argumentoFiltro = argumentos[2] #argumento del primer filtro(fecha)
		argumentoFiltro2 = argumentos[4] #argumento del segundo filtro(hora)
		argumentoFinal = everything+argumentoFiltro+":"+argumentoFiltro2+":"+digito+":"+digito+everything

	return re.compile(argumentoFinal) #Todo se convierte en una sola expresion regular
	
def get_only_errors(lista):
	REGISTROS = []
	for line in lista:
		#print(line)
		Date = re.findall(regDate,line)
		Splitter = Date[0].split(" ")
		Client = re.findall(regClient,line)
		IP = re.findall(regIP,line)
		#Files = re.findall(regFile,line)
		path = re.findall(regPath,line)
		method = re.findall(regMethod,line)
		code = re.findall(regCode,line)
		resp = re.findall(regRESP,line)
		#print("Fecha:{} Cliente:{} Ip:{} dirC:{} dirS:{} Op:{} Cod:{}".format(Splitter[0],Client,IP,Files,path,method,code))
		#print("Fecha:{} Ip:{} dirS:{} Op:{} Cod:{} Resp:{}".format(Splitter[0],IP,path,method,code,resp))
		#REGISTROS.append([Splitter[0][1:],Client[0],IP[0],Files[0],path[0],method[0],code[0]])
		if(len(path)==0):
			#print('1')
			REGISTROS.append([Splitter[0][1:],IP[0],'-',method[0],code[0],resp[0]])
		else:
			#print('2')
			REGISTROS.append([Splitter[0][1:],IP[0],path[0],method[0],code[0],resp[0]])
	#print(tabulate(REGISTROS,headers=['Fecha','Cliente','Ip','dirC','dirS','Op','Cod'],tablefmt="fancy_grid"))	
	if(len(REGISTROS)>5):
		REGISTROS = REGISTROS[len(REGISTROS)-5:]#toma los últimos 5
	print(tabulate(REGISTROS,headers=['Fecha','Ip','dirS','Op','Cod','Resp'],tablefmt="fancy_grid"))	

		
def getTable(lista):
	REGISTROS = []
	for line in lista:
		#print(line)
		Date = re.findall(regDate,line)
		Splitter = Date[0].split(" ")
		Client = re.findall(regClient,line)
		IP = re.findall(regIP,line)
		Files = re.findall(regFile,line)
		path = re.findall(regPath,line)
		method = re.findall(regMethod,line)
		code = re.findall(regCode,line)
		resp = re.findall(regRESP,line)
		#print("Fecha:{} Cliente:{} Ip:{} dirC:{} dirS:{} Op:{} Cod:{}".format(Splitter[0],Client,IP,Files,path,method,code))

		#REGISTROS.append([Splitter[0][1:],Client[0],IP[0],Files[0],path[0],method[0],code[0]])
		if ((len(code)==0 or code[0]!='-' or code[0][0]!='5') and Files[0]!='-'):
			REGISTROS.append([Splitter[0][1:],Client[0],IP[0],path[0],method[0],code[0]])
	#print(tabulate(REGISTROS,headers=['Fecha','Cliente','Ip','dirC','dirS','Op','Cod'],tablefmt="fancy_grid"))	
	print(tabulate(REGISTROS,headers=['Fecha','Cliente','Ip','dirS','Op','Cod'],tablefmt="fancy_grid"))	

def printList(lista):
	for line in lista:
		print(line)

#print("sys.argv {}".format(sys.argv))
readLog("/var/log/proftpd/custom.log",sys.argv)
#resumenUsuarios()

""" 

#Agregar las siguientes líneas al archivo proftpd.conf

LogFormat custom "TIME:%t CLIENT:%u IP:%a FILE:%F PATH:%f METHOD:%m CODE:%s RESP:%S"
TransferLog /var/log/proftpd/xferlog
SystemLog   /var/log/proftpd/proftpd.log
ExtendedLog /var/log/proftpd/custom.log ALL custom

#Agregar las siguientes líneas al archivo proftpd.conf

Ejecutando el script desde consola:

1.-Ver registros por fecha: 
python3 readerFTP.Py Date dd/mmm/aaaa. 

dd = día del mes a dos dígitos.
mmm = mes del año, los tres primeros caracteres(en minúsculas), ej. si el mes es Octubre: oct.
aaaa = los cuatro dígitos del año actual.

2.-Ver registros por fecha y hora(formato de 24hrs): 
python3 readerFTP.Py Date dd/mmm/aaaa Hour \d{2}

donde \d{2} es un dígito de dos números, ej. 00,01,02,03,04,05,06,07... 19,20,21,22,23 

3.-Ver registros por nombre de usuario: 
python3 readerFTP.py User name_user

4.-Ver registros por ip: 
python3 readerFTP.py Ip ip_user

5.-Correr bucle de errores
python3 readerFTP.py error

	este último comando mostrara los últimos 5 errores que hubo en el server

"""