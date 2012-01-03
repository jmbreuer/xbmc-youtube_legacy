# -*- coding: utf-8 -*-
import BaseTestCase
import nose
import sys
import os
from mock import Mock


class TestYouTubeDownloader(BaseTestCase.BaseTestCase):
        def ttest_plugin_should_download_standard_videos(self):
                sys.modules["__main__"].xbmcvfs.rename.side_effect = os.rename
                sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
                sys.modules["__main__"].downloader._getNextItemFromQueue = Mock()
                (video, status) = sys.modules["__main__"].player.getVideoObject({"action": "download", "videoid": "54VJWHL2K3I"})
                sys.modules["__main__"].downloader._getNextItemFromQueue.side_effect = [("54VJWHL2K3I", video), {}]

                self.navigation.executeAction({"action": "download", "videoid": "54VJWHL2K3I"})
                assert(os.path.exists('./tmp/Roll a D6-[54VJWHL2K3I].mp4'))

        def ttest_plugin_should_download_agerestricted_over_18_videos(self):
                sys.modules["__main__"].xbmcvfs.rename.side_effect = os.rename
                sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
                sys.modules["__main__"].downloader._getNextItemFromQueue = Mock()
                (video, status) = sys.modules["__main__"].player.getVideoObject({"action": "download", "videoid": "fOdNOtS8ZIs"})
                sys.modules["__main__"].downloader._getNextItemFromQueue.side_effect = [("fOdNOtS8ZIs", video), {}]

                self.navigation.executeAction({"action": "download", "videoid": "fOdNOtS8ZIs", "no_embed": "true"})

                assert(os.path.exists("./tmp/נלה מהיפה והחנון בסטריפ צ'אט בקליפ של חובבי ציון-[fOdNOtS8ZIs].mp4"))

        def ttest_plugin_should_download_with_subtitles_when_available(self):
                sys.modules["__main__"].xbmcvfs.rename.side_effect = os.rename
                sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
                sys.modules["__main__"].downloader._getNextItemFromQueue = Mock()
                (video, status) = sys.modules["__main__"].player.getVideoObject({"action": "download", "videoid": "bUcszN8jRB8"})
                sys.modules["__main__"].downloader._getNextItemFromQueue.side_effect = [("bUcszN8jRB8", video), {}]

                self.navigation.executeAction({"action": "download", "videoid": "bUcszN8jRB8"})

                assert(os.path.exists('./tmp/Morning Dew — a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].mp4'))
                assert(os.path.exists('./tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa'))

if __name__ == "__main__":
        nose.runmodule()
