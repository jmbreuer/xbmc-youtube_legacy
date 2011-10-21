# -*- coding: utf-8 -*-
import BaseTestCase
import nose, sys
from mock import Mock

class TestYouTubePlayer(BaseTestCase.BaseTestCase):	
	def test_plugin_should_download_standard_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue = Mock()
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = ["54VJWHL2K3I", ""]
		
		self.navigation.executeAction({"action":"download", "videoid": "54VJWHL2K3I"})

		import os
		assert(os.path.exists('./tmp/Roll a D6-[54VJWHL2K3I].mp4'))

	def test_plugin_should_download_agerestricted_over_18_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue = Mock()
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = ["fOdNOtS8ZIs", ""]

		self.navigation.executeAction({"action":"download", "videoid": "fOdNOtS8ZIs", "no_embed": "true"})

		import os
		assert(os.path.exists("./tmp/נלה מהיפה והחנון בסטריפ צ'אט בקליפ של חובבי ציון-[fOdNOtS8ZIs].mp4"))

	def test_plugin_should_download_with_subtitles_when_available(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue = Mock()
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = ["bUcszN8jRB8", ""]

		self.navigation.executeAction({"action":"download", "videoid": "byv-wpqDydI"}) #This is JUST annotations for now.

		import os
		assert(os.path.exists('./tmp/Morning Dew — a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].mp4'))
		assert(os.path.exists('./tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa'))
		
if __name__ == "__main__":
	nose.runmodule()
