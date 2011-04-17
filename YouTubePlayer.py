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

import sys, urllib, urllib2, re, os.path, datetime
from xml.dom.minidom import parseString
import xbmc

class YouTubePlayer(object):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	__dbgv__ = False

	urls = {};
	# YouTube General Feeds
	urls['video_stream'] = "http://gdata.youtube.com/feeds/api/playlists/%s"
	urls['timed_text_index'] = "http://www.youtube.com/api/timedtext?type=list&v=%s"
	urls['video_info'] = "http://gdata.youtube.com/feeds/api/videos/%s"
	
	def saveSubtitle(self, params = {}):
		f = open("http://www.youtube.com/api/timedtext?type=list&v=" + params['videoid'], "r")
		dom = parseString(f.read())
		f.close()
		entries = dom.getElementsByTagName("track")
		name = ""
		ename = ""
		lang_code = [ self.__language__( 30277 ), self.__language__( 30278  ), self.__language__( 30279 ), self.__language__( 30280 ), self.__language__( 30281 ), self.__language__( 30282 ), self.__language__( 30283 )][int(self.__settings__.getSetting("lang_code"))]
		for node in entries:
			if node.getAttribute("lang_code") == lang_code:
				name = node.getAttribute("name").replace(" ", "%20")
			if node.getAttribute("lang_code") == "en":
				ename = node.getAttribute("name").replace(" ", "%20")

		if self.__dbg__:
			print self.__plugin__ + " saveSubtitle: lang_code: " + lang_code + " - name: " + name + " - ename: " + ename + " - transcode: " + self.__settings__.getSetting("transcode") + " - trans_url: " + params['trans_url']

		if name == "" and ename == "":
			if params['trans_url'] == "" or self.__settings__.getSetting("transcode") == "false":
				return False

			if self.__dbg__:
				print self.__plugin__ + " saveSubtitle: Getting transcription: " + params['trans_url']

			f = open(params['trans_url'], "r")
			dom = parseString(f.read())
			f.close()
		else:
			if name == "":
				if self.__dbg__:
					print self.__plugin__ + " saveSubtitle: Getting default subtitles"
				f = open("http://www.youtube.com/api/timedtext?type=track&v=" + params['videoid'] +"&name=" + ename + "&lang=en", "r")
			else:
				if self.__dbg__:
					print self.__plugin__ + " saveSubtitle: Getting " + name + " subtitles"
				f = open("http://www.youtube.com/api/timedtext?type=track&v=" + params['videoid'] +"&name=" + name + "&lang=" + lang_code, "r")

			dom = parseString(f.read())
			f.close()
		entries = dom.getElementsByTagName("text")
		i = 0;
		ret = ""
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
						ret += start + " --> " + ( dur ) + "\n" + text + "\n\n"

		path = os.path.join( xbmc.translatePath( "special://temp" ), params['videoid'] + ".srt" )
		w = open(path, "w")
		ret = ret.replace("&#39;", "'")
		w.write(ret.encode('utf-8'))
		w.close()
		return True

	def construct_video_url(self, params, encoding = 'utf-8', download = False):
		get = params.get
		if ( not get("videoid") ):
			return ( "", 200)

		videoid = get("videoid")
		
		if self.__dbg__:
			print self.__plugin__ + " construct_video_url : " + repr(videoid)

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
		
		if download:
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
		
		(fmtSource, swfConfig, video['stream_map'], video['trans_url']) = self._extractVariables(videoid)
		
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
		if (video['stream_map'] == 'True'):
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
		
		if (video['stream_map'] == 'True'):
			video['swf_config'] = swfConfig
		
		video['video_url'] = video_url;

		if self.__dbg__:
			print self.__plugin__ + " construct_video_url done"

		return (video, 200);

	def arrayToPipe(self, input):
		pipedItems = ""
		for item in input:
			pipedItems += item + "|"
		return pipedItems
		
	def _extractVariables(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " extractVariables : " + repr(videoid)

		( htmlSource, status ) = self._fetchPage('http://www.youtube.com/watch?v=' +videoid + "&safeSearch=none&hl=en_us")

		if status != 200:
			if self.__dbg__:
				print self.__plugin__ + " extractVariables failed"
			return ( htmlSource, status, status )
		
		if self.__dbg__:
			print self.__plugin__ + " _fetchPage returned " #+ repr(htmlSource)

		swf_url = False

		fmtSource = re.findall('"fmt_url_map": "([^"]+)"', htmlSource);

		tempSource1 = htmlSource[htmlSource.find("ttsurl="):len(htmlSource)]
		tempSource = tempSource1[0:tempSource1.find("&amp;")+5]

		temp_url = re.findall('.*ttsurl=(.*)&amp;.*', tempSource)

		trans_url = ""
		if len(temp_url) > 0:
			temp_url = urllib.unquote(temp_url[0]).replace("\\", "")
			temp_url = temp_url.split("&")
			expire = ""
			signature = ""

			for item in temp_url: 
				if ( item.find("expire") == 0 ):
					expire = item[item.find("expire")+7:len(item)]
				if ( item.find("signature") == 0 ):
					signature = item[item.find("signature")+10:len(item)]
			if expire != "" and signature != "":
				trans_url = "http://www.youtube.com/api/timedtext?caps=asr&kind=asr&type=track&key=yttt1&expire=" + expire + "&sparams=caps%2Cexpire%2Cv&v=" + videoid + "&signature=" + signature + "&lang=en"

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
				
		return (fmtSource, swf_url, stream_map, trans_url)
	
	def _getAlert(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " _getAlert begin"
		
		http_result = self._fetchPage('http://www.youtube.com/watch?v=' +videoid + "&safeSearch=none", login = True)
		
		start = http_result.find('class="yt-alert-content">')
		if start == -1:
			return self.__language__(30622)
		
		start += len('class="yt-alert-content">')
		result = http_result[start: http_result.find('</div>', start)].strip()
		
		if self.__dbg__:
			print self.__plugin__ + " _getAlert done: " + repr(start)
		
		return result
	
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