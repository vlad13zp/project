# -*- coding: utf-8 -*-
from todo_new import Json_reservation
import unittest

dict_name = {'description' : 'asd',
			'deadline' : 'asd', 'importance' : 'asd'}

local_string = '{"importance": "asd", "deadline": "asd", "description": "asd"}'

class Test_json(unittest.TestCase):

	def setUp(self):
		self.js = Json_reservation()

	def test_dumping(self):
		self.assertEqual(self.js.add_to_dump(dict_name),local_string)

	def test_loading(self):
		self.assertEqual(self.js.load_me(local_string),dict_name)

if __name__ == "__main__":
	unittest.main()