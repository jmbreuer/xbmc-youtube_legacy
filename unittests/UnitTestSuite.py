import unittest
import YouTubePlayerTests

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(YouTubePlayerTests.YouTubePlayerTests)
	unittest.TextTestRunner(verbosity=2).run(suite)