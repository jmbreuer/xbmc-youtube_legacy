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

import urllib, urllib2, re, cookielib

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):  
		return str(headers)

	def http_error_302(self, req, fp, code, msg, headers):
		return str(headers) 
	
class Tester(object):
	login_info =""
	cookie_jar =""
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
		
	urls = {};
	urls['http_login'] = "https://www.google.com/accounts/ServiceLogin?service=youtube"
	urls['http_login_confirmation'] = "http://www.youtube.com/signin?action_handle_signin=true&nomobiletemp=1&hl=en_US&next=/index&hl=en_US&ltmpl=sso"
	urls['gdata_login'] = "https://www.google.com/accounts/ClientLogin"
	urls["test"] = "http://www.youtube.com/verify_age?next_url=http%3A//www.youtube.com/watch%3Fv%3DO-77ElyvRxI"
				
	def _httpLogin(self):
		uname = "SmokeyTester51"
		pword = "Farscape47"
		
		if ( uname == "" and pword == "" ):
			return ""
										
		self.cookie_jar = cookielib.LWPCookieJar()
		
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
		urllib2.install_opener(opener)

		# Get GALX
		url = urllib2.Request(urllib.unquote("https://www.google.com/accounts/ServiceLogin?service=youtube"))
		url.add_header('User-Agent', self.USERAGENT)

		try:
			con = urllib2.urlopen(url)
			header = con.info()
			galx = re.compile('Set-Cookie: GALX=(.*);Path=/accounts;Secure').findall(str(header))[0]

			cont = urllib.unquote("http%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26nomobiletemp%3D1%26hl%3Den_US%26next%3D%252Findex&hl=en_US&ltmpl=sso")
			
			params = urllib.urlencode({'GALX': galx,
						   'Email': uname,
						   'Passwd': pword,
						   'PersistentCookie': 'yes',
						   'continue': cont})

			# Login to Google
			url = urllib2.Request('https://www.google.com/accounts/ServiceLoginAuth?service=youtube', params)
			url.add_header('User-Agent', self.USERAGENT)
			
			con = urllib2.urlopen(url)
			result = con.read()

			newurl = re.compile('<meta http-equiv="refresh" content="0; url=&#39;(.*)&#39;"></head>').findall(result)[0].replace("&amp;", "&")
			url = urllib2.Request(newurl)
			url.add_header('User-Agent', self.USERAGENT)
			
			# Login to youtube
			con = urllib2.urlopen(newurl)
			
			# Save cookiefile in settings
			cookies = repr(self.cookie_jar)
			start = cookies.find("name='LOGIN_INFO', value='") + len("name='LOGIN_INFO', value='")
			login_info = cookies[start:cookies.find("', port=None", start)]
			self.login_info = login_info
		except:
			print " _httplogin failed "
	
	def _verifyAge(self):
		url = self.urls["test"]
				
		request = urllib2.Request(url)
		request.add_header('User-Agent', self.USERAGENT)
		request.add_header('Cookie', 'LOGIN_INFO=' + self.login_info )
		con = urllib2.urlopen(request)
		result = con.read()
		
		# <div id="verify-age-actions">
		next_url_start = result.find('"next_url" value="') + len('"next_url" value="')
		next_url_stop = result.find('">',next_url_start)
		next_url = result[next_url_start:next_url_stop]
		
		print "next_url=" + next_url
		
		session_token_start = result.find("'XSRF_TOKEN': '") + len("'XSRF_TOKEN': '")
		session_token_stop = result.find("',",session_token_start) 
		session_token = result[result.find("'XSRF_TOKEN': '"):session_token_stop + 10]
		print "session_token=" + session_token
		session_token = result[session_token_start:session_token_stop]
		print "session_token=" + session_token
				
		request = urllib2.Request(url)
		request.add_header('User-Agent', self.USERAGENT)
		request.add_header('Cookie', 'LOGIN_INFO=' + self.login_info )
		request.add_header("Content-Type","application/x-www-form-urlencoded")
		values = urllib.urlencode( { "next_url": next_url, "action_confirm": "1", "session_token":session_token })
		
		print "post content: " + values
		con = urllib2.urlopen(request, values)
		new_url = con.geturl()
		result = con.read()
		con.close()
		
		#If verification is success full new url must look like: 'http://www.youtube.com/index?has_verified=1'
		print "New url: " + repr(new_url)
		
if (__name__ == "__main__" ):
	tester = Tester()
	tester._httpLogin()
	tester._verifyAge()