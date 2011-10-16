class MockYouTubeDepends:
	common = ""
	def mock(self):
		import sys, string
		from mock import Mock
		sys.path.append("../plugin/")
		
		#Setup default test various values 
		sys.modules[ "__main__" ].plugin = "YouTube - Integrationtest"
		sys.modules[ "__main__" ].dbg = True
		sys.modules[ "__main__" ].dbglevel = 10
		sys.modules[ "__main__" ].login = "" 
		
		sys.modules[ "__main__" ].cache = Mock()		
	
	def mockXBMC(self):
		import sys
		from mock import Mock
		sys.path.append("../xbmc-mocks/")
		import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
		
		#Setup basic xbmc dependencies
		sys.modules[ "__main__" ].xbmc = Mock(spec=xbmc)
		sys.modules[ "__main__" ].xbmc.translatePath = Mock()
		sys.modules[ "__main__" ].xbmc.translatePath.return_value = "testing"
		sys.modules[ "__main__" ].xbmc.log.side_effect = self.log
		sys.modules[ "__main__" ].xbmc.getSkinDir = Mock()
		sys.modules[ "__main__" ].xbmc.getSkinDir.return_value = "testSkinPath"
		sys.modules[ "__main__" ].xbmc.getInfoLabel.return_value = "some_info_label"
		sys.modules[ "__main__" ].xbmcaddon = Mock(spec=xbmcaddon)
		sys.modules[ "__main__" ].xbmcgui = Mock(spec=xbmcgui)
		sys.modules[ "__main__" ].xbmcgui.WindowXMLDialog.return_value = "testWindowXML"
		
		sys.modules[ "__main__" ].xbmcplugin = Mock(spec=xbmcplugin)
		sys.modules[ "__main__" ].xbmcvfs = Mock(spec=xbmcvfs)
		sys.modules[ "__main__" ].settings = Mock(spec= xbmcaddon.Addon()) # TODO: We need a better way to specify th
		sys.modules[ "__main__" ].settings.getAddonInfo.return_value = "somepath"
		sys.modules[ "__main__" ].language = Mock()  # we need a proper mock for this
	
	def log(self, description, level = 0):
		import inspect
		print "[%s] %s : '%s'" % ("YouTube", inspect.stack()[1][3], description)
