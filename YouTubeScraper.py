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
import YouTubeCore, YouTubeUtils
from BeautifulSoup import BeautifulSoup, SoupStrainer

class YouTubeScraper(YouTubeCore.YouTubeCore, YouTubeUtils.YouTubeUtils):	 

	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__feeds__ = sys.modules[ "__main__" ].__feeds__
	__storage__ = sys.modules [ "__main__" ].__storage__
	
	def __init__(self):
		self.urls['categories'] = "http://www.youtube.com/videos"
		self.urls['current_trailers'] = "http://www.youtube.com/trailers?s=trit&p=%s&hl=en"
		self.urls['disco_main'] = "http://www.youtube.com/disco" 
		self.urls['disco_mix_list'] = "http://www.youtube.com/watch?v=%s&feature=disco&playnext=1&list=%s"
		self.urls['disco_search'] = "http://www.youtube.com/disco?action_search=1&query=%s"
		self.urls['game_trailers'] = "http://www.youtube.com/trailers?s=gtcs"
		self.urls['live'] = "http://www.youtube.com/live"
		self.urls['main'] = "http://www.youtube.com"
		self.urls['movies'] = "http://www.youtube.com/ytmovies"
		self.urls['popular_game_trailers'] = "http://www.youtube.com/trailers?s=gtp&p=%s&hl=en"
		self.urls['popular_trailers'] = "http://www.youtube.com/trailers?s=trp&p=%s&hl=en"
		self.urls['recommended'] = "http://www.youtube.com/videos?r=1&hl=en"
		self.urls['show_list'] = "http://www.youtube.com/show"
		self.urls['shows'] = "http://www.youtube.com/shows"
		self.urls['trailers'] = "http://www.youtube.com/trailers?s=tr"
		self.urls['latest_trailers'] = "http://www.youtube.com/trailers?s=tr"
		self.urls['latest_game_trailers'] = "http://www.youtube.com/trailers?s=gtcs"
		self.urls['upcoming_game_trailers'] = "http://www.youtube.com/trailers?s=gtcs&p=%s&hl=en"
		self.urls['upcoming_trailers'] = "http://www.youtube.com/trailers?s=tros&p=%s&hl=en"
		self.urls['watch_later'] = "http://www.youtube.com/my_watch_later_list"
		self.urls['liked_videos'] = "http://www.youtube.com/my_liked_videos"
		self.urls['music'] = "http://www.youtube.com/music"
		self.urls['artist'] = "http://www.youtube.com/artist?a=%s&feature=artist"	
		
#=================================== Trailers ============================================
	def scrapeTrailersListFormat (self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeTrailersListFormat"

		yobjects = []
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
		
		list = SoupStrainer(id="recent-trailers-container", name="div")
		trailers = BeautifulSoup(html, parseOnlyThese=list)
		
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
			(yobjects, status) = self.getBatchDetailsThumbnails(items)
			
		if (not yobjects):
			return (yobjects, 500)
		
		return (yobjects, status)
	
#=================================== Categories  ============================================
	def scrapeCategoriesGrid(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeCategoriesGrid"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})

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
						id = id[id.find("=") + 1:]
					if (id.find("&") > 0):
						id = id[:id.find("&")]
					items.append(id)
					video = video.findNextSibling(name="div", attrs = {'class':"video-cell"})
				
		return (items, status)
		
#=================================== Music  ============================================
	def scrapeMusicCategories(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeMusicCategories"
		
		items = []
		url = self.urls["music"]
		(html, status) = self._fetchPage({"link": url})
		
		if status == 200:
			list = SoupStrainer(name="div", id="browse-filter-menu")
			content = BeautifulSoup(html, parseOnlyThese=list)
			if (len(content) > 0):
				cat_list = content.ul
				while cat_list != None:
					category = cat_list.li
					if (category.a == None):
						category = category.findNextSibling()
					while category != None:
						item = {}
						title = self.makeAscii(category.a.contents[0])
						title = self.replaceHtmlCodes(title)
						id = category.a["href"].replace("/music/","/")
						item["Title"] = title
						item["category"] = urllib.quote_plus(id)
						item["icon"] = "music"
						item["thumbnail"] = "music"
						item["scraper"] = get("scraper")
						if get("scraper") == "music_artists":
							item["folder"] = "true"
						
						items.append(item)
						category = category.findNextSibling()
					cat_list = cat_list.findNextSibling()
		return (items, status) 

	
	def scrapeArtist(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeArtist"

		items = []
		videos = []
		if self.__dbg__:
			print self.__plugin__ + " scrapeArtist"
		
		if get("artist"):
			url = self.urls["artist"] % get("artist")
			(html, status) = self._fetchPage({"link": url})
			
			if status == 200:
				videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=artist" title="').findall(html);
				
		for v in videos:
			if v not in items:
				items.append(v)
		
		return ( items, status )
	
	def scrapeSimilarArtists(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeSimilarArtist"
		
		items = []
		if get("artist"):
			url = self.urls["artist"] % get("artist")
			(html, status) = self._fetchPage({"link": url})
			
			if status == 200:
				list = SoupStrainer(name="div", id ="similar-artists")
				content = BeautifulSoup(html, parseOnlyThese=list)
				artists = content.findAll(name = "div", attrs = {"class":"similar-artist"})
				for artist in artists:
					item = {}
					title = self.makeAscii(artist.a.contents[0])
					title = self.replaceHtmlCodes(title)
					item["Title"] = title
					
					id = artist.a["href"]
					id = id[id.find("?a=") + 3:id.find("&")]
					item["artist"] = id
					item["icon"] = "music"
					item["scraper"] = "music_artist"
					item["thumbnail"] = "music"
					items.append(item)
		
		return ( items, status )
		
	def scrapeMusicCategoryArtists(self, params={}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeMusicCategoryArtists"
			
		status = 200
		items = []
		
		if get("category"):
			category = urllib.unquote_plus(get("category"))
			url = self.urls["music"] + category
			(html, status) = self._fetchPage({"link":url})
			
			list = SoupStrainer(name="div", attrs = {"class":"ytg-fl browse-content"})
			content = BeautifulSoup(html, parseOnlyThese=list)
			
			if (len(content) > 0):
				artists = content.findAll(name="div", attrs = {"class":"browse-item artist-item"}, recursive=True)
				for artist in artists:
					item = {}
					title = self.makeAscii(artist.div.h3.a.contents[0])
					title = self.replaceHtmlCodes(title)
					item["Title"] = title
					item["scraper"] = "music_artist"
					
					id = artist.a["href"]
					id = id[id.find("?a=") + 3:id.find("&")]
					item["artist"] = id
					item["icon"] = "music"
					item["thumbnail"] = artist.a.span.span.span.img["data-thumb"]
					items.append(item)
		
		return (items, status)
	
	def scrapeMusicCategoryHits(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeMusicCategoryHits"

		status = 200
		items = []
		params["batch"] = "true"
		
		if get("category"):
			category = urllib.unquote_plus(get("category"))
			url = self.urls["music"] + category
			(html, status) = self._fetchPage({"link":url})
			
			list = SoupStrainer(name="div", attrs = {"class":"ytg-fl browse-content"})
			content = BeautifulSoup(html, parseOnlyThese=list)
			
			if (len(content) > 0):
				videos = content.findAll(name="div", attrs = {"class":"browse-item music-item "}, recursive=True)
				for video in videos: 
					id = video.a["href"]
					id = id[id.find("?v=") + 3:id.find("&")]
					items.append(id)
		
		return (items, status)
	

	def searchDisco(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " searchDisco"
		
		items = []

		url = self.urls["disco_search"] % urllib.quote_plus(get("search"))
		(page, status) = self._fetchPage({"link": url})
		
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
										
			(page, status) = self._fetchPage({"link": url})
			
			list = SoupStrainer(name="div", id ="playlist-bar")
			mix_list = BeautifulSoup(page, parseOnlyThese=list)
			if (len(mix_list) > 0):
				items = mix_list.div["data-video-ids"].split(",")
		
		return ( items, status)
	
	def scrapeDiscoTop50(self, params = {}):
		get = params.get		
		if self.__dbg__:
			print self.__plugin__ + " scrapeDiscoTop50"
			
		url = self.urls["disco_main"]
		(page, status) = self._fetchPage({"link": url})
		
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
		
		return ( items, status)
	
	def scrapeDiscoTopArtist(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeTopArtists"
		
		url = self.urls["disco_main"]
		(page, status) = self._fetchPage({"link":url})
		
		list = SoupStrainer(name="div", attrs = {"class":"popular-artists"})
		popular = BeautifulSoup(page, parseOnlyThese=list)
		yobjects = []
		if (len(popular)):
			artists = popular.findAll(attrs={"class":"popular-artist-row"})
			for artist in artists:
				item = {}
				title = self.makeAscii(artist.contents[0])
				item["search"] = title
				item["Title"] = title
				
				params["thumb"] = "true"
				thumb = self.__storage__.retrieve(params, "thumbnail", item)
				if not thumb:
					item["thumbnail"] = "discoball"
				else:
					item["thumbnail"] = thumb
				
				item["path"] = get("path")
				item["scraper"] = "search_disco"
				yobjects.append(item)
				
		return (yobjects, status)

#=================================== Live ============================================
	def scrapeLiveNow(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeLiveNow"

		url = self.urls[get("scraper")]
		
		(response , status) = self._fetchPage({"link": url})
		
		list = SoupStrainer(name="div", id='live-now-list-container')
		live = BeautifulSoup(response, parseOnlyThese=list)
		videos = []
		if (len(live) > 0):
			video = live.div.div
			while (video != None):
				item = {}
				videoid = video.div.a["href"]
				videoid = videoid[videoid.rfind("/")+1:]
				item["videoid"] = videoid
				item["icon"] = "live"
				thumbnail = video.div.a.span.span.img["src"]
				thumbnail = thumbnail.replace("default","0")
				item["thumbnail"] = thumbnail
				title = "Unknown Title"
				
				info = video.div.findNextSibling(name="div", attrs = {'class':"live-browse-info"})
				if len(info) > 0: 
					title = info.a.contents[0]
				item["Studio"] = info.span.a["title"]
				item ["Title"] = title
				videos.append(item)
				video = video.findNextSibling(name="div", attrs= {"class":"video-cell"})
		
		return (videos, status)	
				
#=================================== User Scraper ============================================
	
	def scrapeRecommended(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeRecommended"
		
		url = self.urls[get("scraper")]
		(result, status) = self._fetchPage({"link": url, "login": "true"})
		
		videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=grec_browse" class=').findall(result);
		
		if len(videos) == 0:
			videos = re.compile('<div id="reco-(.*)" class=').findall(result);
		
		return ( videos, status )

	def scrapeWatchLater(self, params):	
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeWatchLater"
		
		url = self.urls[get("scraper")]
		
		(response , status) = self._fetchPage({"link": url, "get_redirect":"true", "login": "true"})
		
		if status == 200:
			if response.find("p=") > 0:
				response = response[response.find("p=") + 2:]
				playlist_id = response[:response.find("&")]
				params["user_feed"] = "playlist"
				params["login"] = "true"
				params["playlist"] = playlist_id
				return self.__feeds__.list(params)
		
		return ([], 303)
	
	def scrapeLikedVideos(self, params):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeLikedVideos"
		
		url = self.urls[get("scraper")]
		
		(response, status) = self._fetchPage({"link": url, "login": "true"})
		
		list = SoupStrainer(name="div", id="vm-video-list-container")
		liked = BeautifulSoup(response, parseOnlyThese=list)
		items = []
		
		if (len(liked) > 0):
			video = liked.ol.li
			while video:
				videoid = video["id"]
				videoid = videoid[videoid.rfind("video-") + 6:]
				items.append(videoid)
				video = video.findNextSibling()
		
		return (items, status)
			
#=================================== Shows ============================================
	def scrapeShowEpisodes(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeShowEpisodes"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
			
		videos = re.compile('<a href="/watch\?v=(.*)&amp;feature=sh_e_sl&amp;list=SL"').findall(html)
			
		list = SoupStrainer(name="div", attrs = {'class':"show-more-ctrl"})
		nexturl = BeautifulSoup(html, parseOnlyThese=list)
		if (len(nexturl) > 0):
			nexturl = nexturl.find(name="div", attrs = {'class':"button-container"})
			if (nexturl.button):
				nexturl = nexturl.button["data-next-url"]
			else:
				nexturl = ""
		
		if nexturl.find("start=") > 0:
			fetch = True
			start = 20
			nexturl = nexturl.replace("start=20", "start=%s")
			while fetch:
				url = self.urls["main"] + nexturl % start
				(html, status) = self._fetchPage({"link":url})
				
				if status == 200:
					html = html.replace("\\u0026","&")
					html = html.replace("\\/","/")
					html = html.replace('\\"','"')
					html = html.replace("\\u003c","<")
					html = html.replace("\\u003e",">")
					more_videos = re.compile('data-video-ids="([^"]*)"').findall(html)
					
					if not more_videos:
						fetch = False
					else:
						videos += more_videos
						start += 20
		
		return (videos, status)
		
		# If the show contains more than one season the function will return a list of folder items,
		# otherwise a paginated list of video items is returned
	def scrapeShow(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeShow"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
		
		if ((html.find('class="seasons"') == -1) or get("season")):
			if self.__dbg__:
				print self.__plugin__ + " parsing videolist for single season"
			return self.scrapeShowEpisodes(params)
		
		params["folder"] = "true"
		del params["batch"]
		return self.scrapeShowSeasons(html, params)
	
	def scrapeShowSeasons(self, html, params = {}):
		get = params.get
		params["folder"] = "true"
		if self.__dbg__:
			print self.__plugin__ + " scrapeShowSeasons"
		
		yobjects = []
		list = SoupStrainer(name="div", attrs = {'class':"seasons"})
		seasons = BeautifulSoup(html, parseOnlyThese=list)
		if (len(seasons) > 0):
			params["folder"] = "true"
			season = seasons.div.div.span.button
			
			while (season != None):
				item = {}
				
				season_id = season.span.contents[0]
				title = self.__language__(30058) % season_id.encode("utf-8")
				title += " - " + season["title"].encode("utf-8")
				item["Title"] = title
				item["season"] = season_id.encode("utf-8")
				item["thumbnail"] = "shows"
				item["scraper"] = "show"
				item["icon"] = "shows"
				item["show"] = get("show")
				yobjects.append(item)
				season = season.findNextSibling()			
		
		if (len(yobjects) > 0):
			return ( yobjects, 200 )
		
		return ([], 303)
	
	def scrapeShowsGrid(self, html, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeShowsGrid"
		
		next = "true"
		items = []
		page = 1
		
		while next == "true":
			next = "false"
			params["page"] = str(page)
			
			url = self.createUrl(params)
			print "some url " + repr(url)
			(html, status) = self._fetchPage({"link":url})
			
			list = SoupStrainer(name="div", attrs = {"class":"popular-show-list"})
			shows = BeautifulSoup(html, parseOnlyThese=list)
		
			if (len(shows) > 0):
				show = shows.div.div
			
				while (show != None):
					
					if (show.a):
						item = {}
						episodes = show.find(name = "div", attrs= {'class':"show-extrainfo"})
						title = show.div.h3.contents[0]
						if (episodes and episodes.span):
							title = title + " (" + episodes.span.contents[0].lstrip().rstrip() + ")"
						title = self.replaceHtmlCodes(title)
						item['Title'] = title
						
						show_url = show.a["href"]
						if (show_url.find("?p=") > 0):
							show_url = show_url[show_url.find("?p=") + 1:]
						else :
							show_url = show_url.replace("/show/", "")
						show_url = urllib.quote_plus(show_url)
						item['show'] = show_url
						
						item['icon'] = "shows"
						item['scraper'] = "show"
						thumbnail = show.a.span.img['src']
						if ( thumbnail.find("_thumb.") > 0):
							thumbnail = thumbnail.replace("_thumb.",".")
						else:
							thumbnail = "shows"
						
						item["thumbnail"] = thumbnail						
						items.append(item)
						
					show = show.findNextSibling(name="div", attrs = { 'class':re.compile("show-cell .") })
					
		return (items, status)

#=================================== Music ============================================

	def scrapeYouTubeTop100(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeYouTubeTop100"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link": url})
		
		items = []
		if status == 200:
			items = re.compile('<a href="/watch\?v=(.*)&amp;feature=musicchart" class=').findall(html);
		
		return (items, status)
		
#=================================== Movies ============================================		

	def scrapeMovieSubCategory(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeMovieSubCategory"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
		
		params["folder"] = "true"
		ytobjects = []
		list = SoupStrainer(name="div", attrs = {'class':"ytg-fl browse-content"})
		categories = BeautifulSoup(html, parseOnlyThese=list)		
		
		if len(categories):
			categorylist = categories.findAll(name="div", attrs = {'class':"yt-uix-slider-head"})
			for category in categorylist:
				item = {}
				cat = category.div.button["href"]
				title = category.div.findNextSibling(name="div")
				title = title.h2.contents[0].strip()
				item['Title'] = title
				cat = cat.replace("/movies/", "")												
				cat = urllib.quote_plus(cat)
				item['category'] = cat
				item['scraper'] = "movies"
				item["thumbnail"] = "movies"
				ytobjects.append(item)
		
		return (ytobjects, status)
	
	def scrapeMoviesGrid(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeMoviesGrid"
		
		params["batch"] = "thumbnails"
		next = "true"
		items = []
		page = 1
		
		while next == "true":
			next = "false"
			params["page"] = str(page)
			
			url = self.createUrl(params)
			(html, status) = self._fetchPage({"link":url})
			
			list = SoupStrainer(name="div", attrs = {'class':"yt-uix-pager"})
			paginator = BeautifulSoup(html, parseOnlyThese=list)
			if (len(paginator) > 0):
				links = paginator.findAll(name="a", attrs = {'class':"yt-uix-pager-link"})
				for link in links:
					print "next page ? link: " + repr(int(link["data-page"])) + " > page: " + str(page)
					if int(link["data-page"]) > page:
						next = "true"
			
			list = SoupStrainer(name="ul", attrs = {'class':"browse-item-list"})
			movies = BeautifulSoup(html, parseOnlyThese=list)
			
			if (len(movies) > 0):
				page += 1
				movie = movies.li
				
				while ( movie != None ):
					videoid = ""
					video_info = movie.div.a.span.findNextSibling(name="span")
					if video_info:
						videoid = video_info['data-video-ids']
							
					if (videoid):					
						items.append( (videoid, movie.div.a.span.img["data-thumb"]) )
					
					movie = movie.findNextSibling(name="li")
		
		del params["page"]
		return (items, status)
	
#================================== Common ============================================
	
	def getNewResultsFunction(self, params = {}):
		get = params.get
		
		function = ""	
		if (get("scraper") == "search_disco"):
			function = self.searchDisco
			params["batch"] = "true"
		if (get("scraper") == "liked_videos"):
			function = self.scrapeLikedVideos
			params["batch"] = "true"
		if (get("scraper") == "live"):
			function = self.scrapeLiveNow
		if (get("scraper") == "disco_top_50"):
			function = self.scrapeDiscoTop50
			params["batch"] = "true"
		if (get("scraper") == "recommended"):
			function = self.scrapeRecommended
			params["batch"] = "true"
		if (get("scraper") == "music_top100"):
			function = self.scrapeYouTubeTop100
			params["batch"] = "true"
		if (get("scraper") == "disco_top_artist"):
			function = self.scrapeDiscoTopArtist
			params["folder"] = "true"
		if (get("scraper") == "music_artist"):
			function = self.scrapeArtist
			params["batch"] = "true"
		if (get("scraper") == "similar_artist"):
			function = self.scrapeSimilarArtists
			params["folder"] = "true"
		if (get("scraper") == "music_hits" or get("scraper") == "music_artists"):
			if get("category") and get("scraper") == "music_hits":
				function = self.scrapeMusicCategoryHits
			elif get("category") and get("scraper") == "music_artists":
				function = self.scrapeMusicCategoryArtists
			else:
				function = self.scrapeMusicCategories
		
		if (get("scraper") in ["categories", "movies", "shows"] and not get("category")):
			function = self.scrapeCategoryList
			params["folder"] = "true"

		if get("scraper") == "shows" and get("category"):
			function = self.scrapeShowsGrid
			if get("show"):
				params["batch"] = "true"
				function = self.scrapeShow
			
		if get("scraper") == "movies" and get("category"):
			params["batch"] = "thumbnails"
			function = self.scrapeMoviesGrid		
			if get("subcategory"):
				params["folder"] = "true"
				del params["batch"]
				function = self.scrapeMovieSubCategory
		
		if get("scraper") == "categories" and get("category"):
			params["batch"] = "true"
			function = self.scrapeCategoriesGrid
		
		if (get("scraper") in ['current_trailers','game_trailers','popular_game_trailers','popular_trailers','trailers','upcoming_game_trailers','upcoming_trailers']):
			params["batch"] = "thumbnails"
			function = self.scrapeGridFormat
		
		if function:
			params["new_results_function"] = function
		
		return True
	
	def createUrl(self, params = {}):
		get = params.get
		page = str(int(get("page","0")) + 1)
		
		if (get("scraper") in self.urls):
			url = self.urls[get("scraper")]
			if url.find('%s') > 0:
				url = url % page
			elif url.find('?') > 0:
				url += "&p=" + page
			else:
				url += "?p=" + page
		
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
		
		if (get("scraper") == "shows" and not get("show")):
			url = self.urls["shows"] + "?hl=en"
			if (get("category")):
				category = get("category")
				category = urllib.unquote_plus(category)
				url = self.urls["shows"] + "/" + category
				if url.find("?") < 0:
					url += "?p=" + page + "&hl=en"
				else:
					url += "&p=" + page + "&hl=en"
			
			if (get("show")):
				show = urllib.unquote_plus(get("show"))
				if (show.find("p=") < 0):
					url = self.urls["show_list"] + "/" + show + "?hl=en"
				else:
					url = self.urls["show_list"] + "?" + show + "&hl=en"
				if (get("season")):
					url = url + "&s=" + get("season")
				
		if (get("scraper") == "movies"):
			if (get("category")):
				category = get("category")
				category = urllib.unquote_plus(category)
				if get("subcategory"):
					url = self.urls["main"] + "/movies/" + category + "?hl=en"
				else:
					url = self.urls["main"] + "/movies/" + category + "?p=" + page + "&hl=en"
			else:
				url = self.urls["movies"] + "?hl=en"
		
		if(get("scraper") == "music_top100"):
			url = self.urls["music"]
		
		return url
	
	def scrapeGridFormat(self, params = {}):
		get = params.get
		items = []
		next = "false"
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
		
		if status == 200:
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
				if (get("scraper") == "categories"):
					cell = "video-cell"
				
				while ( trailer != None ):
					videoid = trailer.div.a['href']
							
					if (videoid):
						if (videoid.find("=") > -1):
							videoid = videoid[videoid.find("=")+1:]
						
						items.append( (videoid, trailer.div.a.span.img['src']) )
					
					trailer = trailer.findNextSibling(name="div", attrs = { 'class':cell })
		
		return (items, status)
	
	def scrapeCategoryList(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " scrapeCategories "
		
		scraper = "categories"
		thumbnail = "explore"
		yobjects = []
		
		if (get("scraper") != "categories"):
			scraper = get("scraper")
			thumbnail = get("scraper")
		
		url = self.createUrl(params)
		(html, status) = self._fetchPage({"link":url})
		
		if status == 200:
			list = SoupStrainer(name="div", attrs = {"class":"yt-uix-expander-body"})
			categories = BeautifulSoup(html, parseOnlyThese=list)
			
			if len(categories) == 0:
				list = SoupStrainer(name="div", id = "browse-filter-menu")
				categories = BeautifulSoup(html, parseOnlyThese=list)
			
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
							cat = category.a["href"].replace("/" + scraper + "/", "")
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
							if get("scraper") == "movies":
								if cat.find("pt=nr") > 0:
									category = category.findNextSibling(name = "li")
									continue
								elif cat == "indian-cinema":
									item["subcategory"] = "true"
							
							cat = urllib.quote_plus(cat)
							item['category'] = cat
							item['scraper'] = scraper
							item["thumbnail"] = thumbnail
							yobjects.append(item)
						
						category = category.findNextSibling(name = "li")
					ul = ul.findNextSibling(name = "ul")
		
			if (not yobjects):
				return (self.__language__(30601), 303)
		
		return (yobjects, status)
	
	def paginator(self, params = {}):
		get = params.get
		
		status = 303
		result = []
		next = 'false'
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
				
		if not get("page"):
			(result, status) = params["new_results_function"](params)
			
			print "new result " + repr(result)
			if len(result) == 0:
				return (result, 303)
			
			self.__storage__.store(params, result)
		else:
			result = self.__storage__.retrieve(params)
			print "retrieved result " + repr(result)
		
		if not get("folder"):
			if ( per_page * ( page + 1 ) < len(result) ):
				next = 'true'
			
			if (get("fetch_all") != "true"):
				result = result[(per_page * page):(per_page * (page + 1))]
			
			if len(result) == 0:
				return (result, status)
		
		if get("batch") == "thumbnails":
			(result, status) = self.getBatchDetailsThumbnails(result, params)
		elif get("batch"):
			(result, status) = self.getBatchDetails(result, params)
		
		if get("batch"):
			del params["batch"]
		
		if next == "true":
			self.addNextFolder(result, params)
		
		return (result, status)
	
	def scrape(self, params = {}):
		get = params.get
		
		if (get("scraper") == "watch_later"):
			return self.scrapeWatchLater(params)
		self.getNewResultsFunction(params)
		return self.paginator(params)
	
if __name__ == '__main__':
	sys.exit(0)