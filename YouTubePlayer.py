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

import sys, urllib, re, os.path, datetime
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
	# YouTube General Feeds
	
	urls['video_stream'] = "http://www.youtube.com/watch?v=%s&safeSearch=none&hl=en_us"
	urls['timed_text_index'] = "http://www.youtube.com/api/timedtext?type=list&v=%s"
	urls['video_info'] = "http://gdata.youtube.com/feeds/api/videos/%s"
	urls['close_caption_url'] = "http://www.youtube.com/api/timedtext?type=track&v=%s&name=%s&lang=%s"
	urls['transcribtion_url'] = "http://www.youtube.com/api/timedtext?caps=asr&kind=asr&type=track&key=yttt1&expire=%s&sparams=caps,expire,v&v=%s&signature=%s&lang=en"
	
	# ================================ Subtitle Downloader ====================================
	def downloadSubtitle(self, html, params = {}):
		get = params.get
		subtitle_url = self.getSubtitleUrl(params)
		
		if not subtitle_url and self.__settings__.getSetting("transcode") == "true":
			subtitle_url = self.getTranscriptionUrl(html, params) 
		
		if subtitle_url:
			srt = ""
			xml = self.__core__._fetchPage(subtitle_url)
			if len(xml) > 0:
				srt = self.transformSubtitleXMLtoSRT(xml, params)
			if len(srt) > 0:
				self.saveSubtitle(srt, params)				
		return True
	
	def saveSubtitle(self, srt, params = {}):
		get = params.get
		filename = get("Title") + " [" + get('videoid') + "]" + ".srt"
		
		path = os.path.join( xbmc.translatePath( "special://temp" ),  )
		w = open(path, "w")
		w.write(srt.encode('utf-8'))
		w.close()
		
	def getSubtitleUrl(self, params = {}):
		get = params.get
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
	
	def getTranscriptionUrl(self, html, params = {}):
		get = params.get
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

	def transformSubtitleXMLtoSRT(self, xml, params):
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
		
	# ================================ Video Playback ====================================
	
	def playVideo(self, params = {}):
		get = params.get
		(video, status) = self.__core__.construct_video_url(params);

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

		if self.__settings__.getSetting("lang_code") != "0" and "local" not in video:
			self.addSubtitles(video)
		
		self.__settings__.setSetting( "vidstatus-" + video['videoid'], "7" )
	
	def getVideoUrlMap(self, html, params):
		get = params.get
		
	
	def getAlert(self, html, params = {}):
		get = params.get
		result = self.__language__(30622)	
		
		search_string = 'class="yt-alert-content">'
		if html.find(search_string) > 0:
			result = html[html.find(search_string) + len(search_string): html.find('</div>', len(search_string))].strip()
		
		return result
	
	def getVideoInfo(self, params):
		result = []
		return result
	
	def getVideoUrl(self, params):
		get = params.get
		
		
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
		
	def construct_video_url(self, params):
		get = params.get
		
		videoid = get("videoid")
		
		video = self._get_details(videoid)
		
		if not video:
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url failed because of missing video from _get_details"
			return ( "", 500 )
		
		if ( 'apierror' in video ):
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url, got apierror: " + video['apierror']
			return (video['apierror'], 303)
		
		#Check if file has been downloaded locally and use that as a source instead
		path = self.__settings__.getSetting( "downloadPath" )
		path = "%s%s-[%s].mp4" % (path, ''.join(c for c in video['Title'] if c in self.VALID_CHARS), video["videoid"])
		if os.path.exists(path):
			video['video_url'] = path
			video['local'] = "true"
			return (video, 200)
		

		
		(fmtSource, swfConfig, video['stream_map']) = self._extractVariables(videoid)
		
		if ( not fmtSource ):
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url Hopefully this extra if check is now legacy THIS SHOULD NOT HAPPEN ANYMORE"
			return ( "", 500 ) 
		
		if ( video['stream_map'] == 303 ):
			return (fmtSource, 303)
		
		fmt_url_map = urllib.unquote_plus(fmtSource[0]).split('|')
		links = {};
		video_url = False

		print self.__plugin__ + " construct_video_url: stream_map : " + video['stream_map']
		if (video['stream_map'] == 'true'):
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url: stream map"
				
			for fmt_url in fmt_url_map:
				if self.__dbg__:
					print self.__plugin__ + " construct_video_url: fmt_url : " + repr(fmt_url)
					
				if (len(fmt_url) > 7 and fmt_url.find(":\\/\\/") > 0):
					if (fmt_url.rfind(',') > fmt_url.rfind('\/id\/')):
						final_url = fmt_url[:fmt_url.rfind(',')]
						final_url = final_url.replace('\u0026','&')
						if (final_url.rfind('\/itag\/') > 0):
							quality = final_url[final_url.rfind('\/itag\/') + 8:]
						else :
							quality = "5"
						links[int(quality)] = final_url.replace('\/','/')
					else :
						final_url = fmt_url
						final_url = final_url.replace('\u0026','&')
						if (final_url.rfind('\/itag\/') > 0):
							quality = final_url[final_url.rfind('\/itag\/') + 8:]
						else :
							quality = "5"
						links[int(quality)] = final_url.replace('\/','/')
		
		else:
			if self.__dbg__:
				print self.__plugin__ + " construct_video_url: non stream map" 
			for fmt_url in fmt_url_map:
				if (len(fmt_url) > 7):
					if (fmt_url.rfind(',') > fmt_url.rfind('&id=')): 
						final_url = fmt_url[:fmt_url.rfind(',')]
						final_url = final_url.replace('\u0026','&')
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
		
		if (video['stream_map'] == 'true'):
			video['swf_config'] = swfConfig
		
		video['video_url'] = video_url;

		if self.__dbg__:
			print self.__plugin__ + " construct_video_url done"

		return (video, 200);
		
	def getVideoHTML(self, params = {}):
		get = params.get
		( html, status ) = self._fetchPage("http://www.youtube.com/watch?v=%s&safeSearch=none&hl=en_us" % get("videoid"))
		
		
	def _extractVariables(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " extractVariables : " + repr(videoid)
		
		swf_url = False
		
		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', htmlSource);
		
		if fmtSource:
			if self.__dbg__:
				print self.__plugin__ + " fmt_url_map found"
			stream_map = "False"
		else:
			if self.__dbg__:
				print self.__plugin__ + " fmt_url_map not found, searching for stream map"
				
			swfConfig = re.findall('var swfConfig = {"url": "(.*)", "min.*};', htmlSource)
			if len(swfConfig) > 0:
				swf_url = swfConfig[0].replace("\\", "")
				
			fmtSource = re.findall('"fmt_stream_map": "([^"]+)"', htmlSource);
			if not fmtSource:
				print self.__plugin__ + " couldn't locate fmt_stream_map"
			
			stream_map = 'True'
			
		if self.__dbg__:
			print self.__plugin__ + " extractVariables done"
				
		return (fmtSource, swf_url, stream_map)
		
	def _get_details(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " _get_details: " + repr(videoid)

		( result, status ) = self._fetchPage("http://gdata.youtube.com/feeds/api/videos/" + videoid, api = True)

		if status == 200:				
			result = self._getvideoinfo(result)
		
			if len(result) == 0:
				if self.__dbg__:
					print self.__plugin__ + " _get_details result was empty"
				return False
			else:
				if self.__dbg__:
					print self.__plugin__ + " _get_details done"
				return result[0];
		else:
			if self.__dbg__:
				print self.__plugin__ + " _get_details got bad status: " + str(status)
			
			video = {}
			video['Title'] = "Error"
			video['videoid'] = videoid
			video['thumbnail'] = "Error"
			video['video_url'] = False

			if (status == 403):
				# Override the 403 passed from _fetchPage with error provided by youtube.
				video['apierror'] = self._getAlert(videoid)
				return video
			elif (status == 503):
				video['apierror'] = self.__language__(30605)
				return video
			else:
				video['apierror'] = self.__language__(30606) + str(status)
				return video