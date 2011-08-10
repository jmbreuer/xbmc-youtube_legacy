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
	__dbg__ = True
	
	__path__ = os.path.join( xbmc.translatePath( "special://database" ), 'commoncache.db')
	__socket__ = ""
	__clientscoket__ = False

	sql2 = False
	sql3 = False
	if repr(sys.modules).find("sqlite3") > -1:
		sql3 = True
	else: # Verify this better
		sql2 = True

	if sql2:
		__conn__ = sqlite.connect(__path__)
	elif sql3:
		__conn__ = sqlite3.connect(__path__, check_same_thread=False)

	__curs__ = __conn__.cursor()

	def run(self):
		self.__plugin__ = "StorageServer"
		print self.__plugin__ + " Storage Server starting " + self.__path__
		try:
			self.__curs__.execute("create table items (name text uniq, data text)")
			self.__conn__.commit()
		except:
			if self.__dbg__:
				print self.__plugin__ + " Database already exists"

                if sys.platform == "win32":
			port = 59994
			self.__socket__ = (socket.gethostname(), port)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')
			#self.__socket__ = "/home/tobias/.xbmc/temp/commoncache.socket"
			if xbmcvfs.exists(self.__socket__):
				if self.__dbg__:
					print self.__plugin__ + " Unlinking stale socket file"
				os.unlink(self.__socket__)	
			sock = socket.socket(socket.AF_UNIX)

		sock.bind(self.__socket__)
		sock.listen(1)
		sock.setblocking(0)
		
		start = time.time()
		i = 0
		while not xbmc.abortRequested:
			if i == 0:
				if self.__dbg__:
					print self.__plugin__ + " Daemon accepting"
				i = 1
			self.__clientsocket__ = False
			try:
				(self.__clientsocket__, address) = sock.accept()
				start = time.time()
			except socket.error, e:
				if e.errno == 11 or e.errno == 10035 or e.errno == 35:
					continue
				if self.__dbg__:
					print self.__plugin__ + " Daemon EXCEPTION : " + repr(e)

			if not self.__clientsocket__:
				continue

			if self.__dbg__:
				print self.__plugin__ + " Daemon accepted"

			data = self.recv(self.__clientsocket__)

			try:
				data = eval(data)
			except:
				if self.__dbg__:
					print self.__plugin__ + " Daemon Couldn't evaluate message : " + repr(data)
				data = {"action": "stop"}

			if self.__dbg__:
				print self.__plugin__ + " Daemon got data: " + str(len(data)) + " - " + str(repr(data))[0:50]

			res = ""
			if data["action"] == "get":
				res = self.sqlGet(data["name"])
			elif data["action"] == "set":
				res = self.sqlSet(data["name"], data["data"])
			elif data["action"] == "lock":
				res = self.lock(data["name"])
			elif data["action"] == "unlock":
				res = self.unlock(data["name"])

			if len(res) > 0:
				if self.__dbg__:
					print self.__plugin__ + " Daemon got response: " + str(len(res))  + " - " + str(repr(res))[0:50]
				self.send(self.__clientsocket__, repr(res))

			if self.__dbg__:
				print self.__plugin__ + " Daemon done"

		if self.__dbg__:
			print self.__plugin__ + " Daemon Closing down"
		self.__curs__.close()
		self.__conn__.close()
		print self.__plugin__ + " Daemon Closed"

	def recv(self, sock):
		data = "   "
		idle = True
		temp = ""
		if self.__dbg__:
			print self.__plugin__ + " recv "
		i = 0
		start = time.time()
		while data[len(data)-2:] != "\r\n" or not idle:
			try:
				if idle:
					recv_buffer = sock.recv(4096)
					idle = False
					i += 1
					#if self.__dbg__:
					#	print self.__plugin__ + " recv got data  : " + str(i) + " - " + repr(idle) + " - " + str(len(data)) + " + " + str(len(recv_buffer)) + " | " + repr(recv_buffer)[len(recv_buffer) -5:]
					data += recv_buffer
					start = time.time()
				elif not idle:
					if data[len(data)-2:] == "\r\n":
						sock.send("COMPLETE\r\n" + ( " " * ( 15 - len("COMPLETE\r\n") ) ) )
						idle = True
						if self.__dbg__:
							print self.__plugin__ + " recv sent COMPLETE " + str(i)
					elif len(recv_buffer) > 0:
						sock.send("ACK\r\n" + ( " " * ( 15 - len("ACK\r\n") )) )
						idle = True
						if self.__dbg__:
							print self.__plugin__ + " recv sent ACK " + str(i)
					recv_buffer = ""
					#print self.__plugin__ + " recv status " + repr( not idle) + " - " + repr(data[len(data)-2:] != "\r\n")
					
			except socket.error, e:
				if not e.errno in [ 10035, 35 ]:
					print self.__plugin__ + " recv except error " + repr(e)

				if e.errno in [ 22 ]: # We can't fix this.
					return ""

				if start + 10 < time.time():
					if self.__dbg__:
						print self.__plugin__ + " recv over time"
					break
		if self.__dbg__:
			print self.__plugin__ + " recv done "
		return data.strip()

	def send(self, sock, data):
		idle = True
		status = ""
		if self.__dbg__:
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
					if self.__dbg__:
						print self.__plugin__ + " recv over time"
					break;
		if self.__dbg__:
			print self.__plugin__ + " send done " 
		return status.find("COMPLETE\r\n") > -1

	def lock(self, name): # This is NOT atomic
		if self.__dbg__:
			print self.__plugin__ + " lock " + name
		locked = True
		curlock = self.sqlGet(name)
		if self.__dbg__:
			print self.__plugin__ + " lock curlock " + repr(curlock)
		if curlock.strip():
			if float(curlock) + 10 < time.time():
				if self.__dbg__:
					print self.__plugin__ + " lock was older than 10 seconds, considered stale, removing"
				if self.sql2:
					self.__curs__.execute("DELETE FROM items WHERE name = %s", ( name, ) )
				elif self.sql3:
					self.__curs__.execute("DELETE FROM items WHERE name = ?", ( name, ) )
				self.__conn__.commit()
				locked = False
		else:
			locked = False

		if not locked:
			if self.sql2:
				self.__curs__.execute("INSERT INTO items VALUES ( %s , %s )", ( name, time.time()) )
			elif self.sql3:
				self.__curs__.execute("INSERT INTO items VALUES ( ? , ? )", ( name, time.time()) )
			self.__conn__.commit()
			return "true"

		if self.__dbg__:
			print self.__plugin__ + " lock done"
		return "false"

	def unlock(self, name):
		if self.__dbg__:
			print self.__plugin__ + " unlock " + name
		if self.sql2:
			self.__curs__.execute("DELETE FROM items WHERE name = %s", ( name, ) )
		elif self.sql3:
			self.__curs__.execute("DELETE FROM items WHERE name = ?", ( name, ) )
		self.__conn__.commit()
		if self.__dbg__:
			print self.__plugin__ + " unlock done"
		return "true"

	def sqlSet(self, name, data):
		if self.__dbg__:
			print self.__plugin__ + " sqlSet " + name + str(repr(data))[0:20]
		if self.sqlGet(name).strip():
			#print self.__plugin__ + " sqlSet Update : " + data
			if self.sql2:
				self.__curs__.execute('UPDATE items SET data = %s WHERE name = %s', ( data, name ))
			elif self.sql3:
				self.__curs__.execute('UPDATE items SET data = ? WHERE name = ?', ( data, name ))
		else:
			#print self.__plugin__ + " sqlSet Insert  "
			if self.sql2:
				self.__curs__.execute("INSERT INTO items VALUES ( %s , %s )", ( name, data) )
			elif self.sql3:
				self.__curs__.execute("INSERT INTO items VALUES ( ? , ? )", ( name, data) )
		self.__conn__.commit()
		if self.__dbg__:
			print self.__plugin__ + " sqlSet done"
		return ""

	def sqlGet(self, name):
		if self.__dbg__:
			print self.__plugin__ + " sqlGet " + name

		if self.sql2:
			self.__curs__.execute("SELECT data FROM items WHERE name = %s", ( name))
		elif self.sql3:
			self.__curs__.execute("SELECT data FROM items WHERE name = ?", ( name,))

		for row in self.__curs__:
			if self.__dbg__:
				print self.__plugin__ + " sqlGet returning : " + str(repr(row[0]))[0:20]
			return row[0]
		if self.__dbg__:
				print self.__plugin__ + " sqlGet returning empty"
		return " "


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
	print s.__plugin__ + " Starting server run called "
	s.run()
	return True


if __name__ == "__main__": 
	run()
elif False:
	run_async(run)
