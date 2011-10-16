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

	def test_sqlSet(self):
		cache = StorageServer.StorageServer()
		result = cache.sqlSet("name", "data")
		assert(result == "")

	def test_sqlGet(self):
		cache = StorageServer.StorageServer()
		result = cache.sqlGet("name")
		assert(result == "")

	def test_sqlSetMulti(self):
		cache = StorageServer.StorageServer()
		result = cache.sqlSetMulti("name", "data")
		assert(result == "")

	def test_sqlGetMulti(self):
		cache = StorageServer.StorageServer()
		result = cache.sqlGetMulti("name", "data")
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
