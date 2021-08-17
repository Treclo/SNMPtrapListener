from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from datetime import datetime
import sqlite3
import socket

class DataBase:
	def connect(self):
		self.database = sqlite3.connect("../web/app/SpazioDatabase.sql")

	def execute(self, query):
		data = self.database.execute(query)
		self.database.commit()
		return data.fetchall()

	def close(self):
		self.database.close()

def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
	while wholeMsg:
		msgVer = int(api.decodeMessageVersion(wholeMsg))
		if msgVer in api.protoModules:
			pMod = api.protoModules[msgVer]
		else:
			print('Unsupported SNMP version %s' % msgVer)
			return
		reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
		ip = '%s' % ( transportAddress[0] )
		if ip == "10.36.34.17":
			machine = "axpr0014"
		elif ip == "10.66.225.132":
			machine = "iab15051"
		elif ip == "10.36.34.12":
			machine = "axpr0009"
		elif ip == "10.65.64.33" or ip == "10.65.0.190":
			machine = "amparo"
		elif ip == "10.65.67.152" or ip == "10.65.64.55" or ip == "10.65.64.56" or ip == "10.65.64.45":
			machine = "berta10.berta20"
		elif ip == "10.65.64.104" or ip == "10.65.0.232":
			machine = "carmen"
		elif ip == "10.65.0.186" or ip == "10.65.0.187" or ip == "10.65.64.29" or ip == "10.65.64.30":
			machine = "cristina10.cristina20"
		elif ip == "10.65.64.90" or ip =="10.65.0.219":
			machine = "dalila"
		elif ip == "10.65.64.89":
			machine = "dunaida10"
		elif ip == "10.65.64.34":
			machine = "dunaida20"
		elif ip == "10.65.67.136" or ip == "10.65.3.59":
			machine = "edelia"
		elif ip == "10.65.64.96" or ip == "10.65.64.96" or ip == "10.65.0.224":
			machine = "engracia"
		elif ip == "10.65.64.240" or ip == "10.65.1.169":
			machine = "front3"
		elif ip == "10.72.224.73":
			machine = "fsb1x106"
		elif ip == "10.72.224.26":
			machine = "fsb1x117"
		elif ip == "10.72.224.74":
			machine = "fsb2x107"
		elif ip == "10.72.224.27":
			machine = "fsb2x617"
		elif ip == "10.66.224.36" or ip == "10.66.224.36":
			machine = "hub00902"
		elif ip == "10.66.224.34" or ip == "10.66.224.34" or ip == "10.66.224.34":
			machine = "hub00903"
		elif ip == "10.66.227.166" or ip == "10.66.227.165":
			machine = "hub11550.hub26550"
		elif ip == "10.66.224.227" or ip == "10.66.224.228":
			machine = "hub15450.hub25950"
		elif ip == "10.66.225.173" or ip == "10.66.225.167":
			machine = "hub15451.hub25951"
		elif ip == "10.64.34.45":
			machine = "ripley"
		elif ip == "10.66.224.28" or ip == "10.66.224.24":
			machine = "iab10050.iab20150"
		elif ip == "10.66.224.29" or ip == "10.66.224.25":
			machine = "iab10051.iab20151"
		elif ip == "10.66.224.30" or ip == "10.66.224.26":
			machine = "iab10052.iab20152"
		elif ip == "10.66.224.81":
			machine = "iab10355"
		elif ip == "10.66.224.63":
			machine = "iab20755"
		elif ip == "10.66.224.54" or ip == "10.66.224.55":
			machine = "iab10250.iab21050"
		elif ip == "10.66.224.27" or ip == "10.66.224.31" or ip == "10.66.225.15":
			machine = "iab10252.iab20352"
		elif ip == "10.66.224.64" or ip == "10.66.224.65" or ip == "10.66.208.46" or ip == "10.66.208.47":
			machine = "iab10751.iab20851"
		elif ip == "10.66.224.71" or ip == "10.66.224.72":
			machine = "iab10753.iab20853"
		elif ip == "10.66.225.131" or ip == "10.66.225.137":
			machine = "iab15050.iab25150"
		elif ip == "10.66.225.145" or ip == "10.66.225.150":
			machine = "iab15250.iab25350"
		elif ip == "10.66.225.158" or ip == "10.66.225.116":
			machine = "iab15750.iab25850"
		elif ip == "10.66.225.139" or ip == "10.66.227.118":
			machine = "iab15052.iab25152"
		elif ip == "10.66.225.123" or ip == "10.66.225.124":
			machine = "iab15253.iab25353"
		elif ip == "10.66.225.11" or ip == "10.66.225.12":
			machine = "iab15752.iab25852"
		elif ip == "10.66.224.82":
			machine = "iab10354"
		elif ip == "10.66.224.83":
			machine = "iab20754"
		elif ip == "10.66.225.134":
			machine = "iab15053"
		elif ip == "10.66.225.138":
			machine = "iab25151"
		elif ip == "10.66.225.140":
			machine = "iab25153"
		elif ip == "10.36.34.252":
			machine = "axpr0009"
		else:
			try:
				machine = socket.gethostbyaddr(ip)[0]
				machine = machine[0:machine.find('.')]
			except:
				machine = ip

		if machine == "alba10-neg":
			machine = "alba10"
		elif machine == "alba20-neg":
			machine = "alba20"
		elif machine == "ssb16350-cpd":
			machine = "ssb16350"
		elif machine == "ssb26450-cpd":
			machine = "ssb26450"

		reqPDU = pMod.apiMessage.getPDU(reqMsg)
		if reqPDU.isSameTypeWith(pMod.TrapPDU()):
			trap = pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
			varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
			now = datetime.now()
			date = now.strftime("%d/%b/%Y %H:%M")
			db = DataBase()

		for oid, val in varBinds:
			if oid.prettyPrint() == "1.3.6.1.4.1.2404.2.4.1.1.2":
				resource = val.prettyPrint()
			elif oid.prettyPrint() == "1.3.6.1.4.1.2404.2.6.1.1.2":
				line = val.prettyPrint()
			elif oid.prettyPrint() == "1.3.6.1.4.1.2404.2.8.6.1.2":
				queue = val.prettyPrint()
			elif oid.prettyPrint() == "1.3.6.1.4.1.2404.2.8.6.1.3":
				resource = val.prettyPrint()
			elif oid.prettyPrint() == "1.3.6.1.4.1.2404.2.10.3.1.2":
				process = val.prettyPrint()

		if trap == "0":
			status = "Spazio parado"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'WARN', 'Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "1":
			status = "Spazio se ha caido"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "2":
			status = "Spazio funcionando correctamente"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "3":
			status = "Spazio en estado desconocido"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "4":
			status = "Gestor {resource} inactivo".format(resource=resource)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Gestores' and status LIKE 'Gestor {resource}%';".format(machine=machine, resource=resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Gestores', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "5":
			status = "Gestor {resource} activo".format(resource=resource)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Gestores' and status LIKE 'Gestor {resource}%';".format(machine=machine, resource=resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Gestores', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "6":
			status = "Linea {line} desactivada".format(line=line)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Lineas' and status LIKE 'Linea {line}%';".format(machine=machine, line=line)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Lineas', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "7":
			status = "Linea {line} activada".format(line=line)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Lineas' and status LIKE 'Linea {line}%';".format(machine=machine, line=line)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Lineas', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "8":
			status = "Transport manager inactivo"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transport manager';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Transport manager', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "9":
			status = "Transport manager activo"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transport manager';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Transport manager', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "10":
			status = "Hay transferencias en fallo"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transferencias';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Transferencias', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "11":
			status = "Sin transferencias en fallo"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transferencias';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Transferencias', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "12":
			status = "Hay transferencias pendientes"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transferencias';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Transferencias', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "13":
			status = "Sin transferencias pendientes"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Transferencias';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Transferencias', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "16":
			status = "La cola {queue} del gestor {resource} tiene ficheros sin extraer".format(queue=queue, resource=resource)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Ficheros' and dangerLevel = 'OK';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Ficheros', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "17":
			status = "Las colas no tienen ficheros sin extraer"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Ficheros' and status = 'La cola {queue} del gestor {resource} tiene ficheros sin extraer';".format(machine=machine, queue=queue, resource=resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Ficheros', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "24":
			status = "El proceso {process} esta caido".format(process=process)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Procesos' and status = 'El proceso {process} esta corriendo';".format(machine=machine, process=process)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Procesos', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "25":
			status = "El proceso {process} esta corriendo".format(process=process)
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Procesos' and status LIKE 'El proceso {process}%';".format(machine=machine, process=process)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Procesos', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "27":
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Spazio' and dangerLevel != 'OK';".format(machine=machine)
			update_query = "update SpazioStatus set date = '{date}' where machine = '{machine}';".format(machine=machine, process=process)
		elif trap == "42":
			status = "El agente SNMP no esta contemplado en la licencia"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Licencia SNMP';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Licencia SNMP', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "43":
			status = "El agente SNMP tiene licencia"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Licencia SNMP';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Licencia SNMP', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "44":
			status = "La licencia de Spazio no es valida"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Licencia Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'NOTOK', 'Licencia Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "45":
			status = "La licencia de Spazio caducara en menos de 30 dias"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Licencia Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'WARN', 'Licencia Spazio', '{date}');".format(machine=machine, status=status, date=date)
		elif trap == "46":
			status = "La licencia de Spazio es correcta"
			delete_query = "delete from SpazioStatus where machine = '{machine}' and problemGroup = 'Licencia Spazio';".format(machine=machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('{machine}', '{status}', 'OK', 'Licencia Spazio', '{date}');".format(machine=machine, status=status, date=date)

		if "delete_query" in locals() and "update_query" in locals():
			try:
				db.connect()
				db.execute(delete_query)

				if trap == "17":
					check = db.execute("select * from SpazioStatus where machine = '{machine}' and problemGroup = 'Ficheros';".format(machine=machine))
					if not check:
						db.execute(update_query)
				else:
					db.execute(update_query)
			except:
				print("Error en la base de datos")

			finally:
				db.close()

	return wholeMsg

transportDispatcher = AsyncoreDispatcher()
transportDispatcher.registerRecvCbFun( cbFun )
transportDispatcher.registerTransport( udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', 5001)) )
transportDispatcher.jobStarted( 1 )
try:
	transportDispatcher.runDispatcher()
except:
	transportDispatcher.closeDispatcher()
	raise