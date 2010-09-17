import sys, urllib, urllib2, re, string, cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import YouTubeCore

class YouTubeScraperCore:	 

	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	core = YouTubeCore.YouTubeCore()
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
	
	urls = {}
	urls['disco_main'] = "http://www.youtube.com/disco" 
	urls['disco_search'] = "http://www.youtube.com/disco?action_search=1&query=%s"
	urls['disco_mix_list'] = "http://www.youtube.com/list_ajax?a=%s&action_get_mixlist=1"
	urls['main'] = "http://www.youtube.com"
	urls['trailers'] = "http://www.youtube.com/trailers?s=tr"
	urls['current_trailers'] = "http://www.youtube.com/trailers?s=trit"
	urls['upcoming_trailers'] = "http://www.youtube.com/trailers?s=tros"
	urls['popular_trailers'] = "http://www.youtube.com/trailers?s=trp"
	urls['recommended'] = "http://www.youtube.com/videos?r=1";
	
	def scrapeRecommended(self, params = {}):
		get = params.get
		url = self.urls["recommended"]
		
		if self.__dbg__:
			print self.__plugin__ + " scrapeVideos: " + url + " - params: - " + repr(params)
		
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		oldVideos = self.__settings__.getSetting("recommendedVideos")
		
		if ( page == 0 or oldVideos == ""):
			( videos, result)  = self._scrapeYouTubeData(url)
			if (result == 200):
				self.__settings__.setSetting("recommendedVideos", self.core.arrayToPipe(videos))									
			else:
				return ( videos, result )
		else:
			videos = oldVideos.split("|")
		
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		else:
			next = 'false'
		
		subitems = videos[(per_page * page):(per_page * (page + 1))]
		
		( ytobjects, status ) = self.core._get_batch_details(subitems)
		
		if status == 200:
			if (len(ytobjects) > 0):
				ytobjects[len(ytobjects)-1]['next'] = next
		
		return (ytobjects, status)
	
	def _scrapeYouTubeData(self, url, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _scrapeYouTubeData: " + url
		result = ""

		login_info = self.__settings__.getSetting( "login_info" )
		if ( not login_info ):
			if ( self.core._httpLogin() ):
				login_info = self.__settings__.getSetting( "login_info" )
		
		url = urllib2.Request(url + "&hl=en")
		url.add_header('User-Agent', self.USERAGENT)
		url.add_header('Cookie', 'LOGIN_INFO=' + login_info)

		try:
			con = urllib2.urlopen(url)
			result = con.read()
			if self.__dbg__:
				print self.__plugin__ + " _scrapeYouTubeData result: " + repr(result)
			con.close()

			videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=grec_browse" class=').findall(result);

			if len(videos) == 0:
				videos = re.compile('<div id="reco-(.*)" class=').findall(result);

			if ( len(videos) == 0 and retry ):
				self.core._httpLogin()
				videos = self._scrapeYouTubeData(url, False)
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
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				print self.__plugin__ + " _scrapeYouTubeData result: " + repr(result)
			return ( "", 500 )
	
	def scrapeTrailersGridFormat (self, page, params = {}):
		get = params.get
		yobjects = []

		list = SoupStrainer(id="popular-column", name="div")
		trailers = BeautifulSoup(page, parseOnlyThese=list)
		
		if (len(trailers) > 0):
			trailer = trailers.div.div
			
			while (trailer != None):
				item ={}
				videoid = trailer.div.a['href']

				if (videoid):
					if (videoid.find("=") > -1):
						videoid = videoid[videoid.find("=")+1:]
					
					item["videoid"] = videoid
					item["thumbnail"] = trailer.div.a.span.img['src'] 
					item["Title"] = trailer.div.a.span.img['title']

					yobjects.append(item)
				trailer = trailer.findNextSibling(name="div", attrs = { 'class':"trailer-cell *vl" })
		
		if (not yobjects):
			return (yobjects, 500)
		
		return (yobjects, 200)
	
	def searchDisco(self, query, params = {}):
		get = params.get
		url = self.urls["disco_search"] % urllib.quote_plus(query)
		print "search url " + url
		page = self._fetchPage(url)
		
		if (page.find("watch?") != -1):
			items = []
			page = page[page.find("a=") + 2:]
			mix_list_id = page[:page.find("&")]
			url = self.urls["disco_mix_list"] % mix_list_id
			page = self._fetchPage(url)
			# TODO: tobias fix this :D
#			
#			list = SoupStrainer(id="quicklist", name="div")
#			ajax = BeautifulSoup(page, parseOnlyThese=list)
#			if (len(ajax) > 0):
#				if (ajax.div["data-active-ajax-url"]):
#					url = self.urls["main"] + ajax.div["data-active-ajax-url"]
#					print "ajax url " + url
#				
#				page = self._fetchPage(url)
#				video_list = SoupStrainer(name="ol")
#				videos = BeautifulSoup(page, parseOnlyThese=video_list)
#				if (len(videos) > 0):
#					video = videos.li
#					while (video != None):
#						videoid = video.a["href"]
#						if (videoid.find("=") > 0):
#							videoid = videoid[videoid.find("=") +1:videoid.find("&")]
#						items.append(videoid)
#						
#						video = video.findNextSibling(name="li", attrs = { 'class':re.compile("^quicklist-item")})
			
			if (items):
				#self.core.playlists(a, page, retry)
				return self.core._get_batch_details(items)
			else:
				if (self.__dbg__):
					print self.__plugin__ + " Disco scraper failed, youtube probably changed their layout"	
		return ([], 303)

		
	def scrapeTrailersListFormat (self, page, params = {}):
		get = params.get		 
		yobjects = []
		
		list = SoupStrainer(id="recent-trailers-container", name="div")
		trailers = BeautifulSoup(page, parseOnlyThese=list)
		
		if (len(trailers) > 0):
			trailer = trailers.div.div
			
			while (trailer != None):
				item ={}
				videoid = trailer.div.div.a['href']

				if (videoid):
					if (videoid.find("=") > -1):
						videoid = videoid[videoid.find("=")+1:]
					item = self.core._get_details(videoid)
					
					if (item):
						item["thumbnail"] = trailer.div.div.a.span.img['src'] 
						yobjects.append(item)
						
				trailer = trailer.findNextSibling(name="div")
		if (not yobjects):
			return (yobjects, 500)
		
		return (yobjects, 200)

	def _fetchPage(self, feed, params = {}):
		url = urllib2.Request(feed)
		url.add_header('User-Agent', self.USERAGENT);
		
		con = urllib2.urlopen(url);
		page = con.read()
		con.close()
		return page
	
	def _get_disco_list(self, playlistid):
		if self.__dbg__:
			print self.__plugin__ + " _get_disco_list : " + playlistid
		link= "http://www.youtube.com/list_ajax?a=" + playlistid + "&amp;action_get_mixlist=1"
		
		url = urllib2.Request(link);
		url.add_header('User-Agent', self.USERAGENT);
		
		try:
			con = urllib2.urlopen(url);
			value = con.read()
			con.close()
			match = re.findall('.*?v=(.*)\&amp;a.*', value)
			if match:
				return self._get_batch_details(match)
			else:
				print self.__plugin__ + " _get_disco_list no match"
		       	return ( self.__language__(30601), 303)
		
		except urllib2.HTTPError, e:
			if self.__dbg__:
				print self.__plugin__ + " _get_disco_list except: " + str(e)
			return ( str(e), 303 )
		except:
			if self.__dbg__:
				print self.__plugin__ + " _get_disco_list caught unknown exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
			return ( "", 500 )
		
	def scrapeDiscoTop25(self, params = {}):
		get = params.get
		url = self.urls["disco_main"]
		page = self._fetchPage(url, params)
		list = SoupStrainer(name="div", attrs = {"class":"popular-message"})
		popular = BeautifulSoup(page, parseOnlyThese=list)
		result = []
		if (len(popular) > 0):
			videos = self.urls["main"] + popular.a["onclick"]
			if (videos.find("&quot;") > 0):
				videos = videos[videos.find("&quot;"):videos.rfind("])")]
				videos = videos.replace("&quot;","")
				videos = videos.replace(" ","")
				items = videos.split(",")
				return self.core._get_batch_details(items)

		return ("Scraper failed", 500)
		
	def scrapeDiscoTopArtist(self, params = {}):
		get = params.get
		url = self.urls["disco_main"]
		page = self._fetchPage(url, params)
		list = SoupStrainer(name="div", attrs = {"class":"popular-artists"})
		popular = BeautifulSoup(page, parseOnlyThese=list)
		if (len(popular)):
			yobjects = []
			artists = popular.findAll(attrs={"class":"popular-artist-row"})
			for artist in artists:
				item = {}
				item["search"] = artist.contents[0]
				item["Title"] = artist.contents[0]
				item["thumbnail"] = "discoball"
				item["path"] = get("path")
				item["action"] = "disco_search"
				yobjects.append(item)
				
		return (yobjects, 200)
	
	def scrapeTrailers(self, params = {}):
		get = params.get
		if (get("scraper") in self.urls):
			url = self.urls[get("scraper")]
		else :
			url = self.urls["trailers"]
		page = self._fetchPage(url, params)
		if (get("scraper") == "latest_trailers"):
			return self.scrapeTrailersListFormat(page, params)
		else:
			return self.scrapeTrailersGridFormat(page, params)
		
	def scrape(self, params = {}):
		get = params.get
		if (get("scraper") == "disco_top_25"):
			return self.scrapeDiscoTop25(params)
		if (get("scraper") == "disco_top_artist"):
			return self.scrapeDiscoTopArtist(params)
		if (get("scraper", "").find("trailers") > -1):
			return self.scrapeTrailers(params)
		if (get("scraper") == "recommended"):
			return self.scrapeRecommended(params)
	
if __name__ == '__main__':

	sys.exit(0);
