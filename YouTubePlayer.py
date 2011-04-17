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
import xbmc, xbmcgui, xbmcplugin
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
	urls['transcribtion_url'] = "http://www.youtube.com/api/timedtext?caps=asr&kind=asr&type=track&key=yttt1&expire=%s&sparams=caps,expire,v&v=%s&signature=%s&lang=en"
	
	# ================================ Subtitle Downloader ====================================
	def downloadSubtitle(self, video = {}):
		get = video.get
		subtitle_url = self.getSubtitleUrl(video)
		
		if not subtitle_url and self.__settings__.getSetting("transcode") == "true":
			(html, status) = self._fetchPage(self.urls["video_stream"] % get("videoid"))
			if status == 200:
				subtitle_url = self.getTranscriptionUrl(html, video) 
		
		if subtitle_url:
			srt = ""
			xml = self.__core__._fetchPage(subtitle_url)
			if len(xml) > 0:
				srt = self.transformSubtitleXMLtoSRT(xml)
			if len(srt) > 0:
				self.saveSubtitle(srt, video)	
				return True
		
		return False
	
	def saveSubtitle(self, srt, video = {}):
		get = video.get
		filename = ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS) + " [" + get('videoid') + "]" + ".srt"
		path = os.path.join( xbmc.translatePath( "special://temp" ), filename )
		w = open(path, "w")
		w.write(srt.encode('utf-8'))
		w.close()
		
	def getSubtitleUrl(self, video = {}):
		get = video.get
		url = ""
		
		xml = self.__core__._fetchPage(self.urls["timed_text_index"] % get('videoid'))
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

	# ================================ Video Playback ====================================
	
	def playVideo(self, params = {}):
		get = params.get
		
		(video, status) = self.getVideoObject(params);

		if status != 200:
			if self.__dbg__ : 
				print self.__plugin__ + " construct video url failed contents of video item " + repr(video)
			self.showErrorMessage(self.__language__(30603), video, status)
			return False
				
		listitem=xbmcgui.ListItem(label=video['Title'], iconImage=video['thumbnail'], thumbnailImage=video['thumbnail'], path=video['video_url']);		
		listitem.setInfo(type='Video', infoLabels=video)
		
		if self.__dbg__:
			print self.__plugin__ + " - Playing video: " + video['Title'] + " - " + get('videoid') + " - " + video['video_url']
		xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)

		if self.__settings__.getSetting("lang_code") != "0":
			self.addSubtitles(video)
		
		self.__settings__.setSetting( "vidstatus-" + video['videoid'], "7" )
	
	def getVideoStreamMap(self, html):
		links = {}
		fmt_url_map = []
		if self.__dbg__:
			print self.__plugin__ + " fmt_url_map not found, searching for stream map"
		
		swf_url = ""		
		fmtSource = re.findall('"fmt_stream_map": "([^"]+)"', html);
		if fmtSource:
			if self.__dbg__:
				print self.__plugin__ + " fmt_stream_map found"
			fmtSource = fmtSource.replace('\u0026','&')
			fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|')
			swfConfig = re.findall('var swfConfig = {"url": "(.*)", "min.*};', html)
			if len(swfConfig) > 0:
				swf_url = swfConfig[0].replace("\\", "")
		else:
			print self.__plugin__ + " couldn't locate either fmt_url_map or fmt_stream_map, no videos on page?"
			return links 
			
		for fmt_url in fmt_url_map:				
			if (len(fmt_url) > 7 and fmt_url.find(":\\/\\/") > 0):
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
		return links
	
	def getVideoUrlMap(self, html):
		links = {}
		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', html);
		
		fmt_url_map = []
		if fmtSource:
			if self.__dbg__:
				print self.__plugin__ + " fmt_url_map found"
			fmtSource = fmtSource.replace('\u0026','&')
			fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|')
			
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
					
		return links
	
	def getAlert(self, html, params = {}):
		get = params.get
		result = self.__language__(30622)	
		
		search_string = 'class="yt-alert-content">'
		if html.find(search_string) > 0:
			result = html[html.find(search_string) + len(search_string): html.find('</div>', len(search_string))].strip()
		
		return result
	
	def getVideoInfo(self, params):
		get = params.get
		
		( result, status ) = self._fetchPage(self.urls["video_info"] % get("videoid"), api = True)

		if status == 200:				
			result = self.__core__._getvideoinfo(result)
		
			if len(result) == 0:
				if self.__dbg__:
					print self.__plugin__ + " Couldn't parse API output, YouTube doesn't seem to know this video id?"
				return (result, 503)
		else:
			if self.__dbg__:
				print self.__plugin__ + " Got API Error from YouTube!"
				
		return (result, status)
	
	def selectVideoQuality(self, links, params):
		get = params.get
		link = links.get
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
					hd_quality = 2
				elif (get("quality") == "720p"):
					hd_quality = 1
				else: 
					hd_quality = 0
		
		# SD videos are default, but we go for the highest res
		if (get(35)):
			video_url = get(35)
		elif (get(34)):
			video_url = get(34)
		elif (get(18)):
			video_url = get(18)
		elif (get(5)):
			video_url = get(5)
		
		if hd_quality > 0: #<-- 720p
			if (get(22)):
				video_url = get(22)
		if hd_quality > 1: #<-- 1080p
			if (get(37)):
				video_url = get(37)
				
		if len(video_url) > 0:
			video_url += " | " + self.__utils__.USERAGENT
		else:
			print self.__plugin__ + " construct_video_url failed, video_url not set"

		return video_url
		
	def getVideoObject(self, params):
		get = params.get
		
		(html, status) = self._fetchPage(self.urls["video_stream"] % get("videoid"))
		(video, status) = self.getVideoInfo(params)
		
		#Check if file has been downloaded locally and use that as a source instead
		path = self.__settings__.getSetting( "downloadPath" )
		path = "%s%s-[%s].mp4" % (path, ''.join(c for c in video['Title'] if c in self.VALID_CHARS), video["videoid"])
		if os.path.exists(path):
			video['video_url'] = path
			return (video, 200)
		
		if status == 403:
			video['apierror'] = self.getAlert(html, params)
		elif status == 503:
			video['apierror'] = self.__language__(30605)
		elif status != 200:
			video['apierror'] = self.__language__(30617)
		
		if status == 200:
			
			links = self.getVideoUrlMap(html)
			if not links:
				links = self.getVideoStreamMap(html)
			if links:
				video["video_url"] = self.selectVideoQuality(links, params)
		
		return (video, status)