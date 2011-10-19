import BaseTestCase
import unittest2
import nose, sys, os

class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	
	def test_playVideo_should_play_videos(self):
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

	def test_playVideo_should_handle_over_18_videos(self):
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

	def test_playVideo_should_handle_not_embeddable_over_18(self): # Currently this is just not embeddable
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


	def test_playVideo_should_handle_rtmpe_vidoes(self):
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

	def test_playVideo_should_handle_live_vidoes(self):
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
	
if __name__ == "__main__":
	nose.runmodule()
