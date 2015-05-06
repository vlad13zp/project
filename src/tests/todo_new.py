# -*- coding: utf-8 -*-
# TODO List
import redis
import json
import os
"""
The program is creating a task list (TODO list)

Class for working with database named redis

The class contains functions to add, delete data from database
"""
class Connect_to_redis(object):
	"""
	The connection to the database
	"""
	def __init__(self, *args):
		self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.js = Json_reservation()
	"""
	Adding data to the database

	:param my_id : record id
	:param my_dict : dictionary, that we need to add to the database
	"""
	def add_to_redis(self, my_id, my_dict):
		local = self.r.set(my_id, self.js.add_to_dump(my_dict))
		return local
	"""
	Deleting data from the database

	:param my_id : record id
	"""
	def delete_from_redis(self, my_id):
		local = self.r.delete(my_id)
		return local
	"""
	Returns all records from the database
	"""
	def make_dict(self):
		return self.r.scan_iter()
	"""
	Returns the record by KeyError

	:param key : key for the record
	"""
	def get_information(self, key):
		return self.r.get(key)
"""
Class to serialize and deserialize data

It includes options for serializing and deserializing data
"""
class Json_reservation(object):
	"""
	The function data serialization

	:param my_dict : dictionary for serialization
	"""
	def add_to_dump(self, my_dict):
		return json.dumps(my_dict)
	"""
	The function data deserialization

	:param my_str : string for make dictionary
	"""
	def load_me(self, my_str):
		return json.loads(my_str)
"""
The main class work with the console and user interaction

The class has the ability to add records, delete, edit and display
"""
class Todo(object):
	"""
	Announcement of other classes of objects and their interaction

	:param *args : arguments for detalization of our record
	"""
	def __init__(self, *args):	
		self.r = Connect_to_redis()	
		self.js = Json_reservation()
		self.dict_name = dict()
		self.args = args
		for arg in self.args:
			self.dict_name[arg.id] = arg.task_args
	"""
	The delete record function
	"""
	def delete(self):
		key = False
		list_box = self.r.make_dict()
		my_id = raw_input('Введите идентификатор задачи : ')
		for i in list_box:
			if (i == my_id):
				self.r.delete_from_redis(my_id)
				key = True
				break
		if (key):
			print 'Система : запись успешно удалена!'
		else :
			print 'Система : записи с таким идентификатором не существует!'
		return True
	"""
	The function of adding a new entry
	"""
	def add(self):		
		val = False		
		my_id = raw_input('Введите идентификатор задачи : ')
		local_list = self.r.make_dict()
		print local_list
		for i in local_list:
			if (i == my_id):
				val = True
				break
		if (val == False):
			my_des = raw_input('Введите описание задачи : ')
			my_ded = raw_input('Введите дату дедлайна (2015-04-15) : ')
			my_imp = raw_input('Введите важность (0 - 10) : ')
			self.dict_name[my_id] = dict(description=my_des,
							deadline=my_ded, importance=my_imp)
			self.r.add_to_redis(my_id,self.dict_name[my_id])
			self.dict_name.pop(my_id)
			print 'Система : запись успешно добавлена!'
		else : 
			print 'Система : идентификатор записи не уникален. Будьте внимательны!'
		return True
	"""
	The function edit an existing record
	"""
	def edit(self):
		key = False
		my_id = raw_input('Введите идентификатор задачи : ')
		local_list = self.r.make_dict()
		for i in local_list:
			if (i == my_id):
				key = True
				break
		if (key):
			self.dict_name[my_id] = json.loads(self.r.get_information(i))
			for i,k in self.dict_name[my_id].iteritems():
				des = raw_input(i + ' : ')
				self.dict_name[my_id][i] = des
			self.r.delete_from_redis(my_id)
			self.r.add_to_redis(my_id, self.dict_name[my_id])
			self.dict_name.pop(my_id)
			print 'Система : запись успешно отредактирована!'
		else :
			print 'Система : записи с таким идентификатором не существует!'
		return True
	"""
	The console output of all records from the database
	"""
	def printMe(self):
		c = 1
		local = dict()
		list_box = self.r.make_dict()
		for i in list_box:
			print '=========================='
			print 'Задача №' + str(c)
			print 'Идентификатор : ' + i
			local = self.js.load_me(self.r.get_information(i))
			for v,d in local.iteritems():
				print '## ' + v + ' : ' + d
			c = c + 1
		return True
	"""
	Exit from the programm
	"""
	def exit(self):
		key = False
		print 'До свидания!'
		return key
"""
The function menu display and user interaction
"""
def main():
	a = Todo()
	key = True
	while (key):
		print '\t\t\t Меню'
		print '[1] - Добавить новую задачу'
		print '[2] - Удалить задачу'
		print '[3] - Редактировать задачу'
		print '[4] - Вывести список задач'
		print '[5] - Выход'
		des = raw_input('Введите желаемую команду : ')
		functions = {'1': a.add, 
             '2': a.delete, 
             '3': a.edit,
             '4': a.printMe,
             '5': a.exit}

		func = functions[des] 
		key = func()
		raw_input()
		os.system('clear')




