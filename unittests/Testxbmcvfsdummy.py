# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
import xbmcvfsdummy as xbmcvfs

class Testxbmcvfsdummy(BaseTestCase.BaseTestCase):
	def test_exists(self):
		patcher = patch("os.path")
		patcher.start()

		import os
		os.path.exists.return_value = "my_result"

		result = xbmcvfs.exists("someFile")
		args = os.path.exists.call_args_list

		patcher.stop()

		print repr(args)
		assert(args[0][0][0] == "someFile")
		assert(result == "my_result")

	def test_rename(self):
		patcher = patch("os.rename")
		patcher.start()

		import os
		os.rename.return_value = "my_result"

		result = xbmcvfs.rename("someFile", "someOtherFile")

		args = os.rename.call_args_list
		patcher.stop()

		print repr(args)	
		assert(args[0][0][0] == "someFile")
		assert(args[0][0][1] == "someOtherFile")
		assert(result == "my_result")

	def test_delete_file_is_dir(self):
		patcher = patch("os.path")
		patcher.start()

		import os
		os.path.isfile.return_value = False

		result = xbmcvfs.delete("someFile")
		args = os.path.isfile.call_args_list
		patcher.stop()

		print repr(args)
		assert(args[0][0][0] == "someFile")
		assert(result == False)

	def test_delete_file(self):
		patcher = patch("os.path")
		patcher.start()

		patcher2 = patch("os.unlink")
		patcher2.start()

		import os
		os.path.isfile.return_value = True
		os.unlink.return_value = "my_result"

		result = xbmcvfs.delete("someFile")
		args = os.path.isfile.call_args_list
		args2 = os.unlink.call_args_list
		patcher.stop()
		patcher2.stop()

		print repr(result)
		assert(result == "my_result")
	
if __name__ == '__main__':
	nose.runmodule()
