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

import sys, urllib, re, os.path, datetime, time, urllib2
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
from xml.dom.minidom import parseString

class YouTubePlayer(object):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__ 
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__core__ = sys.modules[ "__main__" ].__core__
	__utils__ = sys.modules[ "__main__" ].__utils__

	urls = {};
	
	# YouTube Playback Feeds
	urls['video_stream'] = "http://www.youtube.com/watch?v=%s&safeSearch=none&hl=en_us"
	urls['timed_text_index'] = "http://www.youtube.com/api/timedtext?type=list&v=%s"
	urls['video_info'] = "http://gdata.youtube.com/feeds/api/videos/%s"
	urls['close_caption_url'] = "http://www.youtube.com/api/timedtext?type=track&v=%s&name=%s&lang=%s"
	urls['transcription_url'] = "http://www.youtube.com/api/timedtext?caps=asr&kind=asr&type=track&key=yttt1&expire=%s&sparams=caps,expire,v&v=%s&signature=%s&lang=en"
	urls['remove_watch_later'] = "http://www.youtube.com/addto_ajax?action_delete_from_playlist=1"
	
	# ================================ Subtitle Downloader ====================================
	def downloadSubtitle(self, video = {}):
		get = video.get

		subtitle_url = self.getSubtitleUrl(video)

		if not subtitle_url and self.__settings__.getSetting("transcode") == "true":
			(html, status) = self.__core__._fetchPage({"link": self.urls["video_stream"] % get("videoid")})
			if status == 200:
				subtitle_url = self.getTranscriptionUrl(html, video) 
		
		if subtitle_url:
			srt = ""
			(xml, status) = self.__core__._fetchPage({"link": subtitle_url})

			if status == 200 and xml:
				srt = self.transformSubtitleXMLtoSRT(xml)
			if len(srt) > 0:
				self.saveSubtitle(srt, video)
				return True
		
		return False
	
        def getSubtitleUrl(self, video = {}):
                get = video.get
                url = ""

                (xml, status) = self.__core__._fetchPage({"link": self.urls["timed_text_index"] % get('videoid')})
        	dom = parseString(xml)
                entries = dom.getElementsByTagName("track")

                subtitle = ""
                lang_code = [ self.__language__( 30277 ), self.__language__( 30278  ), self.__language__( 30279 ), self.__language__( 30280 ), self.__language__( 30281 ), self.__language__( 30282 ), self.__language__( 30283 )][int(self.__settings__.getSetting("lang_code"))]
                code = ""
                for node in entries:
                        if node.getAttribute("lang_code") == lang_code:
                                subtitle = node.getAttribute("name").replace(" ", "%20")
				code = lang_code
                                break
                        if node.getAttribute("lang_code") == "en":
                                subtitle = node.getAttribute("name").replace(" ", "%20")
				code = "en"

                if subtitle and code:
                        url = self.urls["close_caption_url"] % ( get("videoid"), subtitle, code)

                return url

	def saveSubtitle(self, srt, video = {}):
		get = video.get

		filename = ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS) + " [" + get('videoid') + "]" + ".srt"
		path = os.path.join( xbmc.translatePath( "special://temp" ), filename )

		w = open(path, "w")
		w.write(srt.encode('utf-8'))
		w.close()

		if video.has_key("downloadPath"):
			xbmcvfs.rename(path, os.path.join( video["downloadPath"], filename ))

	def getTranscriptionUrl(self, html, video = {}):
		get = video.get
		trans_url = ""	
		if (html.find("ttsurl=") > 0):	
			html = html[html.find("ttsurl="):len(html)]
			html = html[0:html.find("&amp;")+5]

			urls = re.findall('.*ttsurl=(.*)&amp;.*', html)
		
			if len(urls) > 0:
				urls = urllib.unquote(urls[0]).replace("\\", "")
				urls = urls.split("&")
				expire = ""
				signature = ""

				for item in urls: 
					if ( item.find("expire") == 0 ):
						expire = item[item.find("expire")+7:len(item)]
					if ( item.find("signature") == 0 ):
						signature = item[item.find("signature")+10:len(item)]
				
				if expire != "" and signature != "":
					trans_url = self.urls["transcription_url"] % (expire, get("videoid"), signature)
		return trans_url
		
	def transformSubtitleXMLtoSRT(self, xml):
		dom = parseString(xml)
		entries = dom.getElementsByTagName("text")
		
		result = ""
		for node in entries:
			if node:
				if node.firstChild:
					if node.firstChild.nodeValue:
						text = node.firstChild.nodeValue
						text = text.replace("&amp;", "&")
						text = text.replace("&quot;", '"')
						text = text.replace("&hellip;", "...")
						start = str(datetime.timedelta(seconds=float(node.getAttribute("start")))).replace("000", "")
						if ( start.find(".") == -1 ):
							start += ".000"
						dur = str(datetime.timedelta(seconds=float(node.getAttribute("start")) + float(node.getAttribute("dur")))).replace("000", "")
						if ( dur.find(".") == -1 ):
							dur += ".000"
						result += start + " --> " + ( dur ) + "\n" + text + "\n\n"
		result = result.replace("&#39;", "'")
		
		return result
		
	def addSubtitles(self, video = {}):
		get = video.get
		
		filename = ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS) + " [" + get('videoid') + "]" + ".srt"
		
		download_path = os.path.join( self.__settings__.getSetting( "downloadPath" ), filename )
		path = os.path.join( xbmc.translatePath( "special://temp" ), filename )

		set_subtitle = False
		if (os.path.exists(download_path)):
			path = download_path
			set_subtitle = True
		elif (os.path.exists(path)):
			set_subtitle = True
		elif (self.downloadSubtitle(video)): 
			set_subtitle = True
		
		if set_subtitle:
			xbmc.Player().setSubtitles(path)
			time.sleep(5)		
			xbmc.Player().setSubtitles(path)

	# ================================= Watch Later =====================================
	
	def removeWatchLater(self, params = {}):
		get = params.get
		data = urllib.urlencode({'video_ids': get("videoid"), 'session_token': get("session_token"), 'playlist_id': get("playlist"), 'index': get("index")})
		
		print self.__plugin__  + " calling remove from playlist with data " + repr(data)
		request = urllib2.Request(self.urls["remove_watch_later"])		
		request.add_header('Content-Type', 'application/x-www-form-urlencoded')
		request.add_header('User-Agent', self.__utils__.USERAGENT)
		request.add_header('Content-Length', str(len(data)))
		request.add_header('Cookie', 'LOGIN_INFO=' + self.__settings__.getSetting( "login_info" ))
		
		try:
			con = urllib2.urlopen(request, data);
			value = con.read()
			con.close()
		except:
			print self.__plugin__ + " remove from watch later failed with contents " + repr(value)
	
	# ================================ Video Playback ====================================
	
	def playVideo(self, params = {}):
		get = params.get
		
		(video, status) = self.getVideoObject(params);
		
		if status != 200:
			if self.__dbg__ : 
				print self.__plugin__ + " construct video url failed contents of video item " + repr(video)
			self.__utils__.showErrorMessage(self.__language__(30603), video["apierror"], status)
			return False
		
		listitem=xbmcgui.ListItem(label=video['Title'], iconImage=video['thumbnail'], thumbnailImage=video['thumbnail'], path=video['video_url']);		
		listitem.setInfo(type='Video', infoLabels=video)
		
		if self.__dbg__:
			print self.__plugin__ + " - Playing video: " + video['Title'] + " - " + get('videoid') + " - " + video['video_url']
		
		xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
		
		if self.__settings__.getSetting("lang_code") != "0":
			self.addSubtitles(video)
		
		if (get("watch_later") == "true" and get("playlist") and get("index")):
			self.removeWatchLater(params)
			#print self.__plugin__ + "trying to remove from watch later playlist"
			
		self.__settings__.setSetting( "vidstatus-" + video['videoid'], "7" )
	
	def getVideoStreamMap(self, html, video = {}):
		links = {}
		fmt_url_map = []
		if self.__dbg__:
			print self.__plugin__ + " fmt_url_map not found, searching for stream map"
		
		swf_url = ""		
		video["stream_map"] = "true"
		if (html.find("live_playback") > 0):
			video["live_play"] = "true"
		
		fmtSource = re.findall('"fmt_stream_map": "([^"]+)"', html);			
		if fmtSource:
			if self.__dbg__:
				print self.__plugin__ + " fmt_stream_map found"
			
			fmtSource = fmtSource[0].replace('\u0026','&')
			fmt_url_map = urllib.unquote_plus(fmtSource).split('|')
			swfConfig = re.findall('var swfConfig = {"url": "(.*)", "min.*};', html)
			if len(swfConfig) > 0:
				swf_url = swfConfig[0].replace("\\", "")
		else:
			print self.__plugin__ + " couldn't locate either fmt_url_map or fmt_stream_map, no videos on page?"
			return links 
			
		for fmt_url in fmt_url_map:				
			if (len(fmt_url) > 7 and fmt_url.find(":\\/\\/") > 0 and fmt_url.find('liveplay?') < 0):
				if (fmt_url.rfind(',') > fmt_url.rfind('\/id\/')):
					final_url = fmt_url[:fmt_url.rfind(',')]
					if (final_url.rfind('\/itag\/') > 0):
						quality = final_url[final_url.rfind('\/itag\/') + 8:]
					else :
						quality = "5"
					if (swf_url):
						final_url += " swfurl=%s swfvfy=1" % swf_url
					links[int(quality)] = final_url.replace('\/','/')
				else :
					final_url = fmt_url
					final_url = final_url
					if (final_url.rfind('\/itag\/') > 0):
						quality = final_url[final_url.rfind('\/itag\/') + 8:]
					else :
						quality = "5"
					if (swf_url):
						final_url += " swfurl=%s swfvfy=1" % swf_url 
					links[int(quality)] = final_url.replace('\/','/')
			elif len(fmt_url) > 7 and fmt_url.find('liveplay?') > 0:
				if (fmt_url.rfind(',') > fmt_url.rfind('&id=')): 
					final_url = fmt_url[:fmt_url.rfind(',')]
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else:
						quality = "5"
					if (final_url.find('rtmp') >= 0 and swf_url):
						final_url += " swfurl=%s swfvfy=1" % swf_url 
					links[int(quality)] = final_url.replace('\/','/')
				else:
					final_url = fmt_url
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else :
						quality = "5"
					if (final_url.find('rtmp') >= 0 and swf_url):
						final_url += " swfurl=%s swfvfy=1" % swf_url 
					links[int(quality)] = final_url.replace('\/','/')
				
		return links
	
	def getVideoUrlMap(self, html, video = {}):
		links = {}
		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', html);
		
		fmt_url_map = []
		if fmtSource:
			if self.__dbg__:
				print self.__plugin__ + " fmt_url_map found"
			fmtSource = fmtSource[0].replace('\u0026','&')
			fmt_url_map = urllib.unquote_plus(fmtSource).split('|')
			
		for fmt_url in fmt_url_map:
			if (len(fmt_url) > 7):
				if (fmt_url.rfind(',') > fmt_url.rfind('&id=')): 
					final_url = fmt_url[:fmt_url.rfind(',')]
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else:
						quality = "5"
					links[int(quality)] = final_url.replace('\/','/')
				else :
					final_url = fmt_url
					if (final_url.rfind('itag=') > 0):
						quality = final_url[final_url.rfind('itag=') + 5:]
						quality = quality[:quality.find('&')]
					else :
						quality = "5"
					links[int(quality)] = final_url.replace('\/','/')
		
		if len(links) > 0:
			video["url_map"] = "true"
		
		return links
	
	def getSessionToken(self, params, html):
		session_token =""
		if html.find('<input type="hidden" name="session_token" value="') > 0:
			session_token = html[html.find('<input type="hidden" name="session_token" value="') + len('<input type="hidden" name="session_token" value="'):]
			session_token = session_token[:session_token.find('"/>')]
		params["session_token"] = session_token
	
	def getAlert(self, html, params = {}):
		get = params.get
		result = self.__language__(30617)	
		
		search_string = 'class="yt-alert-content">'
		if html.find(search_string) > 0:
			result = html[html.find(search_string) + len(search_string): html.find('</div>', len(search_string))].strip()
		
		return result
	
	def getVideoInfo(self, params):
		get = params.get
		video = {}
		
		( result, status ) = self.__core__._fetchPage({"link": self.urls["video_info"] % get("videoid"), "api": "true"})

		if status == 200:				
			result = self.__core__.getVideoInfo(result, params)
		
			if len(result) == 0:
				if self.__dbg__:
					print self.__plugin__ + " Couldn't parse API output, YouTube doesn't seem to know this video id?"
				video["apierror"] = self.__language__(30629)
				return (video, 303)
		else:
			if self.__dbg__:
				print self.__plugin__ + " Got API Error from YouTube!"
			video["apierror"] = result
			
			return (video,303)
		video = result[0]
		return (video, status)
	
	def selectVideoQuality(self, links, params):
		get = params.get
		link = links.get
		if self.__dbg__:
			print self.__plugin__ + " url map: " + repr(links)
		video_url = ""
		
		if get("action") == "download":
			hd_quality = int(self.__settings__.getSetting( "hd_videos_download" ))
			if ( hd_quality == 0 ):
				hd_quality = int(self.__settings__.getSetting( "hd_videos" ))
			else:
				hd_quality -= 1
		else:
			if (not get("quality")):
				hd_quality = int(self.__settings__.getSetting( "hd_videos" ))
			else:
				if (get("quality") == "1080p"):
					hd_quality = 3
				elif (get("quality") == "720p"):
					hd_quality = 2
				else: 
					hd_quality = 1
		
		# SD videos are default, but we go for the highest res
		if (link(35)):
			video_url = link(35)
		elif (link(34)):
			video_url = link(34)
		elif (link(43)):
			video_url = link(43)
		elif (link(26)):
			video_url = link(26)
		elif (link(18)):
			video_url = link(18)
		elif (link(5)):
			video_url = link(5)
		
		if hd_quality > 1: #<-- 720p
			if (link(22)):
				video_url = link(22)
			if (link(45)):
				video_url = link(45)
		if hd_quality > 2: #<-- 1080p
			if (link(37)):
				video_url = link(37)
		
		if hd_quality == 0 and not get("quality"):
			return self.userSelectsVideoQuality(params, links)
		
		if not len(video_url) > 0:
			print self.__plugin__ + " construct_video_url failed, video_url not set"
			return video_url
		
		if get("action") != "download":
			video_url += " | " + self.__utils__.USERAGENT
			
		return video_url
	
	def userSelectsVideoQuality(self,params, links):
		get = params.get
		link = links.get
		list = []
		choices = []
		
		print "select video quality"
		if link(37):
			list.append((37,"1080p"))
		if link(22):
			list.append((22,"720p"))
		elif link(45):
			list.append((45,"720p"))	
		
		if link(35):
			list.append((18,"480p"))
		elif link(44):
			list.append((44,"480p"))
		
		if link(18):
			list.append((18,"380p"))
		
		if link(34):
			list.append((34,"360p"))
		elif link(43):
			list.append((43,"360p"))
		
		if link(5):
			list.append((5,"240p"))
		if link(17):
			list.append((17,"144p"))
		
		for (quality, message) in list:
			choices.append(message)
		
		dialog = xbmcgui.Dialog()
		selected = dialog.select(self.__language__(30537), choices)
		
		if selected > -1:
			(quality, message) = list[selected]
			return link(quality)
		
		return ""
	
	def getVideoObject(self, params):
		get = params.get
		video = {}
		
		(html, status) = self.__core__._fetchPage({"link": self.urls["video_stream"] % get("videoid")})
		
		if status != 200:
			video["apierror"] = html 
			return (video,status)
		
		if get("watch_later","false") == "true":
			self.getSessionToken(params, html)
		
		(video, status) = self.getVideoInfo(params)
		
		#Check if file has been downloaded locally and use that as a source instead
		if (status == 200 and get("action","") != "download"):
			path = self.__settings__.getSetting( "downloadPath" )
			path = "%s%s-[%s].mp4" % (path, ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS), video["videoid"])
			try:
				if os.path.exists(path):
					video['video_url'] = path
					return (video, 200)
			except:
				print self.__plugin__ + " attempt to locate local file failed with unknown error, trying youtube instead"
		
		vget = video.get
		if status == 403:
			video['apierror'] = self.getAlert(html, params)
		elif status != 200:
			if not vget('apierror'):
				video['apierror'] = self.__language__(30617)
		
		if status == 200:			
			links = self.getVideoUrlMap(html, video)
			
			if len(links) == 0:
				links= self.getVideoStreamMap(html, video)
		
		if not links:
			status = 303
			vget = video.get
			if vget("live_play"):
				video['apierror'] = self.__language__(30628)
			elif vget("stream_map"):
				video['apierror'] = self.__language__(30620)
			else:
				video['apierror'] = self.__language__(30618)
		else:
			video["video_url"] = self.selectVideoQuality(links, params)
		
		return (video, status)
