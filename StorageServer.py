'''
    YouTube plugin for XBMC
    Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Version 0.8
'''

import os, sys, socket, time
import xbmc
try: import xbmcvfs
except: import xbmcvfsdummy as xbmcvfs
try: import sqlite
except: import sqlite3

class StorageServer():
	__plugin__ = "StorageClient"
	__dbg__ = 1
	
	__path__ = os.path.join( xbmc.translatePath( "special://database" ), 'commoncache.db')
	__socket__ = ""
	__clientscoket__ = False
	__sql2__ = False
	__sql3__ = False
	__daemon_start_time__ = time.time()
	def startDB(self):
		try:
			self.sql2 = False
			self.sql3 = False
			if repr(sys.modules).find("sqlite3") > -1:
				self.sql3 = True
			else: # Verify this better
				self.sql2 = True

			if self.__dbg__ > 2:
				print self.__plugin__ + " startDB 1 : " + repr(self.sql2) + " - " + repr(self.sql3)

			if self.sql2:
				if self.__dbg__ > 2:
					print self.__plugin__ + " startDB 2 "
				self.__conn__ = sqlite.connect(self.__path__)
			elif self.sql3:
				if self.__dbg__ > 2:
					print self.__plugin__ + " startDB 3 "
				self.__conn__ = sqlite3.connect(self.__path__, check_same_thread=False)

			self.__curs__ = self.__conn__.cursor()
			return True
		except sqlite.Error, e:
			if self.__dbg__ > 0:
				print self.__plugin__ + " startDB exception: " + repr(e)
			xbmcvfs.delete(self.__path__)
			return False	

	def run(self):
		self.__plugin__ = "StorageServer"
		print self.__plugin__ + " Storage Server starting " + self.__path__
		if not self.startDB():
			self.startDB()

                if sys.platform == "win32":
			port = 59994
			self.__socket__ = (socket.gethostname(), port)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')
			#self.__socket__ = "/home/tobias/.xbmc/temp/commoncache.socket"
			if xbmcvfs.exists(self.__socket__):
				if self.__dbg__ > 0:
					print self.__plugin__ + " Unlinking stale socket file"
				os.unlink(self.__socket__)	
			sock = socket.socket(socket.AF_UNIX)

		sock.bind(self.__socket__)
		sock.listen(1)
		sock.setblocking(0)
		#socket.setdefaulttimeout(15)
		
		idle_since = time.time()
		waiting = 0
		while not xbmc.abortRequested:
			if waiting == 0 :
				if self.__dbg__ > 1:
					print self.__plugin__ + " Daemon accepting"
				waiting = 1
			try:
				(self.__clientsocket__, address) = sock.accept()
				waiting = 0
			except socket.error, e:
				if e.errno == 11 or e.errno == 10035 or e.errno == 35:
					# There has to be a better way to accomplish this.
					if idle_since + 5 < time.time():
						if waiting == 1:
							if self.__dbg__ > 0:
								print self.__plugin__ + " Daemon has been idle for 10 seconds. Going to sleep. zzzzzzzz "
						time.sleep(0.5)
						waiting = 2
					continue
				if self.__dbg__ > 0:
					print self.__plugin__ + " Daemon EXCEPTION : " + repr(e)

			if waiting:
				continue

			if self.__dbg__ > 1:
				print self.__plugin__ + " Daemon accepted"
			data = self.recv(self.__clientsocket__)

			try:
				data = eval(data)
			except:
				if self.__dbg__ > 0:
					print self.__plugin__ + " Daemon Couldn't evaluate message : " + repr(data)
				data = {"action": "stop"}

			if self.__dbg__ > 1:
				print self.__plugin__ + " Daemon got data: " + str(len(data)) + " - " + str(repr(data))[0:50]

			res = ""
			if data["action"] == "get":
				res = self.sqlGet(data["table"], data["name"])
			elif data["action"] == "get_multi":
				res = self.sqlGetMulti(data["table"], data["name"], data["items"])
			elif data["action"] == "set_multi":
				res = self.sqlSetMulti(data["table"], data["name"], data["data"])
			elif data["action"] == "set":
				res = self.sqlSet(data["table"], data["name"], data["data"])
			elif data["action"] == "lock":
				res = self.lock(data["table"], data["name"])
			elif data["action"] == "unlock":
				res = self.unlock(data["table"], data["name"])

			if len(res) > 0:
				if self.__dbg__ > 1:
					print self.__plugin__ + " Daemon got response: " + str(len(res))  + " - " + str(repr(res))[0:50]
				self.send(self.__clientsocket__, repr(res))

			idle_since = time.time()
			if self.__dbg__ > 1:
				print self.__plugin__ + " Daemon done"

		if self.__dbg__ > 0:
			print self.__plugin__ + " Daemon Closing down"
		self.__conn__.close()
		print self.__plugin__ + " Daemon Closed"

	def recv(self, sock):
		data = "   "
		idle = True
		temp = ""
		if self.__dbg__ > 2:
			print self.__plugin__ + " recv "
		i = 0
		start = time.time()
		while data[len(data)-2:] != "\r\n" or not idle:
			try:
				if idle:
					recv_buffer = sock.recv(4096)
					idle = False
					i += 1
					#if self.__dbg__ > 2:
					#	print self.__plugin__ + " recv got data  : " + str(i) + " - " + repr(idle) + " - " + str(len(data)) + " + " + str(len(recv_buffer)) + " | " + repr(recv_buffer)[len(recv_buffer) -5:]
					data += recv_buffer
					start = time.time()
				elif not idle:
					if data[len(data)-2:] == "\r\n":
						sock.send("COMPLETE\r\n" + ( " " * ( 15 - len("COMPLETE\r\n") ) ) )
						idle = True
						if self.__dbg__ > 2:
							print self.__plugin__ + " recv sent COMPLETE " + str(i)
					elif len(recv_buffer) > 0:
						sock.send("ACK\r\n" + ( " " * ( 15 - len("ACK\r\n") )) )
						idle = True
						if self.__dbg__ > 2:
							print self.__plugin__ + " recv sent ACK " + str(i)
					recv_buffer = ""
					#print self.__plugin__ + " recv status " + repr( not idle) + " - " + repr(data[len(data)-2:] != "\r\n")
					
			except socket.error, e:
				if not e.errno in [ 10035, 35 ]:
					print self.__plugin__ + " recv except error " + repr(e)

				if e.errno in [ 22 ]: # We can't fix this.
					return ""

				if start + 10 < time.time():
					if self.__dbg__ > 0:
						print self.__plugin__ + " recv over time"
					break
		if self.__dbg__ > 2:
			print self.__plugin__ + " recv done "
		return data.strip()

	def send(self, sock, data):
		idle = True
		status = ""
		if self.__dbg__ > 2:
			print self.__plugin__ + " send : " + str(len(data)) + " - " + repr(data)[0:20]
		i = 0
		start = time.time()
		while len(data) > 0 or not idle:
			send_buffer = " "
			try:
				if idle:
					if len(data) > 4096:
						send_buffer = data[:4096]
					else:
						send_buffer = data + "\r\n"

					result = sock.send(send_buffer)
					i += 1
					idle = False
					start = time.time()
				elif not idle:
					status = ""
					while status.find("COMPLETE\r\n") == -1 and status.find("ACK\r\n") == -1:
						status = sock.recv(15)
						i -= 1

					idle = True
					if len(data) > 4096:
						data = data[4096:]
					else:
						data = ""

					#print self.__plugin__ + " send Got response " + str(i) + " - " + str(result) + " == " + str(len(send_buffer)) + " | " + str(len(data)) + " - " + repr(send_buffer)[len(send_buffer)-5:]

			except socket.error, e:
				if e.errno != 10035 and e.errno != 35 and e.errno != 107 and e.errno != 32:
					print self.__plugin__ + " send except error " + repr(e)
				if start + 10 < time.time():
					if self.__dbg__ > 0:
						print self.__plugin__ + " recv over time"
					break;
		if self.__dbg__ > 2:
			print self.__plugin__ + " send done " 
		return status.find("COMPLETE\r\n") > -1

	def lock(self, table, name): # This is NOT atomic
		if self.__dbg__ > 0:
			print self.__plugin__ + " lock " + name
		locked = True
		curlock = self.sqlGet(table, name)
		if curlock.strip():
			if float(curlock) < self.__daemon_start_time__:
				if self.__dbg__ > 0:
					print self.__plugin__ + " lock removing stale lock."
				if self.sql2:
					self.__curs__.execute("DELETE FROM " + table + " WHERE name = %s", ( name, ) )
				elif self.sql3:
					self.__curs__.execute("DELETE FROM " + table + " WHERE name = ?", ( name, ) )
				self.__conn__.commit()
				locked = False
		else:
			locked = False

		if not locked:
			if self.sql2:
				self.__curs__.execute("INSERT INTO " + table + " VALUES ( %s , %s )", ( name, time.time()) )
			elif self.sql3:
				self.__curs__.execute("INSERT INTO " + table + " VALUES ( ? , ? )", ( name, time.time()) )
			self.__conn__.commit()
			if self.__dbg__ > 0:
				print self.__plugin__ + " lock locked: " + name
			return "true"

		if self.__dbg__ > 0:
			print self.__plugin__ + " lock failed for : " + name
		return "false"

	def unlock(self, table, name):
		if self.__dbg__ > 0:
			print self.__plugin__ + " unlock " + name	

		self.checkTable(table)
		if self.sql2:
			self.__curs__.execute("DELETE FROM " + table + " WHERE name = %s", ( name, ) )
		elif self.sql3:
			self.__curs__.execute("DELETE FROM " + table + " WHERE name = ?", ( name, ) )
		self.__conn__.commit()
		if self.__dbg__ > 0:
			print self.__plugin__ + " unlock done"
		return "true"


	def sqlSetMulti(self, table, pre, inp_data):
		if self.__dbg__ > 1:
			print self.__plugin__ + " sqlSetMulti " + table + " - " + pre + " - " + str(len(inp_data)) #repr(inp_data)) #[0:20]

		self.checkTable(table)
		for name in inp_data:
			if self.sqlGet(table, pre + name).strip():
				if self.__dbg__ > 2:
					print self.__plugin__ + " sqlSetMulti Update : " + pre + name
				if self.sql2:
					self.__curs__.execute("UPDATE " + table + " SET data = %s WHERE name = %s", ( inp_data[name], pre + name ))
				elif self.sql3:
					self.__curs__.execute("UPDATE " + table + " SET data = ? WHERE name = ?", ( inp_data[name], pre + name ))
			else:
				if self.__dbg__ > 2:
					print self.__plugin__ + " sqlSetMulti Insert  " + pre + name
				if self.sql2:
					self.__curs__.execute("INSERT INTO " + table + " VALUES ( %s , %s )", ( pre + name, inp_data[name]) )
				elif self.sql3:
					self.__curs__.execute("INSERT INTO " + table + " VALUES ( ? , ? )", ( pre + name, inp_data[name]) )

		self.__conn__.commit()
		if self.__dbg__ > 0:
			print self.__plugin__ + " sqlSetMulti done"
		return ""

	def sqlGetMulti(self, table, pre, items):
		if self.__dbg__ > 0:
			print self.__plugin__ + " sqlGetMulti " + pre

		self.checkTable(table)
		ret_val = []
		for name in items:
			if self.__dbg__ > 2:
				print self.__plugin__ + " sqlGetMulti : " + pre + name
			if self.sql2:
				self.__curs__.execute("SELECT data FROM " + table + " WHERE name = %s", ( pre + name))
			elif self.sql3:
				self.__curs__.execute("SELECT data FROM " + table + " WHERE name = ?", ( pre + name,))

			result = ""
			for row in self.__curs__:
				if self.__dbg__ > 3:
					print self.__plugin__ + " sqlGetMulti adding : " + str(repr(row[0]))[0:20]
				result = row[0]
			ret_val += [result]
		if self.__dbg__ > 2:
				print self.__plugin__ + " sqlGetMulti returning : " + repr(ret_val)
		return ret_val

	def sqlSet(self, table, name, data):
		if self.__dbg__ > 2:
			print self.__plugin__ + " sqlSet " + name + str(repr(data))[0:20]

		self.checkTable(table)
		if self.sqlGet(table, name).strip():
			#print self.__plugin__ + " sqlSet Update : " + data
			if self.sql2:
				self.__curs__.execute("UPDATE " + table + " SET data = %s WHERE name = %s", ( data, name ))
			elif self.sql3:
				self.__curs__.execute("UPDATE " + table + " SET data = ? WHERE name = ?", ( data, name ))
		else:
			#print self.__plugin__ + " sqlSet Insert  "
			if self.sql2:
				self.__curs__.execute("INSERT INTO " + table + " VALUES ( %s , %s )", ( name, data) )
			elif self.sql3:
				self.__curs__.execute("INSERT INTO " + table + " VALUES ( ? , ? )", ( name, data) )
		self.__conn__.commit()

		if self.__dbg__ > 2:
			print self.__plugin__ + " sqlSet done"
		return ""

	def sqlGet(self, table, name):
		if self.__dbg__ > 2:
			print self.__plugin__ + " sqlGet " + name

		self.checkTable(table)
		if self.sql2:
			self.__curs__.execute("SELECT data FROM " + table + " WHERE name = %s", ( name))
		elif self.sql3:
			self.__curs__.execute("SELECT data FROM " + table + " WHERE name = ?", ( name,))

		for row in self.__curs__:
			if self.__dbg__ > 2:
				print self.__plugin__ + " sqlGet returning : " + str(repr(row[0]))[0:20]
			return row[0]
		if self.__dbg__ > 2:
				print self.__plugin__ + " sqlGet returning empty"
		return " "

	def checkTable(self, table):
		try:
			self.__curs__.execute("create table " + table + " (name text unique, data text)")
			self.__conn__.commit()
			if self.__dbg__ > 0:
				print self.__plugin__ + " checkTable created new table"
		except:
			if self.__dbg__ > 2:
				print self.__plugin__ + " checkTable passed"




__workersByName = {}
def run_async(func, *args, **kwargs):
    from threading import Thread
    worker = Thread(target = func, args = args, kwargs = kwargs)
    __workersByName[worker.getName()] = worker
    worker.start()
    return worker

def run():
	s = StorageServer()
	print " StorageServer Module loaded RUN : " + str(len(__workersByName)) + " - " + repr(__workersByName)
	if len(__workersByName) > 1:
		print s.__plugin__ + " Starting Child already exists"
		#waitForWorkersToDie(1)
		return False
	print s.__plugin__ + " Starting server"
	s.run()
	return True


if __name__ == "__main__": 	
	run()
#elif False:
	#run_async(run)
