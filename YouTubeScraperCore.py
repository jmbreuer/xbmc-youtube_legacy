import sys, urllib, urllib2, re
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
	urls['current_trailers'] = "http://www.youtube.com/trailers?s=trit&p=%s&hl=en"
	urls['upcoming_trailers'] = "http://www.youtube.com/trailers?s=tros&p=%s&hl=en"
	urls['popular_trailers'] = "http://www.youtube.com/trailers?s=trp&p=%s&hl=en"
	urls['recommended'] = "http://www.youtube.com/videos?r=1";

#=================================== Recommended ============================================
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

#=================================== Trailers ============================================
	def scrapeTrailersGridFormat(self, html, params = {}):
		get = params.get
		yobjects = []
		next = "false"
		
		pager = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
		pagination = BeautifulSoup(html, parseOnlyThese=pager)

		if (len(pagination) > 0):
			tmp = str(pagination)
			print "pagination scraper returned: " + str(pagination)
			if (tmp.find("Next") > 0):
				next = "true"
			
		list = SoupStrainer(id="popular-column", name="div")
		trailers = BeautifulSoup(html, parseOnlyThese=list)
				
		if (len(trailers) > 0):
			trailer = trailers.div.div

			item = []
			while ( trailer != None ):
				videoid = trailer.div.a['href']
						
				if (videoid):
					if (videoid.find("=") > -1):
						videoid = videoid[videoid.find("=")+1:]
						print self.__plugin__ + " scrapeTrailersGridFormat video : " + videoid
					
					item.append( (videoid, trailer.div.a.span.img['src']) )
					
				trailer = trailer.findNextSibling(name="div", attrs = { 'class':"trailer-cell *vl" })
			
			(yobjects, result ) = self.core._get_batch_details_thumbnails(item);
			
			if result != 200:
				return (yobjects, result)

		if (not yobjects):
			return (yobjects, 500)
		
		yobjects[len(yobjects)-1]['next'] = next

		return (yobjects, 200)
	
	def scrapeTrailersListFormat (self, page, params = {}):
		get = params.get		 
		yobjects = []
		
		list = SoupStrainer(id="recent-trailers-container", name="div")
		trailers = BeautifulSoup(page, parseOnlyThese=list)
		
		if (len(trailers) > 0):
			trailer = trailers.div.div
			item = []
			
			while (trailer != None):
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
#=================================== Categories  ============================================

	def scrapeCategoriesGrid(self, html, params = {}):
		print self.__plugin__ + " scrapeCategoriesGrid"
		print html
		get = params.get
		
		next = "false"
		pager = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
		pagination = BeautifulSoup(html, parseOnlyThese=pager)

		if (len(pagination) > 0):
			tmp = str(pagination)
			if (tmp.find("Next") > 0):
				next = "true"

		items = []
		result = re.compile('<div id="video-description-(.*)" dir="ltr" class="video-description">').findall(html)
		
		if len(result) > 0:
			for videoid in result:
				items.append(videoid)

		if (items):
			(results, status) = self.core._get_batch_details(items)
			results[len(results) -1]["next"] = next
			return (results, status)
		
		return ([], 303)
	
	def scrapeCategoryList(self, html, params = {}):
		get = params.get
				
		list = SoupStrainer(name="div", attrs = {"class":"browse-side-column"})
		categories = BeautifulSoup(html, parseOnlyThese=list)
		
		yobjects = []
		status = 200
		if (len(categories) > 0):
			category = categories.ul.li
			while (category != None):
				if (len(str(category["class"])) < 10):
					item = {}
					title = category.a.contents[0]
					title = title.replace("&amp;", "&")
					item['Title'] = title
					cat = category.a["href"]
					cat = urllib.quote_plus(cat)
					item['category'] = cat
					item['scraper'] = "categories"
					item["thumbnail"] = "explore"
					if (title != "Music"):
						yobjects.append(item)
				
				category = category.findNextSibling(name = "li")
		
		if (not yobjects):
			return (self.__language__(30601), 303)
		
		return (yobjects, status)
	
#=================================== Disco  ============================================

	def searchDisco(self, params = {}):
		get = params.get
		
		query = get("search")
		query = urllib.unquote_plus(query)
		
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		existingVideos = self.__settings__.getSetting("disco_%s" % query)
		
		if ( page == 0 or existingVideos == ""):
			( videos, result)  = self._get_disco_list(query)
			if (result == 200):
				self.__settings__.setSetting("disco_%s" % query, self.core.arrayToPipe(videos))
		else:
			videos = existingVideos.split("|")
		
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
		
	def _get_disco_list(self, query):
		if self.__dbg__:
			print self.__plugin__ + " _get_disco_list"
			
		url = self.urls["disco_search"] % urllib.quote_plus(query)
		if (self.__dbg__):
			print "Disco search url %s" % url
		page = self._fetchPage(url)
		
		if (page.find("a=") != -1):
			page = page[page.find("a=") + 2:]
			mix_list_id = page[:page.find("&")]
			url = self.urls["disco_mix_list"] % mix_list_id
			if (self.__dbg__):
				print "Disco respsonse url: %s" % url
								
			try:
				page = self._fetchPage(url)
				match = re.findall('.*?v=(.*)\&amp;a.*', page)
				if match:
					return (match, 200)
				else:
					return ( self.__language__(30601), 303)
			except:
				if self.__dbg__:
					print self.__plugin__ + " _get_disco_list caught unknown exception"
					print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__, sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				return ( "", 500 )
		
		if (self.__dbg__):
			print self.__plugin__ + " _get_disco_list no match"
			
		return ( self.__language__(30601), 303)
	
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
				if (self.__settings__.getSetting("disco_search_" + artist.contents[0] + "_thumb")):
					item["thumbnail"] = self.__settings__.getSetting("disco_search_" + artist.contents[0] + "_thumb")
				else:
					item["thumbnail"] = "discoball"
				item["path"] = get("path")
				item["action"] = "search_disco"
				yobjects.append(item)
				
		return (yobjects, 200)
#=================================== Common ============================================		

	def _fetchPage(self, feed, params = {}):
		url = urllib2.Request(feed)
		url.add_header('User-Agent', self.USERAGENT);
		
		con = urllib2.urlopen(url);
		page = con.read()
		con.close()
		return page
			
	def scrapePageinator(self, params = {}):
		get = params.get
		scraper_per_page = 0
		result = []
		
		if (get("scraper") in self.urls):
			scraper_per_page = 40
		elif ( get("scraper") == "categories" and get("category")):
			scraper_per_page = 23
		
		print "scraper per page " + str(scraper_per_page) 
		
		if (scraper_per_page > 0):
			# begin dark magic
			request_page = int(get("page", "0"))
			page_count = request_page
			per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
			xbmc_index = page_count * per_page 
			
			begin_page = (xbmc_index / scraper_per_page) + 1
			begin_index = (xbmc_index % scraper_per_page)
			
			params["page"] = str(begin_page)
			url = self.createUrl(params)
			html = self._fetchPage(url, params)
			if (self.__dbg__):
				print "requesting url " + url

			if (get("scraper") == "categories"):
				(result, status) = self.scrapeCategoriesGrid(html, params)	
			else:
				(result, status) = self.scrapeTrailersGridFormat(html, params)
			
			next = "false"
			next = result[len(result) -1]["next"]
			result = result[begin_index:]
			
			page_count = begin_page + 1
			params["page"] = str(page_count)
			
			i = 1
			while (len(result) <  per_page and result[len(result)-1]["next"] == "true"):
				url = self.createUrl(params)
				if (self.__dbg__):
					print "requesting url " + url
				html = self._fetchPage(url, params)

				if (get("scraper") == "categories"):
					(new_result, status) = self.scrapeCategoriesGrid(html, params)	
				else:
					(new_result, status) = self.scrapeTrailersGridFormat(html, params)
								
				next = new_result[len(new_result) - 1]["next"]
				result = result + new_result 
				page_count = page_count + 1
				params["page"] = str(page_count)
				
				i = i+1
				if (i > 9):	
					if (self.__dbg__):
						print "Scraper pagination failed, requested more than 10 pages which should never happen."
					return False
				
			if (result):
				result = result[:per_page]
				result[len(result) - 1]["next"] = next
				params["page"] = request_page
				return (result, status)
			else:
				return ([], 303)
		else :
			url = self.createUrl(params)
			html = self._fetchPage(url, params)
			if (get("scraper") == "categories" and not get("category"))	:
				return self.scrapeCategoryList(html, params)
			elif (get("scraper") == "categories" and get("category")):
				return self.scrapeCategoriesGrid(html, params)
			else:
				return self.scrapeTrailersListFormat(html, params)	
	
	def createUrl(self, params = {}):
		get = params.get
		page = get("page")
		if (get("scraper") == "categories" and get("category")):
			category = get("category")
			category = urllib.unquote_plus(category)
			
			if (category.find("/") != -1):
				url = self.urls["main"] + category + "?hl=en" + "&p=" + page
			else:
				url = self.urls["main"] + "/videos" + category + "&hl=en" + "&p=" + page
		elif(get("scraper") == "categories"):
			url = self.urls["recommended"] + "&hl=en"
		else:
			if (get("scraper") in self.urls):
				url = self.urls[get("scraper")]
				url = url % page
			else :
				url = self.urls["trailers"]
				
		return url
		
	def scrape(self, params = {}):
		get = params.get
		if (get("scraper") == "disco_top_25"):
			return self.scrapeDiscoTop25(params)
		if (get("scraper") == "disco_top_artist"):
			return self.scrapeDiscoTopArtist(params)
		if (get("scraper") == "recommended"):
			return self.scrapeRecommended(params)
		
		return self.scrapePageinator(params)
	
if __name__ == '__main__':
	
	sys.exit(0);
