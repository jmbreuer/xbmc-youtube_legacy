import BaseTestCase
import nose, sys

class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_play_standard_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_video", "videoid": "54VJWHL2K3I"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)

	def test_plugin_should_play_agerestricted_over_18_videos(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")

		self.navigation.executeAction({"action":"play_video", "videoid": "fOdNOtS8ZIs", "no_embed": "true"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)

	def test_plugin_should_play_non_embeddable_over_18_videos(self): # Currently this is just not embeddable
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_video", "videoid": "3PjTEO948Lo"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)


	def test_plugin_should_play_rtmpe_vidoes(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")

		self.navigation.executeAction({"action":"play_video", "videoid": "8wxOVn99FTE"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		print "Args: " + repr(args)
		print repr(args[0][1].has_key("listitem"))
		print repr(args[0][1]["handle"] == -1)
		print repr(args[0][1]["succeeded"] == True)

		assert(args[0][1].has_key("listitem"))
		assert(args[0][1]["handle"] == -1)
		assert(args[0][1]["succeeded"] == True)

	def test_plugin_should_play_live_vidoes(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
				
		self.navigation.executeAction({"action":"play_video", "videoid": "JpYHuK45We0"})

		args = sys.modules[ "__main__" ].xbmcplugin.setResolvedUrl.call_args_list
		if sys.modules[ "__main__"].xbmc.executebuiltin.call_count == 0:
			print "Args: " + repr(args)
			print repr(args[0][1].has_key("listitem"))
			print repr(args[0][1]["handle"] == -1)
			print repr(args[0][1]["succeeded"] == True)
	
			assert(args[0][1].has_key("listitem"))
			assert(args[0][1]["handle"] == -1)
			assert(args[0][1]["succeeded"] == True)
	
	def test_plugin_should_play_videos_with_subtitles_when_available(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
				
		self.navigation.executeAction({"action":"play_video", "videoid": "JpYHuK45We0"})
		
		assert(False)

	
	def test_plugin_should_play_videos_with_subtitles_and_annotation_when_available(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
				
		self.navigation.executeAction({"action":"play_video", "videoid": "JpYHuK45We0"})
		
		assert(False)
		
if __name__ == "__main__":
	nose.runmodule()
