from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from datetime import datetime
import sqlite3
import socket

class DataBase:
	def connect(self):
		self.database = sqlite3.connect("../docs/app/database")

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

		try:
			machine = socket.gethostbyaddr(ip)[0]
			machine = machine[0:machine.find('.')]
		except:
			machine = ip

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
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'WARN', 'Spazio', '%s');" % (machine, status, date)
		elif trap == "1":
			status = "Spazio se ha caido"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Spazio', '%s');" % (machine, status, date)
		elif trap == "2":
			status = "Spazio funcionando correctamente"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Spazio', '%s');" % (machine, status, date)
		elif trap == "3":
			status = "Spazio en estado desconocido"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Spazio', '%s');" % (machine, status, date)
		elif trap == "4":
			status = "Gestor %s inactivo" % (resource)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Gestores' and status LIKE 'Gestor %s%';" % (machine, resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Gestores', '%s');" % (machine, status, date)
		elif trap == "5":
			status = "Gestor %s activo" % (resource)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Gestores' and status LIKE 'Gestor %s%';" % (machine, resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Gestores', '%s');" % (machine, status, date)
		elif trap == "6":
			status = "Linea %s desactivada" % (line)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Lineas' and status LIKE 'Linea %s%';" % (machine, line)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Lineas', '%s');" % (machine, status, date)
		elif trap == "7":
			status = "Linea %s activada" % (line)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Lineas' and status LIKE 'Linea %s%';" % (machine, line)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Lineas', '%s');" % (machine, status, date)
		elif trap == "8":
			status = "Transport manager inactivo"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transport manager';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Transport manager', '%s');" % (machine, status, date)
		elif trap == "9":
			status = "Transport manager activo"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transport manager';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Transport manager', '%s');" % (machine, status, date)
		elif trap == "10":
			status = "Hay transferencias en fallo"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transferencias';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Transferencias', '%s');" % (machine, status, date)
		elif trap == "11":
			status = "Sin transferencias en fallo"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transferencias';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Transferencias', '%s');" % (machine, status, date)
		elif trap == "12":
			status = "Hay transferencias pendientes"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transferencias';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Transferencias', '%s');" % (machine, status, date)
		elif trap == "13":
			status = "Sin transferencias pendientes"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Transferencias';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Transferencias', '%s');" % (machine, status, date)
		elif trap == "16":
			status = "La cola %s del gestor %s tiene ficheros sin extraer" % (queue, resource)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Ficheros' and dangerLevel = 'OK';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Ficheros', '%s');" % (machine, status, date)
		elif trap == "17":
			status = "Las colas no tienen ficheros sin extraer"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Ficheros' and status = 'La cola %s del gestor %s tiene ficheros sin extraer';" % (queue, resource)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Ficheros', '%s');" % (machine, status, date)
		elif trap == "24":
			status = "El proceso %s esta caido" % (process)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Procesos' and status = 'El proceso %s esta corriendo';" % (machine, process)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Procesos', '%s');" % (machine, status, date)
		elif trap == "25":
			status = "El proceso %s esta corriendo" % (process)
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Procesos' and status = 'El proceso %s esta caido';" % (machine, process)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Procesos', '%s');" % (machine, status, date)
		elif trap == "27":
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Spazio' and dangerLevel != 'OK';" % (machine)
			update_query = "update SpazioStatus set date = '%s' where machine = '%s';" % (date, machine)
		elif trap == "42":
			status = "El agente SNMP no esta contemplado en la licencia"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Licencia SNMP';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Licencia SNMP', '%s');" % (machine, status, date)
		elif trap == "43":
			status = "El agente SNMP tiene licencia"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Licencia SNMP';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Licencia SNMP', '%s');" % (machine, status, date)
		elif trap == "44":
			status = "La licencia de Spazio no es valida"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Licencia Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'NOTOK', 'Licencia Spazio', '%s');" % (machine, status, date)
		elif trap == "45":
			status = "La licencia de Spazio caducara en menos de 30 dias"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Licencia Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'WARN', 'Licencia Spazio', '%s');" % (machine, status, date)
		elif trap == "46":
			status = "La licencia de Spazio es correcta"
			delete_query = "delete from SpazioStatus where machine = '%s' and problemGroup = 'Licencia Spazio';" % (machine)
			update_query = "insert into SpazioStatus(machine, status, dangerLevel, problemGroup, date) values ('%s', '%s', 'OK', 'Licencia Spazio', '%s');" % (machine, status, date)

		if "delete_query" in locals() and "update_query" in locals():
			db.connect()
			db.execute(delete_query)

			if trap == "17":
				check = db.execute("select * from SpazioStatus where machine = '%s' and problemGroup = 'Ficheros';" % (machine))
				if not check:
					db.execute(update_query)
			else:
				db.execute(update_query)
			
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