import BaseTestCase
import nose, sys
from mock import Mock

class TestYouTubePlayer(BaseTestCase.BaseTestCase):	
	def ttest_plugin_should_download_standard_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"download", "videoid": "54VJWHL2K3I"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)

	def ttest_plugin_should_download_agerestricted_over_18_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")

		self.navigation.executeAction({"action":"download", "videoid": "fOdNOtS8ZIs", "no_embed": "true"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)

	
	def ttest_plugin_should_download_with_subtitles_when_available(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		import os
                sys.modules[ "__main__" ].xbmcvfs.exists.side_effect = os.path.exists
		self.navigation.executeAction({"action":"download", "videoid": "bUcszN8jRB8"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		args2 = sys.modules[ "__main__" ].xbmc.Player().setSubtitles.call_args_list
		print "Args: " + repr(args)
		print "Args2: " + repr(args2[0][0][0])
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)
		print repr(args2[0][0][0] == './tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa')

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)
		assert(args2[0][0][0] == './tmp/Morning Dew  a bad lip reading of Bruno Mars, feat. Lady Gaga and Jay-Z-[bUcszN8jRB8].ssa')

	
	def ttest_plugin_should_download_with_subtitles_and_annotation_when_available(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue = Mock()
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = ["byv-wpqDydI", ""]

		#import os
                #sys.modules[ "__main__" ].xbmcvfs.exists.side_effect = os.path.exists
				
		self.navigation.executeAction({"action":"download", "videoid": "byv-wpqDydI"}) #This is JUST annotations for now.
		
		assert("" == './tmp/Super Bass - Nicki Minaj (Cover by @KarminMusic)-[byv-wpqDydI].ssa')
		
if __name__ == "__main__":
	nose.runmodule()
