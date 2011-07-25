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

import sys, urllib, re, socket, json
import xbmc
import YouTubeUtils
import YouTubeCore

# ERRORCODES:
# 0 = Ignore
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class YouTubeLogin(YouTubeCore.YouTubeCore, YouTubeUtils.YouTubeUtils):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__

	APIKEY = "AI39si6hWF7uOkKh4B9OEAX-gK337xbwR9Vax-cdeF9CF9iNAcQftT8NVhEXaORRLHAmHxj6GjM-Prw04odK4FxACFfKkiH9lg";
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
		
	urls = {};
	urls['http_login'] = "https://www.google.com/accounts/ServiceLogin?service=youtube"
	urls['http_login_confirmation'] = "http://www.youtube.com/signin?action_handle_signin=true&nomobiletemp=1&hl=en_US&next=/index&hl=en_US&ltmpl=sso"
	urls['gdata_login'] = "https://www.google.com/accounts/ClientLogin"
	
	def __init__(self):
		timeout = self.__settings__.getSetting( "timeout" )
		if not timeout:
			timeout = "5"
		socket.setdefaulttimeout(float(timeout))
		return None
	
	def login(self, params = {}):
		self.__settings__.openSettings()
		
		if self.__settings__.getSetting("username") and self.__settings__.getSetting( "user_password" ):
			refreshed = False
			if self.__settings__.getSetting( "oauth2_refresh_token" ):
				if self.__dbg__:
					print self.__plugin__ + " login refreshing token: " + str(refreshed)
				refreshed = self._oRefreshToken()
				if self.__dbg__:
					print self.__plugin__ + " login refreshing token: " + str(refreshed)

			if not refreshed:
				if self.__dbg__:
					print self.__plugin__ + " login token not refresh, or new uname or password"

				self.__settings__.setSetting("oauth2_access_token","")
				self.__settings__.setSetting("oauth2_refresh_token","")
				self.__settings__.setSetting("oauth2_expires at", "")
				self.__settings__.setSetting("nick","")
				(http_login, status) = self._httpLogin(True)
				result = "_httpLogin"

				if status == 200:
					(result, status) = self._apiLogin()
				
				if status == 200:
					self.showErrorMessage(self.__language__(30031), result, 303)
				else:
					self.showErrorMessage(self.__language__(30609), result, status)
		
		xbmc.executebuiltin( "Container.Refresh" )

	def _apiLogin(self, error = 0):
                if self.__dbg__:
                        print self.__plugin__ + " _login - errors: " + str(error)
                        
                uname = self.__settings__.getSetting( "username" )
                passwd = self.__settings__.getSetting( "user_password" )
                
                self.__settings__.setSetting('auth', "")
                self.__settings__.setSetting('nick', "")
                
                if ( uname == "" or passwd == "" ):
                        if self.__dbg__:
                                print self.__plugin__ + " _login no username or password set "
                        return ( "", 0 )

                url = "https://accounts.google.com/o/oauth2/auth?client_id=208795275779.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=http%3A%2F%2Fgdata.youtube.com&response_type=code"
                ret = self._fetchPage({ "link": url})
		#print self.__plugin__ + " _login : " + repr(ret)

		newurl = re.compile('<form action="(.*?)" method="POST">').findall(ret["content"])
		if len(newurl) == 0:
                        if self.__dbg__:
                                print self.__plugin__ + " _login no form method "
			return ( "", 0)

		state_wrapper = re.compile('<input type="hidden" id="state_wrapper" name="state_wrapper" value="(.*?)">').findall(ret["content"])
		if len(state_wrapper) == 0:
                        if self.__dbg__:
                                print self.__plugin__ + " _login no state_wrapper "
			return ( "", 0)

		submit_approve_access = re.compile('<input id="submit_approve_access" name="submit_approve_access" type="submit" tabindex="1" value="(.*?)" class="').findall(ret["content"])
		if len(submit_approve_access) == 0:
                        if self.__dbg__:
                                print self.__plugin__ + " _login no submit_approve_access "
			return ( "", 0)

		url_data = { "state_wrapper": state_wrapper[0],
			     "submit_approve_access": submit_approve_access[0]}
		ret = self._fetchPage({ "link": newurl[0], "url_data": url_data})

                code = re.compile('code=(.*)</title>').findall(ret['content'])
		if len(code) == 0:
                        if self.__dbg__:
                                print self.__plugin__ + " _login no 2-factor confirmation code found"
			return ( "", 0)
		code = code[0]

                url = "https://accounts.google.com/o/oauth2/token"
		url_data = { "client_id": "208795275779.apps.googleusercontent.com",
			     "client_secret": "sZn1pllhAfyonULAWfoGKCfp",
			     "code": code,
			     "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
			     "grant_type": "authorization_code"}
                ret = self._fetchPage({ "link": url, "url_data": url_data})

		oauth = json.loads(ret["content"])
		#print self.__plugin__ + " _login3 : " + repr(oauth)
		self.__settings__.setSetting("oauth2_access_token", oauth["access_token"])
		self.__settings__.setSetting("oauth2_refresh_token", oauth["refresh_token"])

		# use token

		# curl https://www.google.com/m8/feeds/contacts/default/full?oauth_token=1/fFAGRNJru1FTz70BzhT3Zg
                                        
                if len(oauth) > 0:
			#self.__settings__.setSetting("oauth2_expires at", oauth["expires_in"] + current time. ) 
			self.__settings__.setSetting("oauth2_access_token", oauth["access_token"])
			self.__settings__.setSetting('auth', oauth["access_token"])
			self.__settings__.setSetting("oauth2_refresh_token", oauth["refresh_token"])

                        if self.__dbg__:
                                print self.__plugin__ + " _login done: " + uname
                        return ( self.__language__(30030), 200 )
                                        
		if self.__dbg__:
			print self.__plugin__ + " _login default return. failing. " 
                return ( self.__language__(30609), 303 )

	def createUrl(self, params):
		url = ""
		return url
		
	def _httpLogin(self, new = False, error = 0):
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin errors: " + str(error)
		result = ""
		status = 200
		
		uname = self.__settings__.getSetting( "username" )
		pword = self.__settings__.getSetting( "user_password" )
		
		if uname == "" and pword == "":
			return ( "", 303)

		if new:
			self.__settings__.setSetting( "login_info", "" )
		elif self.__settings__.getSetting( "login_info" ) != "":
			if self.__dbg__:
				print self.__plugin__ + " returning existing login info: " + self.__settings__.getSetting( "login_info" )
			return ( self.__settings__.getSetting( "login_info" ), 200)
		
		ret = self._fetchPage({ "link": "https://www.google.com/accounts/ServiceLogin?uilel=3&service=youtube&passive=true&continue=http%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26nomobiletemp%3D1%26hl%3Den_US%26next%3D%252F&hl=en_US&ltmpl=sso"})

		galx = re.compile('Set-Cookie: GALX=(.*);Path=/accounts;Secure').findall(str(ret["header"]))
		if len(galx) == 0:
			return ( "", 0)
		galx = galx[0]

		if self.__dbg__:
			print self.__plugin__ + " _httpLogin: getting new login_info"

		# Login to Google
		cont = urllib.unquote("http%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26nomobiletemp%3D1%26hl%3Den_US%26next%3D%252Findex&hl=en_US&ltmpl=sso")
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin: cont_url = " + cont

                ret = self._fetchPage({ "link": "https://www.google.com/accounts/ServiceLoginAuth?service=youtube", "url_data": {'GALX': galx, 'Email': uname, 'Passwd': pword, 'PersistentCookie': 'yes', 'continue': cont} });

		# Login to youtube
		newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin: newurl " + str(len(newurl)) + " - " + ret["content"]
		if len(newurl) > 0: # Normal login
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin: Normal login"
			newurl = newurl[0].replace("&amp;", "&")

		        # We need to do this twice now.
			ret = self._fetchPage({ "link": newurl});
			# Login to youtube
			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				if self.__dbg__:
					print self.__plugin__ + " _httpLogin: Couldn't get new url"
				return ( "", 0)

			newurl = newurl[0].replace("&amp;", "&")
			
			ret = self._fetchPage({ "link": newurl });		
		elif ret["content"].find("smsToken") > -1:
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin: 2-factor login"
			smsToken = re.compile('<input type="hidden" name="smsToken"\n        value="(.*?)">').findall(ret["content"])
			if len(smsToken) == 0:
				return ( "", 0)

			email = re.compile('<input type="hidden" name="email"\n          value="(.*?)">').findall(ret["content"])
			if len(email) == 0:
				return ( "", 0)

			url_data = { "smsToken": smsToken[0],
				     "PersistentCookie": "yes",
				     "service": "youtube",
				     "smsUserPin" : self.getUserInput(self.__language__(30627)),
				     "smsVerifyPin" : "Verify",
				     "timeStmp" : "",
				     "secTok" : "",
				     "email" : email[0]}

			ret = self._fetchPage({ "link": "https://www.google.com/accounts/SmsAuth?persistent=yes", "url_data": url_data })

			smsToken = re.compile('<input type="hidden" name="smsToken" value="(.*?)">').findall(ret["content"])
			if len(smsToken) == 0:
				return ( "", 0)
			cont = re.compile('<input type="hidden" name="continue" value="(.*?)">').findall(ret["content"])
			if len(cont) == 0:
				return ( "", 0)

			url_data = { "smsToken": smsToken[0],
				     "continue": cont[0],
				     "PersistentCookie": "yes",
				     "service": "youtube",
				     "GALX": galx}
			ret = self._fetchPage({ "link": "https://www.google.com/accounts/ServiceLoginAuth?service=youtube", "url_data": url_data })

			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				return ("", 0)
                        newurl = newurl[0].replace("&amp;", "&").replace("http%25253A%252F", "http%253A%252F") # Google has an extra 25 in their code.

                        if self.__dbg__:
                                print self.__plugin__ + " new_url3: " + newurl
                        ret = self._fetchPage({ "link": newurl});

                        if self.__dbg__:
                                print self.__plugin__ + " new_url4: " + repr(ret)
			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				return ("", 0)
                        newurl = urllib.unquote(newurl[0])

                        ret = self._fetchPage({ "link": newurl});
		else:
                        if self.__dbg__:
                                print self.__plugin__ + " _login couldn't find method to authenticate: " + str(ret["content"].find("smsToken"))

		if self.__dbg__:
			print self.__plugin__ + " _httpLogin: Logged in. Parsing data."

		nick = ""
		if ret["content"].find("USERNAME', ") > 0:
			nick = ret["content"][ret["content"].find("USERNAME', ") + 12:]
			nick = nick[:nick.find('")')]
		
		if nick:
			self.__settings__.setSetting("nick", nick)
		else:
			status = 303
			print self.__plugin__ + " _httpLogin failed to get usename from youtube"
		
		# Save cookiefile in settings
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin scanning cookies for login info: "
		
		login_info = ""
		cookies = repr(self.__cj__)
			
		if cookies.find("name='LOGIN_INFO', value='") > 0:
			start = cookies.find("name='LOGIN_INFO', value='") + len("name='LOGIN_INFO', value='")
			login_info = cookies[start:cookies.find("', port=None", start)]
		
		if login_info:
			self.__settings__.setSetting( "login_info", login_info )
		else:
			status = 303
		
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin done : " + str(status) + " - " + login_info
		
		result = self.__settings__.getSetting( "login_info" )
		
		return (result, status)

