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

import sys, urllib, urllib2, re, socket, json, cookielib
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

	__cj__ = cookielib.LWPCookieJar()
	__opener__ = urllib2.build_opener(urllib2.HTTPCookieProcessor(__cj__))
	urllib2.install_opener(__opener__)
	
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
				(result, status) = self._httpLogin(True)

				if status == 200:
					(result, status) = self._apiLogin()
				
				if status == 200:
					self.showErrorMessage(self.__language__(30031), result, 303)
				else:
					self.showErrorMessage(self.__language__(30609), result, status)
		
		xbmc.executebuiltin( "Container.Refresh" )

	def _apiLogin(self, error = 0):
		if self.__dbg__:
			print self.__plugin__ + " _apiLogin - errors: " + str(error)
		
		uname = self.__settings__.getSetting( "username" )
		passwd = self.__settings__.getSetting( "user_password" )
		
		self.__settings__.setSetting('auth', "")
		self.__settings__.setSetting('nick', "")
		
		if ( uname == "" or passwd == "" ):
			if self.__dbg__:
				print self.__plugin__ + " _apiLogin no username or password set "
			return ( "", 0 )

		url = "https://accounts.google.com/o/oauth2/auth?client_id=208795275779.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=http%3A%2F%2Fgdata.youtube.com&response_type=code"
		ret = self._fetchPage({ "link": url, "no-language-cookie": "true" })
		#print self.__plugin__ + " _apiLogin : " + repr(ret)

		newurl = re.compile('<form action="(.*?)" method="POST">').findall(ret["content"])
		if len(newurl) == 0:
			if self.__dbg__:
				print self.__plugin__ + " _apiLogin no form method : " + repr(ret)
			return ( "", 0)

		state_wrapper = re.compile('<input type="hidden" id="state_wrapper" name="state_wrapper" value="(.*?)">').findall(ret["content"])
		if len(state_wrapper) == 0:
			if self.__dbg__:
				print self.__plugin__ + " _apiLogin no state_wrapper "
			return ( "", 0)
		
		submit_approve_access = re.compile('<input id="submit_approve_access" name="submit_approve_access" type="submit" tabindex="1" value="(.*?)" class="').findall(ret["content"])
		if len(submit_approve_access) == 0:
			if self.__dbg__:
				print self.__plugin__ + " _apiLogin no submit_approve_access "
			return ( "", 0)

		url_data = { "state_wrapper": state_wrapper[0],
			     "submit_approve_access": submit_approve_access[0]}
		ret = self._fetchPage({ "link": newurl[0], "url_data": url_data, "no-language-cookie": "true" })

		code = re.compile('code=(.*)</title>').findall(ret['content'])
		if len(code) == 0:
			if self.__dbg__:
				print self.__plugin__ + " _apiLogin no 2-factor confirmation code found"
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
		#print self.__plugin__ + " _apiLogin3 : " + repr(oauth)
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
				print self.__plugin__ + " _apiLogin done: " + uname
			return ( self.__language__(30030), 200 )
		
		if self.__dbg__:
			print self.__plugin__ + " _apiLogin default return. failing. " 
		return ( self.__language__(30609), 303 )
	
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


		if self.__dbg__:
			print self.__plugin__ + " _httpLogin step 1"
		ret = self._fetchPage({ "link": "http://www.youtube.com/"})
		newurl = self.parseDOM(ret["content"], { "name": "a", "class": "end", "return": "href"})
		if len(newurl) == 0:
			return ( "", 0)

		if self.__dbg__:
			print self.__plugin__ + " _httpLogin step 2 : "+ repr(newurl)
		ret = self._fetchPage({ "link": newurl[0]})

		newurl = self.parseDOM(ret["content"].replace("\n", " "), { "name": "form", "id": "id", "id-match": "gaia_loginform", "return": "action"})
		rmShown = re.compile('<input type="hidden" name=\'rmShown\' value="(.*?)" />').findall(ret["content"])
		#cont = re.compile('<input type="hidden" name="continue" id="continue"\n           value="(.*?)" /> ').findall(ret["content"])
		#cont2 = self.parseDOM(ret["content"].replace("\n", " "), { "name": "input", "id": "id", "id-match": "continue", "return": "value"})
		cont = ["http://www.youtube.com/signin?action_handle_signin=true&amp;nomobiletemp=1&amp;hl=en_US&amp;next=%2F"]
		uilel = re.compile('<input type="hidden" name="uilel" id="uilel"\n           value="(.*?)" />').findall(ret["content"])
		dsh = re.compile('<input type="hidden" name="dsh" id="dsh"\n           value="(.*?)" />').findall(ret["content"])
		galx = re.compile('Set-Cookie: GALX=(.*);Path=/accounts;Secure').findall(str(ret["header"]))

		if len(galx) == 0 or len(cont) == 0 or len(uilel) == 0 or len(dsh) == 0 or len(rmShown) == 0 or len(newurl) == 0:
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin missing values for login form " + repr(galx) + repr(cont) + repr(uilel) + repr(dsh) + repr(rmShown) + str(len(newurl))
			return ( "", 0)

		galx = galx[0]
		url_data = { "pstMsg": "0",
			     "ltmpl": "sso",
			     "dnConn": "",
			     "continue": cont[0],
			     "service": "youtube",
			     "uilel": uilel[0],
			     "dsh": dsh[0],
			     "hl": "en_US",
			     "timeStmp": "",
			     "secTok": "",
			     "GALX": galx,
			     "Email": uname,
			     "Passwd": pword,
			     "PersistentCookie": "yes",
			     "rmShown": rmShown[0],
			     "signin": "Sign in",
			     "asts": ""
			}

		if self.__dbg__:
			print self.__plugin__ + " _httpLogin step 3 : " + repr(url_data)
		ret = self._fetchPage({ "link": newurl[0], "no-language-cookie": "true", "url_data": url_data });

		# Login to youtube
		newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])

		if len(newurl): # Normal login
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin: Normal login"
			newurl = newurl[0].replace("&amp;", "&")

			# We need to do this twice now.

			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 4 - normal login"
			ret = self._fetchPage({ "link": newurl});

			# Login to youtube
			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				if self.__dbg__:
					print self.__plugin__ + " _httpLogin: Couldn't get new url"
				return ( "", 0)

			newurl = newurl[0].replace("&amp;", "&")
			
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 5 - normal login"
			ret = self._fetchPage({ "link": newurl, "no-language-cookie": "true" })
		elif ret["content"].find("smsToken") > -1:
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

			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 4 - 2-factor login"
			ret = self._fetchPage({ "link": "https://www.google.com/accounts/SmsAuth?persistent=yes", "url_data": url_data, "no-language-cookie": "true" })
			
			error = self.parseDOM(ret['content'], { "name": "div", "class": "error smaller", "content": "true"})
			if len(error) > 0:
				error = error[0]
				error = urllib.unquote(error[0:error.find("<")]).replace("&#39;", "'")
				return ( error.strip(), 303)
			
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

			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 5 - 2-factor login"
			ret = self._fetchPage({ "link": "https://www.google.com/accounts/ServiceLoginAuth?service=youtube", "url_data": url_data, "no-language-cookie": "true"})

			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				return ("", 0)
			
			newurl = newurl[0].replace("&amp;", "&").replace("http%25253A%252F", "http%253A%252F") # Google has an extra 25 in their code.

			if self.__dbg__:
				print self.__plugin__ + " new_url3: " + newurl

			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 6 - 2-factor login"
			ret = self._fetchPage({ "link": newurl});

			if self.__dbg__:
				print self.__plugin__ + " new_url4: " + repr(ret)
			
			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(ret["content"])
			if len(newurl) == 0:
				return ("", 0)
			newurl = urllib.unquote(newurl[0])

			if self.__dbg__:
				print self.__plugin__ + " _httpLogin step 7 - 2-factor login"
			ret = self._fetchPage({ "link": newurl, "no-language-cookie": "true"});
		else:
			error = self.parseDOM(ret['content'], { "name": "div", "class": "errormsg", "content": "true"})
			if len(error) > 0:
				error = error[0]
				error = urllib.unquote(error[0:error.find("[")]).replace("&#39;", "'")
				return ( error.strip(), 303)
				if self.__dbg__:
					print self.__plugin__ + " _login couldn't find method to authenticate: " + repr(ret)

			return ( "", 0)

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

