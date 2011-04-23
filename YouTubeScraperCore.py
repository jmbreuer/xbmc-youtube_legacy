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

import sys, urllib, re
from BeautifulSoup import BeautifulSoup, SoupStrainer

class YouTubeScraperCore:	 

	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__utils__ = sys.modules[ "__main__" ].__utils__
	__core__ = sys.modules[ "__main__" ].__core__
	
	urls = {}
	urls['categories'] = "http://www.youtube.com/videos"
	urls['movies'] = "http://www.youtube.com/movies"
	urls['shows'] = "http://www.youtube.com/shows"
	urls['show_list'] = "http://www.youtube.com/show"
	urls['disco_main'] = "http://www.youtube.com/disco" 
	urls['disco_search'] = "http://www.youtube.com/disco?action_search=1&query=%s"
	urls['disco_mix_list'] = "http://www.youtube.com/watch?v=%s&feature=disco&playnext=1&list=%s"
	urls['main'] = "http://www.youtube.com"
	urls['trailers'] = "http://www.youtube.com/trailers?s=tr"
	urls['game_trailers'] = "http://www.youtube.com/trailers?s=gtcs"
	urls['current_trailers'] = "http://www.youtube.com/trailers?s=trit&p=%s&hl=en"
	urls['upcoming_trailers'] = "http://www.youtube.com/trailers?s=tros&p=%s&hl=en"
	urls['popular_trailers'] = "http://www.youtube.com/trailers?s=trp&p=%s&hl=en"
	urls['popular_game_trailers'] = "http://www.youtube.com/trailers?s=gtp&p=%s&hl=en"
	urls['upcoming_game_trailers'] = "http://www.youtube.com/trailers?s=gtcs&p=%s&hl=en"
	urls['recommended'] = "http://www.youtube.com/videos?r=1&hl=en"
	urls['watch_later'] = "http://www.youtube.com/my_watch_later_list"

#=================================== Recommended ============================================
	def scrapeRecommended(self, params = {}):
		get = params.get
				
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		oldVideos = self.__settings__.getSetting("recommendedVideos")
		
		if ( page == 0 or oldVideos == ""):
			( videos, result)  = self.scrapeYouTubeData(params)
			if (result == 200):
				self.__settings__.setSetting("recommendedVideos", self.__utils__.arrayToPipeDelimitedString(videos))
			else:
				return ( videos, result )
		else:
			videos = oldVideos.split("|")
		
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		else:
			next = 'false'
		
		subitems = videos[(per_page * page):(per_page * (page + 1))]
		
		if self.__dbg__:
			print self.__plugin__ + " calling get batch"
		if len(subitems) > 0:
			( ytobjects, status ) = self.__core__.getBatchDetails(subitems)
		else:
			return (subitems, 303)
		
		if (len(ytobjects) > 0):
			if (next == "true"):
				item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(int(get("page", "0")) + 1)} 
				for k, v in params.items():
					if (k != "thumbnail" and k != "Title" and k != "page"):
						item[k] = v
				ytobjects.append(item)
		
		return (ytobjects, status)
	
	def scrapeYouTubeData(self, params ={}):
		get = params.get
		retry = 0
		
		login_info = self.__settings__.getSetting( "login_info" )
		
		while not login_info and retry < 10:
			if ( self.__core__._httpLogin() ):
				login_info = self.__settings__.getSetting( "login_info" )
			retry += 1
		
		url = self.urls[get("scraper")]
		(result, status) = self.__core__._fetchPage({"link": url, "login": "true"})
		
		videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=grec_browse" class=').findall(result);
		
		if len(videos) == 0:
			videos = re.compile('<div id="reco-(.*)" class=').findall(result);
		
		return ( videos, 200 )
		
#=================================== Trailers ============================================
	def scrapeTrailersListFormat (self, page, params = {}):
		get = params.get		 
		yobjects = []
		
		list = SoupStrainer(id="recent-trailers-container", name="div")
		trailers = BeautifulSoup(page, parseOnlyThese=list)
		
		if (len(trailers) > 0):
			trailer = trailers.div.div
			items = []
			
			while (trailer != None):
				videoid = trailer.div.div.a['href']

				if (videoid):
					if (videoid.find("=") > -1):
						videoid = videoid[videoid.find("=")+1:]  
						items.append( (videoid, trailer.div.div.a.span.img['src']) )
				
				trailer = trailer.findNextSibling(name="div")
			
		if (items):
			(yobjects, status) = self.__core__.getBatchDetailsThumbnails(items)
			
		if (not yobjects):
			return (yobjects, 500)
		
		return (yobjects, status)
	
#=================================== Categories  ============================================
	def scrapeCategoriesGrid(self, html, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeCategoriesGrid"
		
		next = "false"
		pager = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
		pagination = BeautifulSoup(html, parseOnlyThese=pager)

		if (len(pagination) > 0):
			tmp = str(pagination)
			if (tmp.find("Next") > 0):
				next = "true"
		
		list = SoupStrainer(name="div", id="browse-video-data")
		videos = BeautifulSoup(html, parseOnlyThese=list)
		
		items = []
		if (len(videos) > 0):
			video = videos.div.div
			while (video != None):
				id = video.div.a["href"]
				if (id.find("/watch?v=") != -1):
					id = id[id.find("=") + 1:id.find("&")]
					items.append(id)
				video = video.findNextSibling(name="div", attrs = {'class':"video-cell *vl"})
		else:
			list = SoupStrainer(name="div", attrs = {'class':"most-viewed-list paginated"})
			videos = BeautifulSoup(html, parseOnlyThese=list)
			if (len(videos) > 0):
				video = videos.div.div.findNextSibling(name="div", attrs={'class':"video-cell"})
				while (video != None):
					id = video.div.a["href"]
					if (id.find("/watch?v=") != -1):
						id = id[id.find("=") + 1:id.find("&")]
						items.append(id)
						video = video.findNextSibling(name="div", attrs = {'class':"video-cell"})
		
		if (items):
			(results, status) = self.__core__.getBatchDetails(items)
			if (status == 200):
				results[len(results) -1]["next"] = next
			return (results, status)
		
		return ([], 303)
		
#=================================== Disco  ============================================

	def searchDisco(self, params = {}):
		get = params.get
		
		query = get("search")
		query = urllib.unquote_plus(query)
		
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		existingVideos = self.__settings__.getSetting("disco_%s" % query)
		
		if ( page == 0 or existingVideos == ""):
			( videos, status)  = self._get_disco_list(query)
			if (status == 200):
				self.__settings__.setSetting("disco_%s" % query, self.__utils__.arrayToPipeDelimitedString(videos))
		else:
			status = 200
			videos = existingVideos.split("|")
		
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		else:
			next = 'false'
		
		subitems = videos[(per_page * page):(per_page * (page + 1))]
		
		if (get("fetch_all") == "true"):
			subitems = videos
		
		if (status == 200):
			( ytobjects, status ) = self.__core__.getBatchDetails(subitems)
		
			if (len(ytobjects) > 0):
				if page == 0:
					self.__settings__.setSetting("disco_search_" + query + "_thumb", ytobjects[0]["thumbnail"])
				
				if (next == "true"):
					item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(int(get("page", "0")) + 1)} 
					for k, v in params.items():
						if (k != "thumbnail" and k != "Title" and k != "page"):
							item[k] = v
					ytobjects.append(item)
					
			return (ytobjects, status)
		
		return ([], 500)
		
	def _get_disco_list(self, query):
		if self.__dbg__:
			print self.__plugin__ + " _get_disco_list"
			
		url = self.urls["disco_search"] % urllib.quote_plus(query)
		if (self.__dbg__):
			print self.__plugin__ + " Disco search url " + repr(url)
		
		(page, status) = self.__core__._fetchPage({"link": url})
		if (page.find("list=") != -1):
			page = page.replace("\u0026", "&")
			mix_list_id = page[page.find("list=") + 5:]
			if (mix_list_id.find("&") != -1):
				mix_list_id = mix_list_id[:mix_list_id.find("&")]
			elif (mix_list_id.find('"') != -1):
				mix_list_id = mix_list_id[:mix_list_id.find('"')]
			
			video_id = page[page.find("v=") + 2:]
			video_id = video_id[:video_id.find("&")]
			
			url = self.urls["disco_mix_list"] % (video_id, mix_list_id)
										
			(page, status) = self.__core__._fetchPage({"link": url})
			
			list = SoupStrainer(name="div", id ="quicklist")
			mix_list = BeautifulSoup(page, parseOnlyThese=list)
			if (len(mix_list) > 0):
				match = mix_list.div["data-video-ids"].split(",")
				
				if match:
					return (match, 200)
				else:
					return ( self.__language__(30601), 303)
		
		if (self.__dbg__):
			print self.__plugin__ + " _get_disco_list no match"
			
		return ( self.__language__(30601), 303)
	
	def scrapeDiscoTop50(self, params = {}):
		get = params.get
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		videos = []
		existingVideos = self.__settings__.getSetting("disco_top_50")
		
		if ( page == 0 or existingVideos == ""):
			videos = self.scrapeDiscoTop50List(params)
			if (videos):
				self.__settings__.setSetting("disco_top_50", self.__utils__.arrayToPipeDelimitedString(videos))
		else:
			videos = existingVideos.split("|")
			videos = videos[:50]
		
		next = 'false'
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		
		subitems = videos[(per_page * page):(per_page * (page + 1))]
		
		if (get("fetch_all") == "true"):
			subitems = videos
		
		if len(subitems) > 0:
			(result , status) = self.__core__.getBatchDetails(subitems)
			if (status == 200):
				if (next == "true"):
					item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(int(get("page", "0")) + 1)} 
					for k, v in params.items():
						if (k != "thumbnail" and k != "Title" and k != "page"):
							item[k] = v
					result.append(item)
			return (result, status) 

		return ([], 500)
	
	def scrapeDiscoTop50List(self, params = {}):
		url = self.urls["disco_main"]
		(page, status) = self.__core__._fetchPage({"link": url})
		list = SoupStrainer(name="div", attrs = {"class":"popular-message"})
		popular = BeautifulSoup(page, parseOnlyThese=list)
		items = []
		
		if (len(popular) > 0):
			videos = self.urls["main"] + popular.a["onclick"]
			videos = videos.replace("&quot;",'"')
			if (videos.find('"') > 0):
				videos = videos[videos.find('["')+2:videos.rfind("])")]
				videos = videos.replace('"',"")
				videos = videos.replace(" ","")
				items = videos.split(",")
		
		return items[:50]
		
	def scrapeDiscoTopArtist(self, params = {}):
		get = params.get
		url = self.urls["disco_main"]
		(page, status) = self.__core__._fetchPage({"link":url})
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
				item["scraper"] = "search_disco"
				yobjects.append(item)
				
		return (yobjects, 200)
	
#=================================== Shows ============================================
	def scrapeShowEpisodes(self, html, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeShowEpisodes"
		
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		oldVideos = self.__settings__.getSetting("show_" + get("show") + "_season_" + get("season","0") )
		
		if ( page == 0 or not oldVideos):
			videos = re.compile('<a href="/watch\?v=(.*)&amp;list=SL">').findall(html)
			if (not videos):
				videos = re.compile('<a class="yt-uix-hovercard-target" href="/watch\?v=(.*)&amp;list=SL"').findall(html)
			
			self.__settings__.setSetting("show_" + get("show") + "_season_" + get("season","0"), self.__utils__.arrayToPipeDelimitedString(videos))
		else:
			videos = oldVideos.split("|")
		
		if ( per_page * ( page + 1 ) < len(videos) ):
			next = 'true'
		else:
			next = 'false'
		
		subitems = videos[(per_page * page):(per_page * (page + 1))]
		
		( ytobjects, status ) = self.__core__.getBatchDetails(subitems)

		if (len(ytobjects) > 0):
			ytobjects[len(ytobjects)-1]['next'] = next
		
		return (ytobjects, status)
		
		# If the show contains more than one season the function will returns a list of folder items,
		# otherwise a paginated list of video items is returned
	def scrapeShow(self, html, params = {}):
		get = params.get
		yobjects = []
		
		if ((html.find("page not-selected") == -1) or get("season")):
			if self.__dbg__:
				print self.__plugin__ + " parsing videolist for single season"
			(yobjects, status) = self.scrapeShowEpisodes(html, params)
						
			return (yobjects, status)
				
		list = SoupStrainer(name="div", attrs = {'class':"shows-episodes-sort browse-pager"})
		seasons = BeautifulSoup(html, parseOnlyThese=list)
		if (len(seasons) > 0):
			params["folder"] = "true"
			season = seasons.div.span.findNextSibling()
			
			print self.__plugin__ + " season " + repr(season)
			while (season != None):
				item = {}
				if (str(season).find("page not-selected") > 0):
					season_url = season["href"]
					
					if (season_url.find("&amp;s=") > 0):
						season_url = season_url[season_url.find("&amp;s=") + 7:]
						if (season_url.find("&amp;") > 0):
							season_url = season_url[:season_url.find("&amp;")]
						item["Title"] = "Season " + season_url.encode("utf-8")
						item["season"] = season_url.encode("utf-8")
						item["thumbnail"] = "shows"
						item["scraper"] = "show"
						item["icon"] = self.__utils__.getThumbnail("shows")
						item["show"] = get("show")
						yobjects.append(item)
				else:
					if (len(season.contents[0]) > 0):
						season_url = season.contents[0]
						item["Title"] = "Season " + season_url.encode("utf-8")
						item["season"] = season_url.encode("utf-8")
						item["thumbnail"] = "shows"
						item["icon"] = self.__utils__.getThumbnail("shows")
						item["scraper"] = "show"
						item["show"] = get("show")
						yobjects.append(item)
				
				season = season.findNextSibling()			
		
		if (yobjects):
			return ( yobjects, 200 )
				
		return ([], 303)
	
	def scrapeShowsGrid(self, html, params = {}):
		get = params.get
		params["folder"] = "true"
		if self.__dbg__:
			print self.__plugin__ + " scrapeShowsGrid"
		
		next = "false"
		pager = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
		pagination = BeautifulSoup(html, parseOnlyThese=pager)

		if (len(pagination) > 0):
			tmp = str(pagination)
			if (tmp.find("Next") > 0):
				next = "true"
		
		#Now look for the shows in the list.
		list = SoupStrainer(name="div", attrs = {"class":"popular-show-list"})
		shows = BeautifulSoup(html, parseOnlyThese=list)
		
		yobjects = []
		status = 200
		
		if (len(shows) > 0):
			
			show = shows.div.div
			
			while (show != None):
				
				if (show.a):
					item = {}
					episodes = show.find(name = "div", attrs= {'class':"show-extrainfo"})
					title = show.div.h3.contents[0]
					if (episodes and episodes.span):
						title = title + " (" + episodes.span.contents[0].lstrip().rstrip() + ")"
					
					title = title.replace("&amp;", "&")
					item['Title'] = title
					
					show_url = show.a["href"]
					if (show_url.find("?p=") > 0):
						show_url = show_url[show_url.find("?p=") + 1:]
					else :
						show_url = show_url.replace("/show/", "")
					
					show_url = urllib.quote_plus(show_url)
					item['show'] = show_url
					item['icon'] = self.__utils__.getThumbnail("shows")
					item['scraper'] = "show"
					thumbnail = show.a.span.img['src']
					if ( thumbnail.find("_thumb.") > 0):
						thumbnail = thumbnail.replace("_thumb.",".")
					else:
						thumbnail = "show"
					
					item["thumbnail"] = thumbnail
					
					if self.__dbg__:
						print self.__plugin__ + " adding show " + repr(item['Title']) + ", url: " + repr(item['show'])
					
					yobjects.append(item)
				
				show = show.findNextSibling(name="div", attrs = { 'class':re.compile("show-cell .") })
			
		if (not yobjects):
			return (self.__language__(30601), 303)
		
		yobjects[len(yobjects) -1]["next"] = next
		
		return (yobjects, status)

#=================================== Common ============================================		
			
	def scrapePageinator(self, params = {}):
		get = params.get
		original_page = int(get("page","0"))
		scraper_per_page = 0
		result = []

		if ( get("scraper") == "categories" and get("category")):
			if urllib.unquote_plus(get("category")).find("/") != -1:
				scraper_per_page = 23
			else:
				scraper_per_page = 36
		elif ( get("scraper") == "shows" and get("category")):
			scraper_per_page = 44
		elif ( get("scraper") == "movies" and get("category")):
			scraper_per_page = 60		
		elif (get("scraper") != "shows" and 
			get("scraper") != "show" and 
			get("scraper") != "categories" and 
			get("scraper") != "movies" and 
			get("scraper") in self.urls):
			scraper_per_page = 40
		
		if (self.__dbg__):
			print self.__plugin__ + " scraper per page " + str(scraper_per_page) 
		
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
			if (self.__dbg__):
				print "fetching url " + url
			(html, status) = self.__core__._fetchPage({"link": url})

			if (get("scraper") == "categories"):
				(result, status) = self.scrapeCategoriesGrid(html, params)
			elif (get("scraper") == "shows"):
				(result, status) = self.scrapeShowsGrid(html, params)	
			else:
				(result, status) = self.scrapeGridFormat(html, params)
			
			next = "false"
			if (result):
				next = result[len(result) -1]["next"]
				result[len(result) -1]["next"] = ""
				result = result[begin_index:]
			
				page_count = begin_page + 1
				params["page"] = str(page_count)
				
				i = 1
				while (len(result) <  per_page and next == "true"):
					url = self.createUrl(params)
					if (self.__dbg__):
						print "fetching url: " + url
					(html, status) = self.__core__._fetchPage({"link": url})
	
					if (get("scraper") == "categories"):
						(new_result, status) = self.scrapeCategoriesGrid(html, params)
					elif (get("scraper") == "shows"):
						(new_result, status) = self.scrapeShowsGrid(html, params)	
					else:
						(new_result, status) = self.scrapeGridFormat(html, params)
					
					if (new_result):
						next = new_result[len(new_result) - 1]["next"]
						result[len(result) -1]["next"] = ""
					else: 
						next = "false"
					
					result = result + new_result 
					page_count = page_count + 1
					params["page"] = str(page_count)
					
					i = i+1
					if (i > 9):	
						if (self.__dbg__):
							print "Scraper pagination failed, requested more than 10 pages which should never happen."
						return False
				
				if (next == "false" and len(result) > per_page):
					next = "true"
					
				result = result[:per_page]
				
				if (next == "true"):
					item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(original_page + 1)} 
					for k, v in params.items():
						if (k != "thumbnail" and k != "Title" and k != "page"):
							item[k] = v
					result.append(item)
				return (result, status)
			else:
				return ([], 303)
		else:
			url = self.createUrl(params)
			
			if self.__dbg__:
				print self.__plugin__ + " fetching url: " + url 
				
			(html,status) = self.__core__._fetchPage({"link": url})
			if (get("scraper") == "categories" )	:
				if (get("category")):
					return self.scrapeCategoriesGrid(html, params)
				else:
					return self.scrapeCategoryList(html, params)
			elif (get("show")):
				return self.scrapeShow(html, params)
			elif (get("scraper") == "shows"):
				if (get("category")):
					return self.scrapeShowsGrid(html, params)
				else:
					return self.scrapeCategoryList(html, params, "shows")
			elif (get("scraper") == "movies"):
				if (get("category")):
					return self.scrapeGridFormat(html, params)
				else: 
					return self.scrapeCategoryList(html, params, "movies")
			else:
				return self.scrapeTrailersListFormat(html, params)
	
	def createUrl(self, params = {}):
		get = params.get
		page = get("page")
		
		if (get("scraper") == "categories"):
			if (get("category")):
				category = get("category")
				category = urllib.unquote_plus(category)  
				if (category.find("/") != -1):
					url = self.urls["main"] + category + "?hl=en" + "&p=" + page
				else:
					url = self.urls["main"] + "/categories" + category + "&hl=en" + "&p=" + page
			else:
				url = self.urls["categories"] + "?hl=en"
		
		elif (get("scraper") == "shows" or get("scraper") == "movies"):
			if (get("category")):
				category = get("category")
				category = urllib.unquote_plus(category)
				url = self.urls[get("scraper")] + "/" + category + "?p=" + page + "&hl=en"
			else:
				url = self.urls[get("scraper")] + "?hl=en"	
				
		elif (get("show")):			
			show = urllib.unquote_plus(get("show"))
			if (show.find("p=") < 0):
				url = self.urls["show_list"] + "/" + show + "?hl=en"
			else:
				url = self.urls["show_list"] + "?" + show + "&hl=en"
			if (get("season")):
				url = url + "&s=" + get("season")
			
		else:
			if (get("scraper") in self.urls):
				url = self.urls[get("scraper")]
				url = url % page
			else :
				if (get("scraper") == "latest_trailers"):					
					url = self.urls["trailers"]
				else:
					url = self.urls["game_trailers"]
				
		return url
	
	def scrapeGridFormat(self, html, params = {}):
		get = params.get
		yobjects = []
		next = "false"
		
		pager = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
		pagination = BeautifulSoup(html, parseOnlyThese=pager)

		if (len(pagination) > 0):
			tmp = str(pagination)
			if (tmp.find("Next") > 0):
				next = "true"
			
		list = SoupStrainer(id="popular-column", name="div")
		trailers = BeautifulSoup(html, parseOnlyThese=list)
		
		if (len(trailers) > 0):
			trailer = trailers.div.div
			if (get("scraper") == "movies"):
				trailer = trailers.div.div.div
			
			cell = "trailer-cell *vl"
			if (get("scraper") == "movies"):
				cell = "movie-cell *vl"
			if (get("scraper") == "categories"):
				cell = "video-cell"
			
			item = []
			while ( trailer != None ):
				videoid = trailer.div.a['href']
						
				if (videoid):
					if (videoid.find("=") > -1):
						videoid = videoid[videoid.find("=")+1:]
					
					item.append( (videoid, trailer.div.a.span.img['src']) )
				
				trailer = trailer.findNextSibling(name="div", attrs = { 'class':cell })
			
			(yobjects, result ) = self.__core__.getBatchDetailsThumbnails(item);
			
			if result != 200:
				return (yobjects, result)

		if (not yobjects):
			return (yobjects, 500)
		
		yobjects[len(yobjects)-1]['next'] = next

		return (yobjects, 200)
	
	def scrapeCategoryList(self, html = "", params = {}, tag = ""):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + "scrapeCategories " 
		scraper = "categories"
		thumbnail = "explore"
		
		if (tag):
			scraper = tag
			thumbnail = tag
		
		list = SoupStrainer(name="div", attrs = {"class":"yt-uix-expander-body"})
		categories = BeautifulSoup(html, parseOnlyThese=list)
		
		yobjects = []
		status = 200
		
		if (len(categories) > 0):
			ul = categories.ul
			while (ul != None):
				category = ul.li
				while (category != None):
					if (category.a):
						item = {}
						title = category.a.contents[0]
						title = title.replace("&amp;", "&")
						item['Title'] = title
						cat = category.a["href"].replace("/" + tag + "/", "")
						if get("scraper") == "categories":
							if title == "Music":
								category = category.findNextSibling(name = "li")
								continue
							if cat.find("?") != -1:
								cat = cat[cat.find("?"):]
							if cat.find("comedy") > 0:
								cat = "?c=23"
							if cat.find("gaming") > 0:
								cat = "?c=20"
						
						cat = urllib.quote_plus(cat)
						item['category'] = cat
						item['scraper'] = scraper
						item["thumbnail"] = thumbnail
						if self.__dbg__:
							print self.__plugin__ + "adding item: " + item['Title'] + ", url: " + item['category']
						yobjects.append(item)
					
					category = category.findNextSibling(name = "li")
				ul = ul.findNextSibling(name = "ul")
		
		if (not yobjects):
			return (self.__language__(30601), 303)
		
		return (yobjects, status)
		
	def scrape(self, params = {}):
		get = params.get
		
		if (get("scraper") == "search_disco"):
			return self.searchDisco(params)
		if (get("scraper") == "disco_top_50"):
			return self.scrapeDiscoTop50(params)
		if (get("scraper") == "disco_top_artist"):
			return self.scrapeDiscoTopArtist(params)
		if (get("scraper") == "recommended"):
			return self.scrapeRecommended(params)
		
		return self.scrapePageinator(params)
	
if __name__ == '__main__':
	sys.exit(0);
