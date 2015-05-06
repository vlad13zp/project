# -*- coding: utf-8 -*-
from todo_new import Connect_to_redis
import unittest

dict_name = {'description' : 'asd',
			'deadline' : 'asd', 'importance' : 'asd'}

class Test_database(unittest.TestCase):

	def setUp(self):
		self.r = Connect_to_redis()

	@unittest.expectedFailure
	def test_connect(self):
		self.assertEqual(self.r.__init__(),'')

	def test_adding(self):
		self.assertEqual(self.r.add_to_redis(1,dict_name),True)

	def test_delete(self):
		self.assertEqual(self.r.delete_from_redis(1),True)

	def test_delete_unregistred(self):
		self.assertEqual(self.r.delete_from_redis(3),0)

	def test_info_unregistred(self):
		self.assertEqual(self.r.get_information(4),None)

if __name__ == "__main__":
	unittest.main()