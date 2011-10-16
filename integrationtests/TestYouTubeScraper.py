import BaseTestCase
import unittest2
import nose
from mock import Mock, patch


class YouTubeScraperTests(BaseTestCase.BaseTestCase):
	
	def test_scrapeTrailersListFormat_should_scraper_recent_trailers_correctly(self):
		self.navigation.listMenu({}) 
		assert(False)
		
if __name__ == "__main__":
	nose.runmodule()