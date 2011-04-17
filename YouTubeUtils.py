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

import sys, os, string
import xbmc

class YouTubeUtils:
	__settings__ = sys.modules[ "__main__" ].__settings__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	
	VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
	plugin_thumbnail_path = os.path.join( __settings__.getAddonInfo('path'), "thumbnails" )
	
	# This function raises a keyboard for user input
	def getUserInput(self, title = "Input", default="", hidden=False):
		result = None

		# Fix for when this functions is called with default=None
		if not default:
			default = ""
		
		keyboard = xbmc.Keyboard(default, title)
		keyboard.setHiddenInput(hidden)
		keyboard.doModal()
		
		if keyboard.isConfirmed():
			result = keyboard.getText()
		
		return result
	
	# Converts the request url passed on by xbmc to the plugin into a dict of key-value pairs  
	def getParameters(self, parameterString):
		commands = {}
		splitCommands = parameterString[parameterString.find('?')+1:].split('&')
		
		for command in splitCommands: 
			if (len(command) > 0):
				splitCommand = command.split('=')
				key = splitCommand[0]
				value = splitCommand[1]
				commands[key] = value
		
		return commands
	
	# This function implements a horrible hack related to python 2.4's terrible unicode handling
	def makeAscii(self, str):
		try:
			return str.encode('ascii')
		except:
			if self.__dbg__:
				print self.__plugin__ + " makeAscii hit except on : " + repr(str)
			s = ""
			for i in str:
				try:
					i.encode("ascii")
				except:
					continue
				else:
					s += i
			return s

	# Shows a more user-friendly notification
	def showMessage(self, heading, message):
		duration = ([5, 10, 15, 20, 25, 30][int(self.__settings__.getSetting( 'notification_length' ))]) * 1000
		xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % ( heading, message, duration) )

	# Resolves the full thumbnail path for the plugins skins directory
	def getThumbnail( self, title ):
		if (not title):
			title = "DefaultFolder.png"
		
		thumbnail = os.path.join( sys.modules[ "__main__" ].__plugin__, title + ".png" )
		
		if ( not xbmc.skinHasImage( thumbnail ) ):
			thumbnail = os.path.join( self.plugin_thumbnail_path, title + ".png" )
			if ( not os.path.isfile( thumbnail ) ):
				thumbnail = "DefaultFolder.png"	
		
		return thumbnail
	
	def arrayToPipeDelimitedString(self, input):
		pipedItems = ""
		for item in input:
			pipedItems += item + "|"
		return pipedItems
		
if __name__ == '__main__':	
	sys.exit(0);