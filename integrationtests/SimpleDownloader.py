'''
   Simple Downloader plugin for XBMC
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

import sys
import urllib2
import os
import time
import DialogDownloadProgress


class SimpleDownloader():
        dialog = ""

        def __init__(self):
                self.version = "0.9.0"
                self.plugin = "SimpleDownloader-" + self.version

                self.INVALID_CHARS = "\\/:*?\"<>|"

                if sys.modules["__main__"].common:
                        self.common = sys.modules["__main__"].common
                else:
                        import CommonFunctions
                        common = CommonFunctions.CommonFunctions()
                        common.plugin = self.plugin

                try:
                        import StorageServer
                        self.cache = StorageServer.StorageServer()
                        self.cache.table_name = "Downloader"
                except:
                        import storageserverdummy as StorageServer
                        self.cache = StorageServer.StorageServer()
                        self.cache.table_name = "Downloader"

                if sys.modules["__main__"].xbmc:
                        self.xbmc = sys.modules["__main__"].xbmc
                else:
                        import xbmc
                        self.xbmc = xbmc

                if sys.modules["__main__"].xbmcvfs:
                        self.xbmcvfs = sys.modules["__main__"].xbmcvfs
                else:
                        try:
                                import xbmcvfs
                                self.xbmcvfs = xbmcvfs
                        except ImportError:
                                import xbmcvfsdummy as xbmcvfs
                                self.xbmcvfs = xbmcvfs

                if sys.modules["__main__"].dbglevel:
                        self.dbglevel = sys.modules["__main__"].dbglevel
                else:
                        self.dbglevel = 3

                if sys.modules["__main__"].dbg:
                        self.dbg = sys.modules["__main__"].dbg
                else:
                        self.dbg = True

                self.settings = sys.modules["__main__"].settings

                self.language = self.settings.getLocalizedString
                self.download_path = self.settings.getSetting("downloadPath")
                self.hide_during_playback = self.settings.getSetting("hideDuringPlayback") == "true"
                self.notification_length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(self.settings.getSetting('notification_length'))]

                if hasattr(sys.modules["__main__"], "settings"):
                        inherited_settings = sys.modules["__main__"].settings
                        if inherited_settings.getSetting("downloadPath"):
                                self.download_path = inherited_settings.getSetting("downloadPath")
                        if inherited_settings.getSetting("hideDuringPlayback"):
                                self.hide_during_playback = inherited_settings.getSetting("hideDuringPlayback") == "true"
                        if inherited_settings.getSetting("notification_length"):
                                self.notification_length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(inherited_settings.getSetting('notification_length'))]

                if sys.modules["__main__"].plugin:
                        self.plugin = sys.modules["__main__"].plugin

        def download(self, itemid, params={}):
                self.common.log("")

                if (not self.download_path):
                        self._showMessage(self.language(30600), self.language(30611))
                        self.settings.openSettings()
                        self.download_path = self.settings.getSetting("downloadPath")

                if self.cache.lock("SimpleDownloaderLock"):
                        self.common.log("Downloader not active, initializing downloader.")

                        self._addItemToQueue(itemid, params)
                        self._processQueue(params)
                        self.cache.unlock("SimpleDownloaderLock")
                else:
                        self.common.log("Downloader is active, Queueing item.")
                        self._addItemToQueue(itemid, params)

        def _processQueue(self, params={}):
                self.common.log("")
                (itemid, item) = self._getNextItemFromQueue()

                if item:
                        if not self.dialog:
                                self.dialog = DialogDownloadProgress.DownloadProgress()
                                self.dialog.create(self.language(30605), "")

                        while item:
                                if not "video_url" in item:
                                        print "a"
                                        if "apierror" in item:
                                                self._showMessage(self.language(30625), item["apierror"])
                                        else:
                                                self._showMessage(self.language(30625), "ERROR")
                                        self._removeItemFromQueue(itemid)
                                        item = self._getNextItemFromQueue()
                                        continue

                                if "stream_map" in item:
                                        print "b"
                                        self._showMessage(self.language(30607), self.language(30619))
                                        self._removeItemFromQueue(itemid)
                                        item = self._getNextItemFromQueue()
                                        continue

                                if item["video_url"].find("swfurl") > 0 or item["video_url"].find("rtmp") > -1:
                                        print "c"
                                        self.common.log("Found RTMP stream")
                                        (ditem, status) = self._downloadRTMP(item, params)
                                        if status != 200:
                                                self._showMessage(self.language(30625), self.language(30619))
                                else:
                                        print "d"
                                        (ditem, status) = self._downloadURL(item)
                                self._removeItemFromQueue(itemid)
                                item = self._getNextItemFromQueue()
                                print "done"

                        self.common.log("Finished download queue.")
                        if self.dialog:
                                self.dialog.close()
                                self.common.log("Closed dialog")
                        self.dialog = ""

        def _downloadRTMP(self, video, params={}):
                get = params.get
                self.common.log(video['Title'])

                if "player_url" in video:
                        player_url = video["player_url"]
                else:
                        player_url = None

                video["downloadPath"] = self.download_path
                if "videoid" in video:
                        filename = "%s-[%s].mp4" % (''.join(c for c in video['Title'].decode("utf-8") if c not in self.INVALID_CHARS), video["videoid"])
                else:
                        filename = "%s.mp4" % (''.join(c for c in video['Title'].decode("utf-8") if c not in self.INVALID_CHARS))

                filename_incomplete = os.path.join(self.xbmc.translatePath("special://temp").decode("utf-8"), filename)
                filename_complete = os.path.join(self.download_path.decode("utf-8"), filename)

                if self.xbmcvfs.exists(filename_complete):
                        self.xbmcvfs.delete(filename_complete)

                try:
                        import subprocess
                        probe_args = ['rtmpdump', '-B', '1'] + [[], ['-v']][get("live", "false") == "true"] + [[], ['-W', player_url]][player_url is not None] + ['-r', video["video_url"], '-o', filename_incomplete]
                        p = subprocess.Popen(probe_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        output = p.communicate()[1]
                        if output.find("filesize") > -1:
                                total_size = int(float(output[output.find("filesize") + len("filesize"):output.find("\n", output.find("filesize"))]))
                        else:
                                total_size = 0

                except (OSError, IOError):
                        self._showMessage(self.language(30600), self.language(30619))
                        return ({}, 500)

                basic_args = ['rtmpdump', '-V'] + [[], ['-v']][get("live", "false") == "true"] + [[], ['-W', player_url]][player_url is not None] + ['-r', video["video_url"], '-o', filename_incomplete]

                p = subprocess.Popen(basic_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.bytes_so_far = 0
                opercent = -1
                retval = 1
                if total_size == 0:
                        total_size = int(get("max_size", "10000000"))

                self.mark = time.time()
                self.queue_mark = 0.0
                self.old_percent = -1
                self.common.log('total_size ')
                for chunk in p.stderr:
                        self.bytes_so_far = os.path.getsize(filename_incomplete)
                        self.common.log('bytes_so_far : ' + str(self.bytes_so_far))
                        if total_size > 0:
                                percent = float(self.bytes_so_far) / float(total_size) * 100
                        else:
                                percent = opercent + 1
                                if percent == 100:
                                        percent = 0.1

                        if percent > self.old_percent:
                                self._updateProgress(video, percent)
                                self.old_percent = percent

                        if self.bytes_so_far >= total_size and total_size != 0:
                                self.common.log("Download complete")
                                retval = 0
                                break

                        # Some rtmp streams seem abort after ~ 99.8%. Don't complain for those
                        if total_size * 0.998 < self.bytes_so_far:
                                self.common.log("Download complete. Size disrepancy: " + str(total_size - self.bytes_so_far))
                                retval = 0
                                break

                if retval == 0:
                        if self.xbmcvfs.exists(filename_incomplete):
                                self.xbmcvfs.rename(filename_incomplete, filename_complete)
                                self.common.log("Download complete")
                        else:
                                self.common.log("Download complete but couldn't find file: " + filename_incomplete)

                        if not self.dialog:
                                self.dialog = DialogDownloadProgress.DownloadProgress()
                        self.dialog.update(heading=self.language(30604), label=video["Title"])

                        self.common.log("done")
                        return (video, 200)
                else:
                        self.common.log("Download failed")
                        return ({}, 500)

        def _downloadURL(self, item, params={}):
                self.common.log(item['Title'])

                item["downloadPath"] = self.download_path

                url = urllib2.Request(item['video_url'])
                url.add_header('User-Agent', self.common.USERAGENT)
                if "videoid" in item:
                        filename = "%s-[%s].mp4" % (''.join(c for c in item['Title'].decode("utf-8") if c not in self.INVALID_CHARS), item["videoid"])
                else:
                        filename = "%s.mp4" % (''.join(c for c in item['Title'].decode("utf-8") if c not in self.INVALID_CHARS))

                filename_incomplete = os.path.join(self.xbmc.translatePath("special://temp").decode("utf-8"), filename)
                filename_complete = os.path.join(self.download_path.decode("utf-8"), filename)

                if self.xbmcvfs.exists(filename_complete):
                        self.xbmcvfs.delete(filename_complete)

                file = self.common.openFile(filename_incomplete, "wb")
                con = urllib2.urlopen(url)

                total_size = 1
                chunk_size = 1024 * 8  # Taken from urllib.py

                if con.info().getheader('Content-Length').strip():
                        total_size = int(con.info().getheader('Content-Length').strip())

                try:
                        self.bytes_so_far = 0

                        self.old_percent = -1
                        self.mark = time.time()
                        self.queue_mark = 0.0
                        while 1:
                                chunk = con.read(chunk_size)

                                self.bytes_so_far += len(chunk)
                                percent = float(self.bytes_so_far) / float(total_size) * 100
                                percent = float(int(percent * 10)) / 10
                                file.write(chunk)

                                if percent > self.old_percent:
                                        self._updateProgress(item, percent)
                                        self.old_percent = percent

                                if not chunk:
                                        break

                        con.close()
                        file.close()
                except:
                        self.common.log("Download failed.")
                        try:
                                con.close()
                                file.close()
                        except:
                                self.common.log("Failed to close download stream and file handle")
                        self._showMessage(self.language(30625), "ERROR")
                        return ({}, 500)

                if self.xbmcvfs.exists(filename_incomplete):
                        self.xbmcvfs.rename(filename_incomplete, filename_complete)
                        self.common.log("Download complete")
                else:
                        self.common.log("Download complete but couldn't find file: " + filename_incomplete)

                if not self.dialog:
                        self.dialog = DialogDownloadProgress.DownloadProgress()
                self.dialog.update(heading=self.language(30604), label=item["Title"])

                self.common.log("done")
                return (item, 200)

        def _updateProgress(self, item, percent):
                queue = False
                new_mark = time.time()
                speed = int((self.bytes_so_far / 1024) / (new_mark - self.mark))

                if new_mark - self.queue_mark > 1.5:
                        queue = self.cache.get("SimpleDownloaderQueue")
                        self.queue = queue
                elif hasattr(self, "queue"):
                        queue = self.queue

                try:
                        items = eval(queue)
                except:
                        items = {}

                if new_mark - self.queue_mark > 1.5:
                        heading = "[%s] %sKb/s (%s%%)" % (len(items), speed, percent)
                        self.common.log("Updating %s - %s" % (heading, self.common.makeUTF8(item["Title"])), 2)
                        self.queue_mark = new_mark

                if self.xbmc.Player().isPlaying() and self.xbmc.getCondVisibility("VideoPlayer.IsFullscreen"):
                        if self.dialog:
                                self.dialog.close()
                                self.dialog = ""
                else:
                        if not self.dialog:
                                self.dialog = DialogDownloadProgress.DownloadProgress()
                                self.dialog.create(self.language(30605), "")

                        heading = "[%s] %s - %s%%" % (len(items), self.language(30624), percent)
                        self.dialog.update(percent=percent, heading=heading, label=item["Title"])

        #============================= Download Queue =================================
        def _getNextItemFromQueue(self):
                if self.cache.lock("SimpleDownloaderQueueLock"):
                        items = []

                        queue = self.cache.get("SimpleDownloaderQueue")
                        self.common.log("queue loaded : " + repr(queue))

                        if queue:
                                try:
                                        items = eval(queue)
                                except:
                                        items = []

                        item = {}
                        if len(items) > 0:
                                item = items[0]
                                self.common.log("returning : " + item[0])

                        self.cache.unlock("SimpleDownloaderQueueLock")
                        return item
                else:
                        self.common.log("Couldn't aquire lock")

        def _addItemToQueue(self, itemid, params={}):
                if self.cache.lock("SimpleDownloaderQueueLock"):

                        items = []
                        if itemid:
                                queue = self.cache.get("SimpleDownloaderQueue")
                                self.common.log("queue loaded : " + repr(queue))

                                if queue:
                                        try:
                                                items = eval(queue)
                                        except:
                                                items = []

                                append = True
                                for index, item in enumerate(items):
                                        (item_id, item) = item
                                        if item_id == itemid:
                                                print "FOUND ID"
                                                append = False
                                                del items[index]
                                                break
                                if append:
                                        items.append((itemid, params))
                                        self.common.log("Added: " + itemid + " to queue - " + str(len(items)))
                                else:
                                        items.insert(1, (itemid, params))
                                        self.common.log("Moved " + itemid + " to front of queue. - " + str(len(items)))

                                self.cache.set("SimpleDownloaderQueue", repr(items))

                        self.cache.unlock("SimpleDownloaderQueueLock")
                        self.common.log("Done")
                else:
                        self.common.log("Couldn't lock")

        def _removeItemFromQueue(self, itemid):
                print "D"
                if self.cache.lock("SimpleDownloaderQueueLock"):
                        print "De"
                        items = []

                        queue = self.cache.get("SimpleDownloaderQueue")
                        self.common.log("queue loaded : " + repr(queue))

                        if queue:
                                try:
                                        items = eval(queue)
                                except:
                                        items = []

                        for index, item in enumerate(items):
                                (queue_itemid, item) = item
                                if queue_itemid == itemid:
                                        del items[index]
                                        self.cache.set("SimpleDownloaderQueue", repr(items))
                                        self.common.log("Removed: " + queue_itemid + " from queue")

                        self.cache.unlock("SimpleDownloaderQueueLock")
                        self.common.log("Done")
                else:
                        self.common.log("Exception")

        def movieItemToPosition(self, itemid, position):
                if position > 0 and  self.cache.lock("SimpleDownloaderQueueLock"):

                        items = []
                        if itemid:
                                queue = self.cache.get("SimpleDownloaderQueue")
                                self.common.log("queue loaded : " + repr(queue))

                                if queue:
                                        try:
                                                items = eval(queue)
                                        except:
                                                items = []

                                self.common.log("pre items: %s " % repr(items))
                                for index, item in enumerate(items):
                                        (queue_itemid, item) = item
                                        if queue_itemid == itemid:
                                                print "FOUND ID"
                                                del items[index]
                                                items = items[:position] + [(queue_itemid, item)] + items[position:]
                                                break
                                self.common.log("post items: %s " % repr(items))

                                self.cache.set("SimpleDownloaderQueue", repr(items))

                        self.cache.unlock("SimpleDownloaderQueueLock")
                        self.common.log("Done")
                else:
                        self.common.log("Couldn't lock")

        # Shows a more user-friendly notification
        def _showMessage(self, heading, message):
                self.xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % (heading, message, self.notification_length))
