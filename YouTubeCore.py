import sys, urllib, urllib2, re, os, cookielib
from xml.dom.minidom import parse, parseString

# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class YouTubeCore(object):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	__dbgv__ = False
	
	APIKEY = "AI39si6hWF7uOkKh4B9OEAX-gK337xbwR9Vax-cdeF9CF9iNAcQftT8NVhEXaORRLHAmHxj6GjM-Prw04odK4FxACFfKkiH9lg";
	USERAGENT = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)";

	#===============================================================================
	#
	# External functions called by YouTubeNavigation.py
	#
	# return MUST be a tupple of ( result[string or dict], status[int] )
	# 
	#===============================================================================
	
	def __init__(self):
		#enable debug
		#self.__settings__.setSetting( "debug", "True" )
		return None

	def login(self):
		if self.__dbg__:
			print self.__plugin__ + " login"
		uname = self.__settings__.getSetting( "username" )
	        passwd = self.__settings__.getSetting( "user_password" )
		self.__dbg__ = True

		url = urllib2.Request("https://www.google.com/youtube/accounts/ClientLogin");
		url.add_header('User-Agent', self.USERAGENT)
		url.add_header('GData-Version', 2)

		if ( uname == "" and passwd == "" ):
			if self.__dbg__:
				print self.__plugin__ + " login no username or password set "
			return ( "", 200 )
	
		headers = urllib.urlencode({'Email': uname, 'Passwd': passwd, 'service': 'youtube', 'source': 'test'});
		try:
			con = urllib2.urlopen(url, headers);
		
			value = con.read();
			result = re.compile('Auth=(.*)\nYouTubeUser=(.*)').findall(value);
			if len(result) > 0:
				( auth, nick ) = result[0]
				self.__settings__.setSetting('auth', auth)
				self.__settings__.setSetting('nick', nick)
				self._httpLogin()
				if self.__dbg__:
					print self.__plugin__ + " login done: " + nick
				return ( "", 200 )
                except urllib2.HTTPError, e:
			error = str(e)
			if self.__dbg__:
				print self.__plugin__ + " login failed, hit except: " + error
			if e.code == 403:
				return ( self.__language__(30621), 303 )
			return ( error, 303 )	
		except:
			if self.__dbg__:
				print self.__plugin__ + " login failed uncaught exception"
			return ( self.__language__(30616), 500 );
	
	def search(self, query, page = "0" ):
		if self.__dbg__:
                        print self.__plugin__ + " search: " + repr(query) + " - page: " + repr(page)
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		safe_search = ("none", "moderate", "strict" ) [int( self.__settings__.getSetting( "safe_search" ) ) ]
		url = urllib2.Request("http://gdata.youtube.com/feeds/api/videos?" + urllib.urlencode({'q': query}) + "&safeSearch=" + safe_search + "&start-index=" + str( per_page * int(page) + 1) + "&max-results=" + repr(per_page) );
		url.add_header('User-Agent', self.USERAGENT);
		url.add_header('GData-Version', 2)
		try:
			con = urllib2.urlopen(url);
			result = self._getvideoinfo(con.read())
			con.close()
			if len(result) > 0:
				if self.__dbg__:
					print self.__plugin__ + " search done :" + str(len(result))
				return (result, 200)
			else:
				if self.__dbg__:
                                        print self.__plugin__ + " search done with no results"
				return (self.__language__(30601), 303)
                except urllib2.HTTPError, e:
			error = str(e)
			if self.__dbg__:
				print self.__plugin__ + " search failed, hit except: " + error
			return ( error, 303 )
		except:
			if self.__dbg__:
				print self.__plugin__ + " search failed with uncaught exception"
			return ( [], 500 )

	def feeds(self, feed, page = "0" ):
		if self.__dbg__:
			print self.__plugin__ + " feeds : " + repr(feed) + " page: " + repr(page)
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		if (feed.find("%s") > 0 ):
			time = ( "all_time", "today", "this_week", "this_month") [ int(self.__settings__.getSetting( "feed_time" ) ) ]
			feed = feed % time
		
		if ( feed.find("?") == -1 ):
			feed += "?"
		else:
			feed += "&"
			feed += "start-index=" + str( per_page * int(page) + 1) + "&max-results=" + repr(per_page)
			
		if (feed.find("standardfeeds") > 0):
			region = ('', 'AU', 'BR', 'CA', 'CZ', 'FR', 'DE', 'GB', 'NL', 'HK', 'IN', 'IE', 'IL', 'IT', 'JP', 'MX', 'NZ', 'PL', 'RU', 'KR', 'ES','SE', 'TW', 'US', 'ZA' )[ int( self.__settings__.getSetting( "region_id" ) ) ]
			if (region):
				feed = feed.replace("/standardfeeds/", "/standardfeeds/"+ region + "/")
		
		url = urllib2.Request(feed); # Implement start-index here                            
		url.add_header('User-Agent', self.USERAGENT);
		url.add_header('GData-Version', 2)
		try:
			con = urllib2.urlopen(url);
			result = self._getvideoinfo(con.read())
			if self.__dbgv__:
				print self.__plugin__ + " feeds result: " + repr(result)
			con.close()
			if len(result) > 0:
				if self.__dbg__:
                                        print self.__plugin__ + " feeds done : " + str(len(result))
				return ( result, 200 )
			else:
				if self.__dbg__:
                                        print self.__plugin__ + " feeds done with no results"
				return (self.__language__(30602), 303)
                except urllib2.HTTPError, e:
			error = str(e)
			if self.__dbg__:
				print self.__plugin__ + " feed failed, hit except: " + error
			return ( error, 303 )										
		except:
			if self.__dbg__:
				print self.__plugin__ + " feed failed with uncaught exception "
			return ( [], 500 )
	
	def list(self, feed, page = "0", retry = True):
		if self.__dbg__:
			print self.__plugin__ + " list: " + repr(feed) + " - page: " + repr(page)
		auth = self._getAuth()
		if ( not auth ):
                        if self.__dbg__:
                                print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
	
		if ( feed.find("?") == -1 ):
                        feed += "?"
                else:
                        feed += "&"
                feed += "start-index=" + str( per_page * int(page) + 1) + "&max-results=" + repr(per_page)
		feed = feed.replace(" ", "+")
		url = urllib2.Request(feed)
		url.add_header('User-Agent', self.USERAGENT)
		url.add_header('GData-Version', 2)
		url.add_header('Authorization', 'GoogleLogin auth=' + auth);
		url.add_header('X-GData-Key', 'key=' + self.APIKEY);
		try:
                        con = urllib2.urlopen(url);
			result = self._getvideoinfo(con.read())
			if self.__dbgv__:
				print self.__plugin__ + " list result: " + repr(result)
			con.close();
			if len(result) > 0:
				if self.__dbg__:
                                        print self.__plugin__ + " list done :" + str(len(result))
				return (result, 200)
			else:
				if self.__dbg__:
                                        print self.__plugin__ + " list done with no results"
				return (self.__language__(30602), 303)

		except urllib2.HTTPError, e:
			error = str(e)
			if ( error.find("401") > 0 and retry ):
				if self.login():
					if self.__dbg__:
						print self.__plugin__ + " list done: retrying"
					return self.list(feed, page, False)
				else:
					if self.__dbg__:
						print self.__plugin__ + " list done: retrying failed because login failed"
					return ( error, 303 )
			if self.__dbg__:
                                        print self.__plugin__ + " list except: " + error
			return ( error, 303 )
                except:
			if self.__dbg__:
                                        print self.__plugin__ + " list uncaught exception"
                        return ( [], 500 )

        def delete_favorite(self, delete_url):
		return self._youTubeDel(delete_url)
	
	def remove_contact(self, contact_id):
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/contacts/%s" % contact_id
		return self._youTubeDel(delete_url)

	def remove_subscription(self, editurl):
		return self._youTubeDel(editurl)

	def add_contact(self, contact_id):
		url = "http://gdata.youtube.com/feeds/api/users/default/contacts"
		add_request = '<?xml version="1.0" encoding="UTF-8"?> <entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:username>%s</yt:username></entry>' % contact_id
		return self._youTubeAdd(url, add_request)
		
	def add_favorite(self, video_id):
		url = "http://gdata.youtube.com/feeds/api/users/default/favorites"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom"><id>%s</id></entry>' % (video_id)
		return self._youTubeAdd(url, add_request)

	def add_subscription(self, user_id):
		url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"> <category scheme="http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat" term="user"/><yt:username>%s</yt:username></entry>' % (user_id)
		return self._youTubeAdd(url, add_request)

	def playlists(self, link, page = '0', retry = True):
		if self.__dbg__:
			print self.__plugin__ + " playlists " + repr(link) + " - page: " + repr(page)
		auth = self._getAuth()
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		if ( link.find("?") == -1 ):
                        link += "?"
                else:
                        link += "&"
                link += "start-index=" + str( per_page * int(page) + 1) + "&max-results=" + repr(per_page)

		url = urllib2.Request(link)
                url.add_header('User-Agent', self.USERAGENT)
                url.add_header('GData-Version', 2)
                url.add_header('Authorization', 'GoogleLogin auth=' + auth);
                url.add_header('X-GData-Key', 'key=' + self.APIKEY);
		
                try:
                        con = urllib2.urlopen(url);
                except urllib2.HTTPError, e:
                        error = str(e)
			if ( error.find("401") > 0 and retry ):
				if self.login():
					if self.__dbg__:
						print self.__plugin__ + " playlist retrying"
					return self.playlists(link, page, False)
				else:
					if self.__dbg__:
						print self.__plugin__ + " playlist retrying failed because login failed"
					return ( error, 303 )
				
			if self.__dbg__:
				print self.__plugin__ + " playlist except: " + error
			return ( error, 303 )
		except:
                        if self.__dbg__:
                                        print self.__plugin__ + " playlist uncaught exception"
                        return ( [], 500 )

		result = con.read()
		if self.__dbgv__:
			print self.__plugin__ + " playlist result: " + repr(result)
		con.close()
		dom = parseString(result);
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		next = "false"

		#find out if there are more pages
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = "true"
					break
				
		playobjects = [];
		for node in entries:
			video = {};
			video['published'] = node.getElementsByTagName("published").item(0).firstChild.nodeValue;
			video['Title'] = str(node.getElementsByTagName("title").item(0).firstChild.nodeValue.replace('Activity of : ', '').replace('Videos published by : ', '')).encode( "utf-8" );
			video['summary'] = self._getNodeValue(node, 'summary', 'Unknown')
			video['content'] = self._getNodeAttribute(node, 'content', 'src', 'FAIL')
			video['playlistId'] = self._getNodeValue(node, 'yt:playlistId', '')
			if node.getElementsByTagName("link"):
				link = node.getElementsByTagName("link")
				for i in range(len(link)):
					if link.item(i).getAttribute('rel') == 'edit':
						video['editurl'] = link.item(i).getAttribute('href')
																
			video['next'] = next

			playobjects.append(video);
			if self.__dbg__:
                                        print self.__plugin__ + " playlist done : " + str(len(playobjects))
		return ( playobjects, 200 );
	
	def downloadVideo(self, path, videoid):
		if self.__dbg__:
			print self.__plugin__ + " downloadVideo : " + repr(path) + " - videoid : " + repr(videoid)
 		( video, status )  = self.construct_video_url(videoid);
		
		if ( status == 200 ):
			path = self.__settings__.getSetting( "downloadPath" )
			try:
				if self.__dbg__:
					print self.__plugin__ + " downloadVideo stream_map: " + video['stream_map']
					
				if video['stream_map'] == "True":
					print self.__plugin__ + " downloadVideo stream_map not implemented in downloadVideo"
					return (self.__language__(30620), 303)
				else:
					(filename, header) = urllib.urlretrieve(video['video_url'], "%s/%s.flv" % ( path,video['Title']))
					self.__settings__.setSetting( "vidstatus-" + videoid, "1" )
			except urllib2.HTTPError, e:
				if self.__dbg__:
                                        print self.__plugin__ + " downloadVideo except: " + str(e)
				return ( str(e), 303 )
			except:
				if self.__dbg__:
                                        print self.__plugin__ + " downloadVideo uncaught exception"
				return (self.__language__(30606), 303)
		else:
			if self.__dbg__:
				print self.__plugin__ + " downloadVideo got error from construct_video_url: [%s] %s" % ( status, video)
			return (video, status)

		if self.__dbg__:
			print self.__plugin__ + " downloadVideo done"
		return ( video, status )


	def construct_video_url(self, videoid, encoding = 'utf-8'):
		if self.__dbg__:
			print self.__plugin__ + " construct_video_url : " + repr(videoid)

		video = self._get_details(videoid)
		video['stream_map'] = 'False'

		if not video:
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url failed because of missing video from _get_details"
			return ("", 500)
		
		hd_quality = int(self.__settings__.getSetting( "hd_videos" ))

		if ( 'apierror' not in video):
			try:
				link = 'http://www.youtube.com/watch?v=' +videoid + "&safeSearch=none&restriction=US&hl=en_US"
				request = urllib2.Request(link);
				request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)');
				con = urllib2.urlopen(request);
				htmlSource = con.read();
				if self.__dbgv__:
					print self.__plugin__ + " construct_video_url result: " + repr(htmlSource)
				con.close()

				fmtSource = re.findall('"fmt_url_map": "([^"]+)"', htmlSource);
				if not fmtSource: 
					fmtSource = re.findall('"fmt_stream_map": "([^"]+)"', htmlSource);
					if (fmtSource) :
						video['stream_map'] = 'True'

				if not fmtSource:
					# Video might be censored, try again with a cookie.
					# Get a new LOGIN_INFO cookie (for some reason the old one will fail) and use request url again.
					if ( self._httpLogin() ):
						request.add_header('Cookie', 'LOGIN_INFO=' + self.__settings__.getSetting( "login_info" ) )
					else:                                                                                           
						if self.__dbg__:
							print self.__plugin__ + " construct_video_url failed because login failed"
						return (self.__language__(30609), 303)
					
					con = urllib2.urlopen(request);
					htmlSource = con.read();
					con.close()

					fmtSource = re.findall('"fmt_url_map": "([^"]+)"', htmlSource)
					if not fmtSource:
						fmtSource = re.findall('"fmt_stream_map": "([^"]+)"', htmlSource);
						if (fmtSource) :
							video['stream_map'] = 'True'
					
					if not fmtSource:
						print self.__plugin__ + " IMPORTANT : " + link
						if self.__dbg__:
							print self.__plugin__ + " construct_video_url failed, empty fmtSource after trying with cookie"
						#print htmlSource
						return (self.__language__(30618), 303)
						  
				fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|');

				links = {};
				video_url = False
				breaker = False
				print self.__plugin__ + " construct_video_url: stream_map : " + video['stream_map']
				if (video['stream_map'] == 'True'):
					if self.__dbg__:
						print self.__plugin__ + " construct_video_url: stream map"
					for fmt_url in fmt_url_map:
						if (len(fmt_url) > 7 and fmt_url.find(":\\/\\/") > 0):
							if (fmt_url.rfind(',') > fmt_url.rfind('\/id\/')):
								final_url = fmt_url[:fmt_url.rfind(',')]
								quality = final_url[final_url.rfind('\/itag\/') + 8:]
								links[int(quality)] = final_url.replace('\/','/')
							else :
								final_url = fmt_url
								quality = final_url[final_url.rfind('\/itag\/') + 8:]
								links[int(quality)] = final_url.replace('\/','/')
				
				else:
					if self.__dbg__:
						print self.__plugin__ + " construct_video_url: non stream map" 
					for fmt_url in fmt_url_map:
						if (len(fmt_url) > 7):
							if (fmt_url.rfind(',') > fmt_url.rfind('&id=')):
								final_url = fmt_url[:fmt_url.rfind(',')]
								quality = final_url[final_url.rfind('itag=') + 5:]
								quality = quality[:quality.find('&')]
								links[int(quality)] = final_url.replace('\/','/')
							else :
								final_url = fmt_url
								quality = final_url[final_url.rfind('itag=') + 5:]
								quality = quality[:quality.find('&')]
								links[int(quality)] = final_url.replace('\/','/')
				
				get = links.get
				
				# SD videos are default, but we go for the highest res
				if (get(35)):
					video_url = get(35)
				elif (get(34)):
					video_url = get(34)
				elif (get(18)):
					video_url = get(18)
				elif (get(5)):
					video_url = get(5)
					 
				if (hd_quality > 0): #<-- 720p
					if (get(22)):
						video_url = get(22)
				if (hd_quality > 1): #<-- 1080p
					if (get(37)):
						video_url = get(37)
						
				if ( not video_url ):
					if self.__dbg__:
						print self.__plugin__ + " construct_video_url failed, video_url not set"
					return (self.__language__(30607), 303)
				video['video_url'] = video_url;

				if self.__dbg__:
					print self.__plugin__ + " construct_video_url done"
				return (video, 200);
			except:
				if self.__dbg__:
					print self.__plugin__ + " construct_video_url uncaught exception"
					print self.__plugin__ + " ERROR-except: %s::%s (%d) - %s" % (self.__class__.__name__  , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				return ('', 500)
		else:
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url, got apierror: " + video['apierror']
			return (video['apierror'], 303)

	def arrayToPipe(self, input):
		pipedItems = ""
		for item in input:
			pipedItems += item + "|"
		return pipedItems

	def scrapeVideos(self, feed, params):
		if self.__dbg__:
			print self.__plugin__ + " scrapeVideos: " + repr(feed) + " - params: - " + repr(params)
		get = params.get
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]

		oldVideos = self.__settings__.getSetting("recommendedVideos")

		if ( page == 0 or oldVideos == ""):
			( videos, result)  = self._scrapeYouTubeData(feed)
			if (result == 200):
				self.__settings__.setSetting("recommendedVideos", self.arrayToPipe(videos))									
			else:
				return ( video, result )
		else:
			videos = oldVideos.split("|")
		
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		else:
			next = 'false'

		subitems = videos[(per_page * page):(per_page * (page + 1))]
		ytobjects = []
                failed = []
		counter = 0
		link = ""

		for item in subitems:
			# Dashes break with google, fetch all video's with a dash in the videoid seperatly.
			if (item.find('-') == -1):
				link += item + "|"
				counter += 1;
			else:
				failed.append(item)
				
			if ( counter > 9 or item == subitems[len(subitems)-1] ):
				link += "&restriction=US"
				url = urllib2.Request("http://gdata.youtube.com/feeds/api/videos?q=" + link);
				url.add_header('User-Agent', self.USERAGENT);
				url.add_header('GData-Version', 2)

				try:
					con = urllib2.urlopen(url);
					value = con.read()
					con.close()
				except urllib2.HTTPError, e:
					if self.__dbg__:
						print self.__plugin__ + " scrapeVideos except: " + str(e)
					return ( str(e), 303 )
				except:
					return ( "", 500 )
				
				temp = self._getvideoinfo(value)
				ytobjects += temp[0:counter]
				counter = 0
				link = ""

		for item in failed:
			videoitem = self._get_details(item)
			if videoitem:
				ytobjects.append(videoitem)
		
		if (len(ytobjects) > 0):
			ytobjects[len(ytobjects)-1]['next'] = next

		if self.__dbg__:
			print self.__plugin__ + " scrapeVideos done"
		return ( ytobjects, 200 )

    #===============================================================================
	#
    # Internal functions to YouTubeCore.py
	#
	# Return should be value(True for bool functions), or False if failed.
	#
	# False MUST be handled properly in External functions
    #
    #===============================================================================

	def _getAuth(self):
		if self.__dbg__:
			print self.__plugin__ + " _getAuth"

		auth = self.__settings__.getSetting( "auth" )

		if ( auth ):
			if self.__dbg__:
                                print self.__plugin__ + " _getAuth returning stored auth"
			return auth
		else:
			if self.login():
				if self.__dbg__:
					print self.__plugin__ + " _getAuth returning new auth"

				return self.__settings__.getSetting( "auth" )
			else:
				if self.__dbg__:
					print self.__plugin__ + " _getAuth failed because login failed"
				return False
	
	def _youTubeAdd(self, url, add_request, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _youTubeAdd: " + repr(url) + " add_request " + repr(add_request)
		auth = self._getAuth()
		if ( not auth ):
                        if self.__dbg__:
                                print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		try:
			request = urllib2.Request(url, add_request)
			request.add_header('Authorization', 'GoogleLogin auth=%s' % auth)
			request.add_header('X-GData-Client', "")
			request.add_header('X-GData-Key', 'key=%s' % self.APIKEY)
			request.add_header('Content-Type', 'application/atom+xml')
			request.add_header('Content-Length', str(len(add_request)))
			request.add_header('GData-Version', 2)
			usock = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			error = str(e)
			if ( error.find("201") > 0):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd: Done"
				return ( "", 200)
			elif (error.find("503") > -1):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd: " + self.__language__(30615)
				return ( self.__language__(30615), 303 )
			elif ( error.find("401") > 0 and retry ):
				if self.login():
					if self.__dbg__:
						print self.__plugin__ + " _youTubeAdd: retry"
					return self.youTubeAdd(url, add_request, False)
				else:
					if self.__dbg__:
						print self.__plugin__ + " _youTubeAdd: " + error
					return ( error, 303 )
			else:
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd: " + error
				return ( error, 303 )
	
	def _youTubeDel(self, delete_url, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _youTubeDel: " + delete_url

		auth = self._getAuth()
		if ( not auth ):
                        if self.__dbg__:
                                print self.__plugin__ + " _youTubeDel auth wasn't set "
			return ( self.__language__(30609) , 303 )

		try:
			headers = {}
			headers['Authorization'] = 'GoogleLogin auth=%s' % (auth)
			headers['X-GData-Client'] = ""
			headers['X-GData-Key'] = 'key=%s' % self.APIKEY
			headers['Content-Type'] = 'application/atom+xml'
			headers['Host'] = 'gdata.youtube.com'
			headers['GData-Version'] = '2'
			import httplib
			conn = httplib.HTTPConnection('gdata.youtube.com')
			conn.request('DELETE', delete_url, headers=headers)
			response = conn.getresponse()
			if (response.status == 200):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeDel: done"
				return ( "", 200 )
			elif (response.status == 401 and retry):
				if self.login():
					if self.__dbg__:
						print self.__plugin__ + " _youTubeDel: retrying"
					return self._youTubeDel(delete_url, False)
				else:
					resp = str(response.read())
					if self.__dbg__:
						print self.__plugin__ + " _youTubeDel: " + resp
					return ( resp, 303 )
			else:
				resp = str(response.read())
				if self.__dbg__:
					print self.__plugin__ + " _youTubeDel: [%s] %s" % ( response.status, resp )
				return ( resp, 303 )
		except urllib2.HTTPError, e:
			if self.__dbg__:
                                print self.__plugin__ + " _youTubeDel except: " + str(e)
			return ( str(e), 303 )
		except:
			if self.__dbg__:
                                print self.__plugin__ + " _youTubeDel uncaught exception"
			return ( "" , 500)
	
	def _getNodeAttribute(self, node, tag, attribute, default = ""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).hasAttribute(attribute):
				return node.getElementsByTagName(tag).item(0).getAttribute(attribute)

		return default;
	
	def _getNodeValue(self, node, tag, default = ""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).firstChild:
				return node.getElementsByTagName(tag).item(0).firstChild.nodeValue
		
		return default;

	# try catch status this
	def _getvideoinfo(self, value):
		if self.__dbg__:
			print self.__plugin__ + " _getvideoinfo: " + str(len(value))
		dom = parseString(value);
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		next = "false"

		#find out if there are more pages
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = "true"
					break

		#construct list of video objects					
		ytobjects = [];
		for node in entries:
			# THIS IS FUCKLY AND NEEDS TO BE FIXED
			video = {};
			if not node.getElementsByTagName("media:title").item(0):
				print self.__plugin__ + ' _getvideoinfo media:title missing';
				continue;
			
			# http://code.google.com/intl/en/apis/youtube/2.0/reference.html#youtube_data_api_tag_yt:state <- more reason codes
			# requesterRegion - This video is not available in your region. <- fails
			# limitedSyndication - Syndication of this video was restricted by its owner. <- works
			
			if node.getElementsByTagName("yt:state").item(0):
				if node.getElementsByTagName("yt:state").item(0).hasAttribute('name'):
					# What to do about failed?
					state = node.getElementsByTagName("yt:state").item(0).getAttribute('name')

	        		if ( state == 'deleted' or state == 'rejected'):
	        			continue
	        		else:
	        			#print self.__plugin__ + "/ERROR: DO NOT REMOVE THIS DEBUG CODE"
	        			#print self.__plugin__ + "/ERROR: A video marked as rejected or failed was just fetched, check if it can play and handle appropriatly"
	        			#print self.__plugin__ + "/ERROR: Name: " + node.getElementsByTagName("yt:state").item(0).getAttribute('name')
	        			#print node.getElementsByTagName("yt:state").item(0).getAttribute('name');
							
					if node.getElementsByTagName("yt:state").item(0).hasAttribute('reasonCode'):
						reason = node.getElementsByTagName("yt:state").item(0).getAttribute('reasonCode')
						value = node.getElementsByTagName("yt:state").item(0).firstChild.nodeValue;
						if ( reason != 'limitedSyndication' ):
							video['reasonCode'] = reason
							video['reasonValue'] = value
							print self.__plugin__ + "/ERROR reasonCode: " + reason + " - " + value

			video['videoid'] = self._getNodeValue(node, "yt:videoid", "missing")

			# this really shouldn't be needed
			if ( video['videoid'] == "missing" ):
				video['videolink'] = node.getElementsByTagName("link").item(0).getAttribute('href')
				match = re.match('.*?v=(.*)\&.*', video['videolink'])
				if match:
					video['videoid'] = match.group(1)
				else:
					continue

			#http://wiki.xbmc.org/?title=InfoLabels
			
			video['Title'] = self._getNodeValue(node, "media:title", "Unknown Title").encode('utf-8') # Convert from utf-16 to combat breakage
			video['Plot'] = self._getNodeValue(node, "media:description", "Unknown Plot").encode( "utf-8" )
			video['Date'] = self._getNodeValue(node, "published", "Unknown Date").encode( "utf-8" )
			video['user'] = self._getNodeValue(node, "name", "Unknown Name").encode( "utf-8" )
			video['Studio'] = self._getNodeValue(node, "media:credit", "Unknown Uploader").encode( "utf-8" )
			duration = int(self._getNodeAttribute(node, "yt:duration", 'seconds', '0'))
			video['Duration'] = "%02d:%02d" % ( duration / 60, duration % 60 )
			video['Rating'] = float(self._getNodeAttribute(node,"gd:rating", 'average', "0.0"))
			#video['viewCount'] = self._getNodeAttribute(node, "yt:statistics", 'viewCount', "0") <- Not used by xbmc
			video['Genre'] = self._getNodeAttribute(node, "media:category", "label", "Unknown Genre").encode( "utf-8" )

			if node.getElementsByTagName("link"):
				link = node.getElementsByTagName("link")
				for i in range(len(link)):
					if link.item(i).getAttribute('rel') == 'edit':
						video['editurl'] = link.item(i).getAttribute('href')

			video['thumbnail'] = "http://i.ytimg.com/vi/" + video['videoid'] + "/0.jpg"
			
			overlay = self.__settings__.getSetting( "vidstatus-" + video['videoid'] )

			if overlay:
				video['Overlay'] = int(overlay)
				
			video['next'] = next

			ytobjects.append(video);
		if self.__dbg__:
			print self.__plugin__ + " _getvideoinfo done"
		return ytobjects;

	def _get_details(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " _get_details: " + repr(videoid)
		url = urllib2.Request("http://gdata.youtube.com/feeds/api/videos/" + videoid);
		url.add_header('User-Agent', self.USERAGENT);
		url.add_header('GData-Version', 2)
		try:
			con = urllib2.urlopen(url);
			result = self._getvideoinfo(con.read())
			con.close()
			if len(result) == 0:
				if self.__dbg__:
					print self.__plugin__ + " _get_details result was empty"
				return False
			else:
				if self.__dbg__:
					print self.__plugin__ + " _get_details done"
				return result[0];
		except urllib2.URLError, err:
			if self.__dbg__:
                                print self.__plugin__ + " _get_details except: " + str(err)

			if (err.code == 403):
				# 403 == Forbidden
				# Happens on "removed by user" and "This video has been removed due to terms of use violation."
				return False

			video = {}
			video['Title'] = "Error"
			video['videoid'] = videoid
			video['thumbnail'] = "Error"
			video['video_url'] = False

			if (err.code == 503):
				if self.__dbg__:
                                        print self.__plugin__ + " _get_details exception 503: " + str(err)
				video['apierror'] = self.__language__(30605)
				return video
			else:
				if self.__dbg__:
					print self.__plugin__ + " _get_details uncaught except: [%s] %s" % ( err.code, str(err) )
				video['apierror'] = self.__language__(30606) + str(err.code)
				return video

		except:
			if self.__dbg__:
                                print self.__plugin__ + " _get_details uncaught exception"
			return False
		
		
	def _httpLogin(self):
		if self.__dbg__:
			print self.__plugin__ + " _httpLogin"
		uname = self.__settings__.getSetting( "username" )
		pword = self.__settings__.getSetting( "user_password" )
	
		cj = cookielib.LWPCookieJar()
		
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
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
			cookies = repr(cj)
			start = cookies.find("name='LOGIN_INFO', value='") + len("name='LOGIN_INFO', value='")
			login_info = cookies[start:cookies.find("', port=None", start)]
			self.__settings__.setSetting( "login_info", login_info )
			if self.__dbg__:
				print self.__plugin__ + " _httpLogin: Logged in with login_info cookie: " + login_info
			return True
		except:
			if self.__dbg__:
                                print self.__plugin__ + " _httpLogin: uncaught exception"
			return False

	# try except status this.
	def _scrapeYouTubeData(self, feed, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _scrapeYouTubeData: " + repr(feed)

		login_info = self.__settings__.getSetting( "login_info" )
                if ( not login_info ):
			if ( self._httpLogin() ):
				login_info = self.__settings__.getSetting( "login_info" )
		
		url = urllib2.Request(feed + "&hl=en")
                url.add_header('User-Agent', self.USERAGENT)
		url.add_header('Cookie', 'LOGIN_INFO=' + login_info)

		try:
			con = urllib2.urlopen(url)
			result = con.read()
			if self.__dbgv__:
				print self.__plugin__ + " _scrapeYouTubeData result: " + repr(result)
			con.close()

			videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=grec_browse" class=').findall(result);

			if len(videos) == 0:
				videos = re.compile('<div id="reco-(.*)" class=').findall(result);

			if ( len(videos) == 0 and retry ):
				self._httpLogin()
				videos = self._scrapeYouTubeData(feed, False)
			if self.__dbg__:
				print self.__plugin__ + " _scrapeYouTubeData done"
			return ( videos, 200 )
                except urllib2.HTTPError, e:
			if self.__dbg__:
                                print self.__plugin__ + " _scrapeYouTubeData exception: " + str(e)
			return ( self.__language__(30619), "303" )
		except:
			if self.__dbg__:
				print self.__plugin__ + " _scrapeYouTubeData uncaught exception"
			return ( "", 500 )
	
if __name__ == '__main__':
	core = YouTubeCore();
#	core.scrape();
	sys.exit(0);
