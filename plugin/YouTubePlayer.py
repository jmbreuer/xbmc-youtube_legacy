'''
   YouTube plugin for XBMC
    Copyright (C) 2010-2012 Tobias Ussing And Henrik Mosgaard Jensen

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

import sys
import urllib
import cgi
try: import simplejson as json
except ImportError: import json
import urllib


class YouTubePlayer():
    fmt_value = {
        5: "240p h263 flv container",
        18: "360p h264 mp4 container | 270 for rtmpe?",
        22: "720p h264 mp4 container",
        26: "???",
        33: "???",
        34: "360p h264 flv container",
        35: "480p h264 flv container",
        37: "1080p h264 mp4 container",
        38: "720p vp8 webm container",
        43: "360p h264 flv container",
        44: "480p vp8 webm container",
        45: "720p vp8 webm container",
        46: "520p vp8 webm stereo",
        59: "480 for rtmpe",
        78: "seems to be around 400 for rtmpe",
        82: "360p h264 stereo",
        83: "240p h264 stereo",
        84: "720p h264 stereo",
        85: "520p h264 stereo",
        100: "360p vp8 webm stereo",
        101: "480p vp8 webm stereo",
        102: "720p vp8 webm stereo",
        120: "hd720",
        121: "hd1080"
        }

    # YouTube Playback Feeds
    urls = {}
    urls['video_stream'] = "http://www.youtube.com/watch?v=%s&safeSearch=none"
    urls['embed_stream'] = "http://www.youtube.com/get_video_info?video_id=%s"
    urls['video_info'] = "http://gdata.youtube.com/feeds/api/videos/%s"

    def __init__(self):
        self.xbmcgui = sys.modules["__main__"].xbmcgui
        self.xbmcplugin = sys.modules["__main__"].xbmcplugin

        self.storage = sys.modules["__main__"].storage
        self.settings = sys.modules["__main__"].settings
        self.language = sys.modules["__main__"].language
        self.dbg = sys.modules["__main__"].dbg

        self.common = sys.modules["__main__"].common
        self.utils = sys.modules["__main__"].utils
        self.cache = sys.modules["__main__"].cache
        self.core = sys.modules["__main__"].core
        self.subtitles = sys.modules["__main__"].subtitles

    def playVideo(self, params={}):
        self.common.log(repr(params), 3)
        get = params.get

        (video, status) = self.getVideoObject(params)

        if status != 200:
            self.common.log(u"construct video url failed contents of video item " + repr(video))
            self.utils.showErrorMessage(self.language(30603), video["apierror"], status)
            return False

        listitem = self.xbmcgui.ListItem(label=video['Title'], iconImage=video['thumbnail'], thumbnailImage=video['thumbnail'], path=video['video_url'])

        listitem.setInfo(type='Video', infoLabels=video)

        self.common.log(u"Playing video: " + repr(video['Title']) + " - " + repr(get('videoid')) + " - " + repr(video['video_url']))

        self.xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)

        if self.settings.getSetting("lang_code") != "0" or self.settings.getSetting("annotations") == "true":
            self.subtitles.addSubtitles(video)

        if (get("watch_later") == "true" and get("playlist_entry_id")):
            self.common.log(u"removing video from watch later playlist")
            self.core.remove_from_watch_later(params)

        self.storage.storeValue("vidstatus-" + video['videoid'], "7")

    def getInfo(self, params):
        get = params.get
        video = self.cache.get("videoidcache" + get("videoid"))
        if len(video) > 0:
            self.common.log(u"returning cache ")
            return (eval(video), 200)

        result = self.core._fetchPage({"link": self.urls["video_info"] % get("videoid"), "api": "true"})

        if result["status"] == 200:
            video = self.core.getVideoInfo(result["content"], params)

            if len(video) == 0:
                self.common.log(u"- Couldn't parse API output, YouTube doesn't seem to know this video id?")
                video = {}
                video["apierror"] = self.language(30608)
                return (video, 303)
        else:
            self.common.log(u"- Got API Error from YouTube!")
            video = {}
            video["apierror"] = result["content"]

            return (video, 303)

        video = video[0]
        self.cache.set("videoidcache" + get("videoid"), repr(video))
        return (video, result["status"])

    def selectVideoQuality(self, links, params):
        get = params.get
        link = links.get
        video_url = ""

        self.common.log(u"")

        if get("action") == "download":
            hd_quality = int(self.settings.getSetting("hd_videos_download"))
            if (hd_quality == 0):
                hd_quality = int(self.settings.getSetting("hd_videos"))

        else:
            if (not get("quality")):
                hd_quality = int(self.settings.getSetting("hd_videos"))
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
        elif (link(59)):
            video_url = link(59)
        elif link(44):
            video_url = link(44)
        elif (link(78)):
            video_url = link(78)
        elif (link(34)):
            video_url = link(34)
        elif (link(43)):
            video_url = link(43)
        elif (link(26)):
            video_url = link(26)
        elif (link(18)):
            video_url = link(18)
        elif (link(33)):
            video_url = link(33)
        elif (link(5)):
            video_url = link(5)

        if hd_quality > 1:  # <-- 720p
            if (link(22)):
                video_url = link(22)
            elif (link(45)):
                video_url = link(45)
            elif link(120):
                video_url = link(120)
        if hd_quality > 2:
            if (link(37)):
                video_url = link(37)
            elif link(121):
                video_url = link(121)

        if link(38) and False:
            video_url = link(38)

        for fmt_key in links.iterkeys():
            if link(int(fmt_key)):
                if self.dbg:
                    text = repr(fmt_key) + " - "
                    if fmt_key in self.fmt_value:
                        text += self.fmt_value[fmt_key]
                    else:
                        text += "Unknown"

                    if (link(int(fmt_key)) == video_url):
                        text += "*"
                    self.common.log(text)
            else:
                self.common.log(u"- Missing fmt_value: " + repr(fmt_key))

        if hd_quality == 0 and not get("quality"):
            return self.userSelectsVideoQuality(params, links)

        if not len(video_url) > 0:
            self.common.log(u"- construct_video_url failed, video_url not set")
            return video_url

        if get("action") != "download":
            video_url += " | " + self.common.USERAGENT

        self.common.log(u"Done")
        return video_url

    def userSelectsVideoQuality(self, params, links):
        link = links.get
        quality_list = []
        choices = []

        if link(37):
            quality_list.append((37, "1080p"))
        elif link(121):
            quality_list.append((121, "1080p"))

        if link(22):
            quality_list.append((22, "720p"))
        elif link(45):
            quality_list.append((45, "720p"))
        elif link(120):
            quality_list.append((120, "720p"))

        if link(35):
            quality_list.append((35, "480p"))
        elif link(44):
            quality_list.append((44, "480p"))

        if link(18):
            quality_list.append((18, "380p"))

        if link(34):
            quality_list.append((34, "360p"))
        elif link(43):
            quality_list.append((43, "360p"))

        if link(5):
            quality_list.append((5, "240p"))
        if link(17):
            quality_list.append((17, "144p"))

        if link(38) and False:
            quality_list.append((37, "2304p"))

        for (quality, message) in quality_list:
            choices.append(message)

        dialog = self.xbmcgui.Dialog()
        selected = dialog.select(self.language(30518), choices)

        if selected > -1:
            (quality, message) = quality_list[selected]
            return link(quality)

        return ""

    def getVideoObject(self, params):
        self.common.log(repr(params))

        links = []
        (video, status) = self.getInfo(params)

        if status != 200:
            video['apierror'] = self.language(30618)
            return (video, 303)

        video_url = self.subtitles.getLocalFileSource(params, video)
        if video_url:
            video['video_url'] = video_url
            return (video, 200)

        (links, video) = self._getVideoLinks(video, params)

        if links:
            video["video_url"] = self.selectVideoQuality(links, params)
            if video["video_url"] == "":
                video['apierror'] = self.language(30618)
                status = 303
        else:
            status = 303
            vget = video.get
            if not "apierror" in video:
                if vget("live_play"):
                    video['apierror'] = self.language(30612)
                elif vget("stream_map"):
                    video['apierror'] = self.language(30620)
                else:
                    video['apierror'] = self.language(30618)

        self.common.log(u"Done : " + repr(status))
        return (video, status)

    def extractFlashVars(self, data):
        flashvars = {}

        for line in data.split("\n"):
            if line.strip().startswith("var swf = \""):
                p1 = line.find("=")
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                    continue
                data = line[p1 + 1:p2]
                break

        data = json.loads(data)
        data = data[data.find("flashvars"):]
        data = data[data.find("\""):]
        data = data[:1 + data[1:].find("\"")]


        for k, v in cgi.parse_qs(data).items():
            flashvars[k] = v[0]

        return flashvars

    def _getVideoLinks(self, video, params):
        self.common.log(u"trying website: " + repr(params))

        links = {}
        get = params.get

        result = self.core._fetchPage({"link": self.urls["video_stream"] % get("videoid")})

        if result["status"] != 200:
            return (links, video)

        flashvars = self.extractFlashVars(result["content"])

        if flashvars.has_key("ttsurl"):
            video["ttsurl"] = flashvars["ttsurl"]

        for url_desc in flashvars["url_encoded_fmt_stream_map"].split(","):
            url_desc_map = cgi.parse_qs(url_desc)

            if not (url_desc_map.has_key("url") or url_desc_map.has_key("stream")):
                continue

            key = int(url_desc_map["itag"][0])
            url = u""
            if url_desc_map.has_key("url"):
                url = urllib.unquote(url_desc_map["url"][0])
            elif url_desc_map.has_key("stream"):
                url = urllib.unquote(url_desc_map["stream"][0])

            if url_desc_map.has_key("sig"):
                signature=url_desc_map["sig"][0]
                url + u"&signature=" + signature

            links[key] = url


        if len(links) == 0:
            self.common.log(u"Couldn't find url map or stream map.")

            if not "apierror" in video:
                video['apierror'] = self.core._findErrors(result)
                if not video['apierror'] and fresult:
                    video['apierror'] = self.core._findErrors(fresult)

        self.common.log(u"Done")
        return (links, video)
