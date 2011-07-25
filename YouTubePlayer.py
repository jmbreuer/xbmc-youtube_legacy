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

import sys, urllib, re, os.path, datetime, time
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
import YouTubeCore, YouTubeUtils
from xml.dom.minidom import parseString

class YouTubePlayer(YouTubeCore.YouTubeCore, YouTubeUtils.YouTubeUtils):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__ 
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	def __init__(self):
		# YouTube Playback Feeds
		self.urls['video_stream'] = "http://www.youtube.com/watch?v=%s&safeSearch=none"
		self.urls['embed_stream'] = "http://www.youtube.com/get_video_info?video_id=%s"
		self.urls['timed_text_index'] = "http://www.youtube.com/api/timedtext?type=list&v=%s"
		self.urls['video_info'] = "http://gdata.youtube.com/feeds/api/videos/%s"
		self.urls['close_caption_url'] = "http://www.youtube.com/api/timedtext?type=track&v=%s&name=%s&lang=%s"
		self.urls['transcription_url'] = "http://www.youtube.com/api/timedtext?caps=asr&kind=asr&type=track&key=yttt1&expire=%s&sparams=caps,expire,v&v=%s&signature=%s&lang=en"
		self.urls['annotation_url'] = "http://www.youtube.com/api/reviews/y/read2?video_id=%s"
		self.urls['remove_watch_later'] = "http://www.youtube.com/addto_ajax?action_delete_from_playlist=1"
		
	# ================================ Subtitle Downloader ====================================
	def downloadSubtitle(self, video = {}):
		get = video.get
		
		result = ""
		
		if self.__settings__.getSetting("annotations") == "true" and not video.has_key("downloadPath"):

			xml = self._fetchPage({"link": self.urls["annotation_url"] % get('videoid')})
			if xml["status"] == 200 and xml["content"]:
				result += self.transformAnnotationToSSA(xml["content"])

                if self.__settings__.getSetting("lang_code") != "0":
			subtitle_url = self.getSubtitleUrl(video)

			if not subtitle_url and self.__settings__.getSetting("transcode") == "true":
				html = self._fetchPage({"link": self.urls["video_stream"] % get("videoid")})
				if html["status"] == 200:
					subtitle_url = self.getTranscriptionUrl(html["content"], video) 
		
			if subtitle_url:
				xml = self._fetchPage({"link": subtitle_url})
				if xml["status"] == 200 and xml["content"]:
					result += self.transformSubtitleXMLtoSRT(xml["content"])

		if len(result) > 0:
			result = "[Script Info]\r\n; This is a Sub Station Alpha v4 script.\r\n; For Sub Station Alpha info and downloads,\r\n; go to http://www.eswat.demon.co.uk/\r\n; or email kotus@eswat.demon.co.uk\r\nTitle: Auto Generated\r\nScriptType: v4.00\r\nCollisions: Normal\r\nPlayResY: 1280\r\nPlayResX: 800\r\n\r\n[V4 Styles]\r\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\r\nStyle: Default,Arial,80,&H00FFFFFF&,65535,65535,&00000000&,-1,0,1,3,2,2,30,30,30,0,0\r\nStyle: speech,Arial,60,0,65535,65535,&H4BFFFFFF&,0,0,3,1,0,1,30,30,30,0,0\r\nStyle: popup,Arial,60,0,65535,65535,&H4BFFFFFF&,0,0,3,3,0,1,30,30,30,0,0\r\nStyle: highlightText,Wolf_Rain,60,15724527,15724527,15724527,&H4BFFFFFF&,0,0,1,1,2,2,5,5,30,0,0\r\n\r\n[Events]\r\nFormat: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\r\n" + result

			result += "Dialogue: Marked=0,0:00:0.00,0:00:0.00,Default,Name,0000,0000,0000,,\r\n" # This solves a bug.
			self.saveSubtitle(result, video)
			return True
		
		return False
	
	def getSubtitleUrl(self, video = {}):
		get = video.get
		url = ""
		
		xml = self._fetchPage({"link": self.urls["timed_text_index"] % get('videoid')})
		
		if self.__dbg__:
			print self.__plugin__ + " subtitle index: " + repr(xml["content"])
		
		if xml["status"] == 200:
			dom = parseString(xml["content"])
			entries = dom.getElementsByTagName("track")

			subtitle = ""
			code = ""
			if len(entries) > 0:
				# Fallback to first in list.
				subtitle = entries[0].getAttribute("name").replace(" ", "%20")
				code = entries[0].getAttribute("lang_code")

			lang_code = [ self.__language__( 30277 ), self.__language__( 30278  ), self.__language__( 30279 ), self.__language__( 30280 ), self.__language__( 30281 ), self.__language__( 30282 ), self.__language__( 30283 )][int(self.__settings__.getSetting("lang_code"))]
			for node in entries:
				if node.getAttribute("lang_code") == lang_code:
					subtitle = node.getAttribute("name").replace(" ", "%20")
					code = lang_code
					if self.__dbg__:
						print self.__plugin__ + " found subtitle specified: " + subtitle + " - " + code
					break
			
				if node.getAttribute("lang_code") == "en":
					subtitle = node.getAttribute("name").replace(" ", "%20")
					code = "en"
					if self.__dbg__:
						print self.__plugin__ + " found subtitle default: " + subtitle + " - " + code

			if code:
				url = self.urls["close_caption_url"] % ( get("videoid"), subtitle, code)
		
		if self.__dbg__:
			print self.__plugin__ + " found subtitle url: " + repr(url)
		
		return url

	def saveSubtitle(self, result, video = {}):
		get = video.get
		
		filename = ''.join(c for c in video['Title'] if c in self.VALID_CHARS) + "-[" + get('videoid') + "]" + ".ssa"
		path = os.path.join( xbmc.translatePath( "special://temp" ), filename )
		
		w = open(path, "w")
		w.write(result.encode('utf-8'))
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
		i = 0
		for node in entries:
			if node:
				if node.firstChild:
					if node.firstChild.nodeValue:
						text = self.replaceHtmlCodes(node.firstChild.nodeValue)
						start = ""
						
						if node.getAttribute("start"):
							start = str(datetime.timedelta(seconds=float(node.getAttribute("start")))).replace("000", "")
							if ( start.find(".") == -1 ):
								start += ".000"
						
						dur = ""
						if node.getAttribute("dur"):
							dur = str(datetime.timedelta(seconds=float(node.getAttribute("start")) + float(node.getAttribute("dur")))).replace("000", "")
							if ( dur.find(".") == -1 ):
								dur += ".000"
						
						if start and dur:
							result += "Dialogue: Marked=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n" % ( "0", start, dur, "Default", "Name", "0000", "0000", "0000", "", text )
		
		return result

	def transformAnnotationToSSA(self, xml):
		dom = parseString(xml)
		entries = dom.getElementsByTagName("annotation")
		result = ""
		i = 0
		for node in entries:
			if node:
				stype = node.getAttribute("type")
				style = node.getAttribute("style")

				if stype == "highlight":
					linkt = self._getNodeAttribute(node, "url", "type", "")
					linkv = self._getNodeAttribute(node, "url", "value", "")
					if linkt == "video":
						if self.__dbg__:
							print self.__plugin__ + " transformAnnotationToSSA Reference to video : " + linkv
				elif node.firstChild:
					if node.firstChild.nodeValue:
						text = self._getNodeValue(node, "TEXT", "")
						start = ""

						if node.getAttribute("start"):
							start = str(datetime.timedelta(seconds=float(node.getAttribute("start")))).replace("000", "")
							if ( start.find(".") == -1 ):
								start += ".000"
						
						dur = ""
						if node.getAttribute("dur"):
							dur = str(datetime.timedelta(seconds=float(node.getAttribute("start")) + float(node.getAttribute("dur")))).replace("000", "")
							if ( dur.find(".") == -1 ):
								dur += ".000"

						if style == "popup":
							cnode = node.getElementsByTagName("rectRegion")
						elif style == "speech":
							cnode = node.getElementsByTagName("anchoredRegion");
						elif style == "higlightText":
							cnode = False
						else:
							cnode = False

						if cnode:
							if cnode.item(0):
								start = cnode.item(0).getAttribute("t")
							if cnode.item(1):
								dur = cnode.item(1).getAttribute("t")
						
						if start and dur and style != "highlightText":
							marginL = "0000"
							marginV = 1280 * float(cnode.item(0).getAttribute("y")) / 100
							marginV += 1280 * float(cnode.item(0).getAttribute("h")) / 100
							marginV = 1280 - int(marginV)
							old_x = int((800 * float(cnode.item(0).getAttribute("x")) / 100) )
							marginL = old_x
							result += "Dialogue: Marked=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n" % ( "0", start, dur, style, "Name", marginL, "0000", marginV, "", text )
				else:
					if self.__dbg__:
						print self.__plugin__ + " transformAnnotationToSSA wrong type"

		return result
		
	def addSubtitles(self, video = {}):
		get = video.get
		if self.__dbg__:
			print self.__plugin__ + " addSubtitles fetching subtitle if available"
		
		filename = ''.join(c for c in video['Title'] if c in self.VALID_CHARS) + "-[" + get('videoid') + "]" + ".ssa"

		download_path = os.path.join( self.__settings__.getSetting( "downloadPath" ), filename )
		path = os.path.join( xbmc.translatePath( "special://temp" ), filename )
		
		set_subtitle = False
		if xbmcvfs.exists(download_path):
			path = download_path
			set_subtitle = True
		elif xbmcvfs.exists(path):
			set_subtitle = True
		elif self.downloadSubtitle(video):
			set_subtitle = True

		if xbmcvfs.exists(path) and not video.has_key("downloadPath") and set_subtitle:
			player = xbmc.Player()
			while not player.isPlaying():
				print self.__plugin__ + " addSubtitles Waiting for playback to start "
				time.sleep(1)
			xbmc.Player().setSubtitles(path);

			if self.__dbg__:
				print self.__plugin__ + " addSubtitles added subtitle %s to playback" % path
	
	# ================================ Video Playback ====================================
	
	def playVideo(self, params = {}):
		get = params.get
		
		(video, status) = self.getVideoObject(params);
		
		if status != 200:
			if self.__dbg__ : 
				print self.__plugin__ + " construct video url failed contents of video item " + repr(video)
			self.showErrorMessage(self.__language__(30603), video["apierror"], status)
			return False
		
		listitem=xbmcgui.ListItem(label=video['Title'], iconImage=video['thumbnail'], thumbnailImage=video['thumbnail'], path=video['video_url']);		
		listitem.setInfo(type='Video', infoLabels=video)
		
		if self.__dbg__:
			print self.__plugin__ + " - Playing video: " + self.makeAscii(video['Title']) + " - " + get('videoid') + " - " + video['video_url']
		
		xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
		
		if self.__settings__.getSetting("lang_code") != "0" or self.__settings__.getSetting("annotations") == "true":
			self.addSubtitles(video)
		
		if (get("watch_later") == "true" and get("playlist") and get("playlist_entry_id")):
			if self.__dbg__:
				print self.__plugin__ + " removing video from watch later playlist"
			self.remove_from_playlist(params)
			
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
		
		# For /get_video_info
		fmtSource = re.findall('&fmt_stream_map=(.*)&', html);
		if not fmtSource:
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
			print self.__plugin__ + " couldn't locate fmt_url_map or fmt_stream_map, no videos on page?"
			return links
		
		for fmt_url in fmt_url_map:				
			quality = "5"
			final_url = ""
			if (len(fmt_url) > 7 and fmt_url.find(":\\/\\/") > 0 and fmt_url.find('liveplay?') < 0):
				final_url = fmt_url
				if (fmt_url.rfind(',') > fmt_url.rfind('\/id\/')):
					final_url = fmt_url[:fmt_url.rfind(',')]
				
				if (final_url.rfind('\/itag\/') > 0):
					quality = final_url[final_url.rfind('\/itag\/') + 8:]

			elif len(fmt_url) > 7 and fmt_url.find('liveplay?') > 0:
				final_url = fmt_url
				if (fmt_url.rfind(',') > fmt_url.rfind('&id=')): 
					final_url = fmt_url[:fmt_url.rfind(',')]
				
				if (final_url.rfind('itag=') > 0):
					quality = final_url[final_url.rfind('itag=') + 5:]
					quality = quality[:quality.find('&')]
			
			if final_url and quality:
				links[int(quality)] = final_url
		
		for quality, url in links.items():
			url = url.replace('\/','/')
			if (url.find('rtmp') >= 0 and swf_url):
				playpath = ""
				for fmt_url in fmt_url_map:
					if fmt_url.find('/' + str(quality)) > 0:
						playpath = fmt_url
						break
				
				pchn = ""
				if html.find("ptchn=") > 0:
					pchn = html[html.find("ptchn=") + len("ptchn="):]
					pchn = pchn[:pchn.find('&')]
				
				ptk = ""
				if html.find("ptk=") > 0:
					ptk = html[html.find("ptk=") + len("ptk="):]
					ptk = ptk[:ptk.find("&")]
				
				if playpath:
					if pchn:
						playpath += '?pchn='+ pchn
					if ptk:
						playpath += '&ptk=' + ptk
					
					playpath = playpath.replace('\/','/')
					
					links[quality] = url + " swfurl=%s playpath=%s swfvfy=1" % (swf_url, playpath)
				else:
					links[quality] = url + " swfurl=%s swfvfy=1" % swf_url
		
		return links

	def getVideoUrlMap(self, html, video = {}):
		links = {}
			
		# For /get_video_info
		fmtSource = re.findall('&fmt_url_map=(.*)&', html);
		if not fmtSource:
			fmtSource = re.findall('"fmt_url_map": "([^"]+)"', html);
				
		fmt_url_map = []
		if fmtSource:
			fmtSource = fmtSource[0].replace('\u0026','&')
			fmt_url_map = urllib.unquote_plus(fmtSource).split('|')
		
		for fmt_url in fmt_url_map:
			if (len(fmt_url) > 7 and fmt_url.find("&") > 7):
				quality = "5"
				final_url = fmt_url
				
				if (fmt_url.rfind(',') > fmt_url.rfind('&id=')): 
					final_url = fmt_url[:fmt_url.rfind(',')]
				
				if (final_url.rfind('itag=') > 0):
					quality = final_url[final_url.rfind('itag=') + 5:]
					quality = quality[:quality.find('&')]
					
				links[int(quality)] = final_url.replace('\/','/')
		
		if len(links) > 0:
			video["url_map"] = "true"
		
		return links
		
	def getAlert(self, html, params = {}):
		get = params.get
		result = self.__language__(30617)	
		
		search_string = 'class="yt-alert-content">'
		if html.find(search_string) > 0:
			result = html[html.find(search_string) + len(search_string): html.find('</div>', len(search_string))].strip()
		
		return result
	
	def getInfo(self, params):
		get = params.get
		video = {}
		
		result = self._fetchPage({"link": self.urls["video_info"] % get("videoid"), "api": "true"})

		if result["status"] == 200:
			video = self.getVideoInfo(result["content"], params)
		
			if len(result) == 0:
				if self.__dbg__:
					print self.__plugin__ + " Couldn't parse API output, YouTube doesn't seem to know this video id?"
				video["apierror"] = self.__language__(30608)
				return (video, 303)
		else:
			if self.__dbg__:
				print self.__plugin__ + " Got API Error from YouTube!"
			video["apierror"] = result["content"]
			
			return (video,303)
		video = video[0]
		return (video, result["status"])
	
	def selectVideoQuality(self, links, params):
		get = params.get
		link = links.get
		video_url = ""

		if self.__dbg__:
			print self.__plugin__ + " selectVideoQuality : " #+ repr(links)
		
		if get("action") == "download":
			hd_quality = int(self.__settings__.getSetting( "hd_videos_download" ))
			if ( hd_quality == 0 ):
				hd_quality = int(self.__settings__.getSetting( "hd_videos" ))
		
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
		elif (link(59)): #<-- 480 for rtmpe
			video_url = link(59)
		elif (link(78)): #<-- seems to be around 400 for rtmpe
			video_url = link(78)
		elif (link(43)):
			video_url = link(43)
		elif (link(26)):
			video_url = link(26)
		elif (link(18)): #<-- 270 for rtmpe but 360 for http?
			video_url = link(18)
		elif (link(33)):
			video_url = link(33)
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
			video_url += " | " + self.USERAGENT
			
		return video_url
	
	def userSelectsVideoQuality(self, params, links):
		get = params.get
		link = links.get
		list = []
		choices = []
		
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
		selected = dialog.select(self.__language__(30518), choices)
		
		if selected > -1:
			(quality, message) = list[selected]
			return link(quality)
		
		return ""
	
	def getVideoObject(self, params):
		get = params.get
		video = {}
		links = []
				
		(video, status) = self.getInfo(params)
		
		#Check if file has been downloaded locally and use that as a source instead
		if (status == 200 and get("action","") != "download"):
			path = self.__settings__.getSetting( "downloadPath" )
			path = "%s%s-[%s].mp4" % (path, ''.join(c for c in video['Title'] if c in self.VALID_CHARS), video["videoid"])
			try:
				if xbmcvfs.exists(path):
					video['video_url'] = path
					return (video, 200)
			except:
				print self.__plugin__ + " attempt to locate local file failed with unknown error, trying youtube instead"

		(links, video) = self._getVideoLinks(video, params)

		if links:
			video["video_url"] = self.selectVideoQuality(links, params)
			if video["video_url"] == "":
				video['apierror'] = self.__language__(30618)
				status = 303
		else:
			status = 303
			vget = video.get
			if vget("live_play"):
				video['apierror'] = self.__language__(30612)
			elif vget("stream_map"):
				video['apierror'] = self.__language__(30620)
			else:
				video['apierror'] = self.__language__(30618)
		
		return (video, status)

	def _getVideoLinks(self, video, params):
		get = params.get
		links = []

		if self.__dbg__:
			print self.__plugin__ + " _getVideoLinks trying website"

		result = self._fetchPage({"link": self.urls["video_stream"] % get("videoid")})

		html = urllib.unquote_plus(result["content"])

		vget = video.get
		if result["status"] == 403:
			video['apierror'] = self.getAlert(html, params)
		elif result["status"] != 200:
			if not vget('apierror'):
				video['apierror'] = self.__language__(30617)
		
		if result["status"] == 200:	
			links = self.getVideoUrlMap(html, video)

		if len(links) == 0 and get("action") != "download":
			links = self.getVideoStreamMap(html, video)

		if len(links) > 0:
			return (links, video)


		# If nothing is found, try the embeded link
		
		# Get data from /get_video_info
		if self.__dbg__:
			print self.__plugin__ + " _getVideoLinks trying embedded"
			
		result = self._fetchPage({"link": self.urls["embed_stream"] % get("videoid") })
		
		if result["content"].find("status=fail") > -1: # this is
			result["status"] = 303
			#result["content"] = re.compile('reason=(.*)%3Cbr').findall(result["content"])[0]

		if result["status"] == 200:
			links = self.getVideoUrlMap(result["content"], video)
			if len(links) == 0 and get("action") != "download":
				links = self.getVideoStreamMap(result["content"], video)

		return (links, video)
