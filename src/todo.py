# -*- coding: utf-8 -*-
# TODO List
import redis
import json
import os


class member(object):

	def __init__(self, id, description, deadline, importance):
		self.id = id
		self.task_args = dict(description=description,
								deadline=deadline, importance=importance)

class Todo(member):

	def __init__(self, *args):
		self.r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
		self.dict_name = dict()
		self.args = args
		for arg in self.args:
			self.dict_name[arg.id] = arg.task_args

	def delete(self,id):
		key = False
		for i in self.r.scan_iter():
			if (i == id):
				self.r.delete(id)
				key = True
				break
		if (key):
			print 'Система : запись успешно удалена!'
			raw_input()
		else :
			print 'Система : записи с таким идентификатором не существует!'
			raw_input()

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
			raw_input()
		else : 
			print 'Система : идентификатор записи не уникален. Будьте внимательны!'
			raw_input()

	def edit(self,id):
		key = False
		for i in self.r.scan_iter():
			if (i == id):
				key = True
				break
		if (key):
			self.dict_name[id] = json.loads(self.r.get(id))
			for i,k in self.dict_name[id].iteritems():
				des = raw_input(i + ' : ')
				self.dict_name[id][i] = des
			self.r.delete(id)
			self.r.set(id, json.dumps(self.dict_name[id]))
			self.dict_name.pop(id)
			print 'Система : запись успешно отредактирована!'
			raw_input()
		else :
			print 'Система : записи с таким идентификатором не существует!'
			raw_input()

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
		if (des == '1'):
			a.add()
			os.system('clear')
		elif (des == '2'):
			my_id = raw_input('Введите номер задачи : ')
			a.delete(my_id)
			os.system('clear')
		elif (des == '3'):
			my_id = raw_input('Введите номер задачи : ')
			a.edit(my_id)
			os.system('clear')
		elif (des == '4'):
			print a.printMe()
			raw_input()
			os.system('clear')
		elif (des == '5'):
			key = False
		else : 
			print 'Система : введено ошибочное значение!'
			raw_input()
			os.system('clear')

main()




