# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
import storageserverdummy as StorageServer

class Teststorageserverdummy(BaseTestCase.BaseTestCase):
	def test_cacheFunction_should_call_funct(self):
		temp_funct = Mock()
		temp_funct.return_value = "mock_return"
		cache = StorageServer.StorageServer()
		result = cache.cacheFunction(temp_funct, "mock_args")
		temp_funct.assert_called_with('mock_args')
		assert(result == "mock_return")

	def test_set_data(self):
		cache = StorageServer.StorageServer()
		result = cache.sSet("name", "data")
		assert(result == "")

	def test_get(self):
		cache = StorageServer.StorageServer()
		result = cache.get("name")
		assert(result == "")

	def test_setMulti(self):
		cache = StorageServer.StorageServer()
		result = cache.setMulti("name", "data")
		assert(result == "")

	def test_getMulti(self):
		cache = StorageServer.StorageServer()
		result = cache.getMulti("name", "data")
		assert(result == "")

	def test_lock(self):
		cache = StorageServer.StorageServer()
		result = cache.lock("name")
		assert(result == False)

	def test_sqlSet(self):
		cache = StorageServer.StorageServer()
		result = cache.unlock("name")
		assert(result == False)
	
if __name__ == '__main__':
	nose.runmodule()
