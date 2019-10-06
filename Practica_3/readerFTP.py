import re
from tabulate import tabulate
import sys

#LogFormat custom "TIME:%t CLIENT:%u IP:%a FILE:%F PATH:%f METHOD:%m CODE:%s"
regDate = r"TIME:(\[.*\])"
regClient = r"CLIENT:(.*?) "
regIP = r"IP:(.*?) "
regFile = r"FILE:(.*?) "
regPath = r"PATH:(.*?) "
regMethod = r"METHOD:(.*?) "
regCode = r"CODE:(\d{1,3})"
everything = r".*" #toma todos los caracteres de la línea excepto el salto de linea

def readLog(path,argumentos):
	try:
		log = reader(path)
		regExpression = prepareReg(argumentos)
		results_list = regExpression.findall(log)#ENCUENTRA TODO LO QUE COINCIDA CON LA EXPRESION REGULAR DEL DÍA INDICADO}
		getTable(results_list)	
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
		#print("3")
	elif(argumentos[1]=='Date' and argumentos[3]=='Hour'):#si se hará el filtrado por dos argumentos(fecha y hora)	
		#print("5")
		digito = r"\d{2}"
		argumentoFiltro = argumentos[2] #argumento del primer filtro(fecha)
		argumentoFiltro2 = argumentos[4] #argumento del segundo filtro(hora)
		argumentoFinal = everything+argumentoFiltro+":"+argumentoFiltro2+":"+digito+":"+digito+everything

	return re.compile(argumentoFinal) #Todo se convierte en una sola expresion regular
	
		
		
def getTable(lista):
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
		#print("Fecha:{} Cliente:{} Ip:{} dirC:{} dirS:{} Op:{} Cod:{}".format(Splitter[0],Client,IP,Files,path,method,code))

		#REGISTROS.append([Splitter[0][1:],Client[0],IP[0],Files[0],path[0],method[0],code[0]])
		REGISTROS.append([Splitter[0][1:],Client[0],IP[0],path[0],method[0],code[0]])
	#print(tabulate(REGISTROS,headers=['Fecha','Cliente','Ip','dirC','dirS','Op','Cod'],tablefmt="fancy_grid"))	
	print(tabulate(REGISTROS,headers=['Fecha','Cliente','Ip','dirS','Op','Cod'],tablefmt="fancy_grid"))	

def printList(lista):
	for line in lista:
		print(line)

#print("sys.argv {}".format(sys.argv))
readLog("/var/log/proftpd/custom.log",sys.argv)
