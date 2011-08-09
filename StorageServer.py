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
'''

import os, sys, socket, time
import xbmc
try: import xbmcvfs
except: import xbmcvfsdummy as xbmcvfs
try: import sqlite
except: import sqlite3
class StorageServer():

	## MOVE THIS BACK INTO YOUTUBE.
	# Test if it is running, if not, launch it through xbmc.
	# Then we can also give arguments ( ie, do this for mac, do this for windows ).

	#socket.setdefaulttimeout(30)
	#__plugin__ = sys.modules[ "__main__" ].__plugin__
	#__dbg__ = sys.modules[ "__main__" ].__dbg__
	__plugin__ = "StorageClient"
	__dbg__ = True
	
	__path__ = os.path.join( xbmc.translatePath( "special://database" ), 'commoncache.db')
	#__path__ = "/home/tobias/.xbmc/temp/bla.db"
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
	__threads__ = []
	__curs__ = __conn__.cursor()

	def run(self):
		self.__plugin__ = "StorageServer"
		print self.__plugin__ + " Storage Server starting " + self.__path__
		try:
			self.__curs__.execute("create table items (name text uniq, data text)")
			self.__conn__.commit()
		except:
			print self.__plugin__ + " Database already exists"

                if sys.platform == "win32":
			port = 59994
			self.__socket__ = (socket.gethostname(), port)
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')
			#self.__socket__ = "/home/tobias/.xbmc/temp/commoncache.socket"
			if xbmcvfs.exists(self.__socket__):
				print self.__plugin__ + " Unlinking stale socket file"
				os.unlink(self.__socket__)	
			sock = socket.socket(socket.AF_UNIX)

		sock.bind(self.__socket__)
		sock.listen(5)
		sock.setblocking(0)
		
		start = time.time()
		i = 0
		while not xbmc.abortRequested:
			if i == 0:
				print self.__plugin__ + " Daemon accepting"
				i = 1
			#sock.setblocking(0)
			#socket.setdefaulttimeout(30)
			self.__clientsocket__ = False
			try:
				(self.__clientsocket__, address) = sock.accept()
				start = time.time()
			except socket.error, e:
				if start + 300 < time.time():
					print self.__plugin__ + " Daemon EXCEPTION OVER TIME : " + repr(e)
					#exit(0)
				if e.errno == 11 or e.errno == 10035 or e.errno == 35:
					continue
				print self.__plugin__ + " Daemon EXCEPTION : " + repr(e)
				#self.stop()

			if not self.__clientsocket__:
				continue
			print self.__plugin__ + " Daemon accepted"

			data = self.recv(self.__clientsocket__)

			try:
				data = eval(data)
			except:
				print self.__plugin__ + " Daemon Couldn't evaluate message : " + repr(data)
				data = {"action": "stop"}

			print self.__plugin__ + " Daemon got data: " + str(len(data))

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
				print self.__plugin__ + " Daemon got response: " + str(len(res)) + " - " + repr(res)
				self.send(self.__clientsocket__, repr(res))

			print self.__plugin__ + " Daemon done"

		print self.__plugin__ + " Daemon Closing down"
		self.__curs__.close()
		self.__conn__.close()
		print self.__plugin__ + " Daemon Closing release"

	def recv(self, sock):
		data = "   "
		idle = True
		temp = ""
		print self.__plugin__ + " recv "
		i = 0
		while data[len(data)-2:] != "\r\n" or not idle:
			print self.__plugin__ + " recv data : " + str(len(data))
			try:
				if idle:
					temp = sock.recv(4096 * 4096)
					idle = False
					i += 1
					print self.__plugin__ + " recv got data  : " + str(i) + " - " + repr(idle) + " - " + str(len(data)) + " + " + str(len(temp)) + " | " + repr(temp)[len(temp) -5:]
					data += temp
				elif not idle:
					if data[len(data)-2:] == "\r\n":
						sock.send("COMPLETE\r\n" + ( " " * ( 15 - len("COMPLETE\r\n") ) ) )
						idle = True
						print self.__plugin__ + " recv sent COMPLETE " + str(i)
					elif len(temp) > 0:
						print self.__plugin__ + " recv trying to sent ACK " + str(i)
						sock.send("ACK\r\n" + ( " " * ( 15 - len("ACK\r\n") )) )
						idle = True
						print self.__plugin__ + " recv sent ACK " + str(i)
					temp = ""
					print self.__plugin__ + " recv status " + repr( not idle) + " - " + repr(data[len(data)-2:] != "\r\n")
					
			except socket.error, e:
				if e.errno != 10035 and e.errno != 35:
					print self.__plugin__ + " recv except error " + repr(e)
				print self.__plugin__ + " recv except error " + repr(e)
		print self.__plugin__ + " recv DONE " + repr( not idle) + " - " + repr(data[len(data)-2:] != "\r\n")
		return data.strip()

	def send(self, sock, res):
		idle = True
		status = ""
		if len(res) < 100:
			print self.__plugin__ + " send : " + str(len(res)) + " - " + repr(res)
		else:
			print self.__plugin__ + " send : " + str(len(res))

		i = 0
		while len(res) > 0 or not idle:
			#print self.__plugin__ + " send to go " + str(len(res))
			data = " "
			try:
				if idle:
					if len(res) > 4096:
						data = res[:4096]
					else:
						data = res + "\r\n"

					result = sock.send(data)
					i += 1
					idle = False
				elif not idle:
					status = ""
					while status.find("COMPLETE\r\n") == -1 and status.find("ACK\r\n") == -1:
						status = sock.recv(15)
						i -= 1
					print self.__plugin__ + " send waiting for response4 " 

					idle =  True
					if len(res) > 4096:
						res = res[4096:]
					else:
						res = ""

					print self.__plugin__ + " send Got response " + str(i) + " - " + str(result) + " == " + str(len(data)) + " | " + str(len(res)) + " - " + repr(data)[len(data)-5:]

			except socket.error, e:
				if e.errno != 10035 and e.errno != 35 and e.errno != 107 and e.errno != 32:
					print self.__plugin__ + " send except error " + repr(e)
		print self.__plugin__ + " send DONE " +  repr(status) + " - " + repr(idle) + " - " + str(len(res)) + " - " + str(i)
		return status.find("COMPLETE\r\n") > -1

	def lock(self, name): # This is NOT atomic
		#print self.__plugin__ + " lock " + name
		locked = True
		curlock = self.sqlGet(name)
		#print self.__plugin__ + " lock curlock " + repr(curlock)
		if curlock.strip():
			#print self.__plugin__ + " lock curlock " + repr(curlock) + " - cur time " + str(time.time())
			#check timestamp in data.
			if float(curlock) + 10 < time.time():
				#print self.__plugin__ + " lock was older than 10 seconds, considered stale, removing"
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

		#print self.__plugin__ + " lock return"
		return "false"

	def unlock(self, name):
		#print self.__plugin__ + " unlock " + name
		if self.sql2:
			self.__curs__.execute("DELETE FROM items WHERE name = %s", ( name, ) )
		elif self.sql3:
			self.__curs__.execute("DELETE FROM items WHERE name = ?", ( name, ) )
		self.__conn__.commit()
		#print self.__plugin__ + " unlock DONE "
		return " "

	def sqlSet(self, name, data):
		#print self.__plugin__ + " sqlSet " + name
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
		#print self.__plugin__ + " sqlSet commit"
		self.__conn__.commit()
		return ""

	def sqlGet(self, name):
		#print self.__plugin__ + " sqlGet " + name
		if self.sql2:
			self.__curs__.execute("SELECT data FROM items WHERE name = %s", ( name))
		elif self.sql3:
			self.__curs__.execute("SELECT data FROM items WHERE name = ?", ( name,))

		for row in self.__curs__:
			#print self.__plugin__ + " sqlGet returning : " + row[0]
			return row[0]
		return " "

	def stop(self):
		print self.__plugin__ + " Stopping Server"
		self.__conn__.close()
		if sys.platform != "win32":
                        #self.__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')
                        self.__socket__ = "/home/tobias/.xbmc/temp/commoncache.socket"
			os.unlink(self.__socket__)	
		print self.__plugin__ + " Stopping Server Done"
		exit(0)


__workersByName = {}
def run_async(func, *args, **kwargs):
    """
        run_async(func)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object

            E.g.:
            @run_async
            def task1():
                do_something

            @run_async
            def task2():
                do_something_too

            t1 = task1()
            t2 = task2()
            ...
            t1.join()
            t2.join()
    """
    from threading import Thread
    worker = Thread(target = func, args = args, kwargs = kwargs)
    __workersByName[worker.getName()] = worker
    worker.start()
    # TODO: attach post-func decorator to target function and remove thread from __workersByName
    return worker

@run_async
def run():
	s = StorageServer()
	print " StorageServer Module loaded RUN : " + str(len(__workersByName)) + " - " + repr(__workersByName)
	if len(__workersByName) > 1:
		print s.__plugin__ + " Starting Child already exists"
		#waitForWorkersToDie(1)
	print s.__plugin__ + " Starting server run called "
	s.run()
	return True

def stop():
	print " StorageServer Module STOPPING "
	s = StorageServer() 
	for name in __workersByName:
		print " StorageServer Module STOPPING worker : " + repr(name)
		__workersByName[name].join(1)
		print " StorageServer Module STOPPED worker : " + repr(name)
	return s.stop()

def restart():
	#waitForWorkersTxoDie(1)
	@run_async
	def bla():
		s = StorageServer()
		print " StorageServer restart : " + str(len(__workersByName)) + " - " + repr(__workersByName)
		s.run()

def waitForWorkersToDie(timeout=None):
    """
    If the main python thread exits w/o first letting all child threads die, then
    xbmc has a bad habit of coredumping. Certainly not desired from a user experience
    perspective. 
    """
    print ' StorageServer Total threads spawned = %d' % len(__workersByName)
    for workerName, worker in __workersByName.items():
        if worker:
            if worker.isAlive():
		    print ' StorageServer Waiting for thread %s to die...' % workerName
		    worker.join(timeout)
		    if worker.isAlive():
			    # apparently, join timed out
			    print ' StorageServer Thread %s still alive after timeout' % workerName
                    
    print 'Done waiting for threads to die'

if __name__ == "__main__": 
	run()


print " StorageServer Module Loaded "
#run()
