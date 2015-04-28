# -*- coding: utf-8 -*-
# TODO List
import redis
import json
import os

class Todo(object):

	def __init__(self, *args):
		self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.dict_name = dict()
		self.args = args
		for arg in self.args:
			self.dict_name[arg.id] = arg.task_args

	def delete(self):
		key = False
		my_id = raw_input('Введите идентификатор задачи : ')
		for i in self.r.scan_iter():
			if (i == my_id):
				self.r.delete(my_id)
				key = True
				break
		if (key):
			print 'Система : запись успешно удалена!'
		else :
			print 'Система : записи с таким идентификатором не существует!'
		return True

	def add(self):		
		val = False		
		my_id = raw_input('Введите идентификатор задачи : ')
		for i in self.r.scan_iter():
			if (i == my_id):
				val = True
				break
		if (val == False):
			my_des = raw_input('Введите описание задачи : ')
			my_ded = raw_input('Введите дату дедлайна (2015-04-15) : ')
			my_imp = raw_input('Введите важность (0 - 10) : ')
			self.dict_name[my_id] = dict(description=my_des,
							deadline=my_ded, importance=my_imp)
			self.r.set(my_id, json.dumps(self.dict_name[my_id]))
			self.dict_name.pop(my_id)
			print 'Система : запись успешно добавлена!'
		else : 
			print 'Система : идентификатор записи не уникален. Будьте внимательны!'
		return True

	def edit(self):
		key = False
		my_id = raw_input('Введите идентификатор задачи : ')
		for i in self.r.scan_iter():
			if (i == my_id):
				key = True
				break
		if (key):
			self.dict_name[my_id] = json.loads(self.r.get(my_id))
			for i,k in self.dict_name[my_id].iteritems():
				des = raw_input(i + ' : ')
				self.dict_name[my_id][i] = des
			self.r.delete(my_id)
			self.r.set(my_id, json.dumps(self.dict_name[my_id]))
			self.dict_name.pop(my_id)
			print 'Система : запись успешно отредактирована!'
		else :
			print 'Система : записи с таким идентификатором не существует!'
		return True

	def printMe(self):
		c = 1
		local = dict()
		for i in self.r.scan_iter():
			print '=========================='
			print 'Задача №' + str(c)
			print 'Идентификатор : ' + i
			local = json.loads(self.r.get(i))
			for v,d in local.iteritems():
				print '## ' + v + ' : ' + d
			c = c + 1
		return True

	def exit(self):
		key = False
		print 'До свидания!'
		return key

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

main()




