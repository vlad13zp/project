# -*- coding: utf-8 -*-
import argparse

class check_data(argparse.Action):
	def __init__(self, option_strings, dest, nargs=None, **kwargs):
		super(check_data, self).__init__(option_strings, dest, nargs, **kwargs)
	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, values)
		
class Validate_int():
	def __init__(self,value):
		try:
			int(value)
			print 'Введенное значение корректно'
		except:
			print 'Введенное значение не корректно'
		
class Validate_float():
	def __init__(self,value):
		try:
			float(value)
			print 'Введенное значение корректно'
		except:
			print 'Введенное значение не корректно'

class Validate_email():
	def __init__(self,value):
		flag = False
		domain = ['yandex.ru','gmail.com','mail.ru','ukr.net']
		word = value.split('@')
		if (len(word) == 2):
			for i in domain:
				if (word[1] == i):
					flag = True
					break
			if (flag):
				print 'Ваш e-mail введен верно!'
			else :
				print 'Скорее всего Вы допустили ошибку'
		else :
			print 'Вы ввели не верный e-mail!'

class Validate_isoDate():
	def __init__(self,value):
		flag = False
		word = value.split('-')
		if (len(word) == 3):
			if ((len(word[0]) == 4) and (len(word[1]) == 2) and (len(word[2]) == 2)):
				try:
					case = int(word[1])
					if (case > 12 or case < 0):
						flag = False
					else :
						flag = True
				except:
					flag = False

				if (flag):

					try:
						case = int(word[2])
						if (case > 31 or case < 0):
							flag = False
						else :
							flag = True
					except:
						flag = False	

			else : 
				flaf = False
		else :
			flag = False

		if (flag):
			print 'Введенные данные корректны isoDate'
		else :
			print 'Вы допустили ошибку в формате даты'
				

parser = argparse.ArgumentParser()
parser.add_argument('--c', action = check_data , dest='Value', nargs='+' , type = Validate_int)
args = parser.parse_args()