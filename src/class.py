# -*- coding: utf-8 -*-
import turtle
import random

class Shape(object):
	border_color = 'black'
	fill_color = None
	start_point = (0,0)
	my_t = None

	def __init__(self,start_point,fill_color, my_t):
		self.start_point = start_point
		self.fill_color = fill_color
		self.my_t = my_t

	def draw(self):
		self.my_t.up()
		self.my_t.goto(self.start_point)
		self.my_t.down()
		self.my_t.color(self.fill_color,self.fill_color)
		self.my_t.begin_fill()
		self._draw()
		self.my_t.end_fill()


class Triangle(Shape):
	def __init__(self, start_point, fill_color, my_t, size = 100):
		self.size = size
		super(Triangle,self).__init__(start_point,fill_color,my_t)

	def _draw(self):
		for i in range(3):
			self.my_t.fd(self.size) 
			self.my_t.left(120)

class Square(Triangle):
	def _draw(self):
		for i in range(4): 
			self.my_t.fd(self.size)
			self.my_t.left(90)

class Circle(Triangle):
	def _draw(self):
		for i in range(72):
			self.my_t.fd(self.size)
			self.my_t.left(5)

class Composite(Shape):
	def __init__(self, *arg):
		self.arg = arg

	#Сложение фигур
	def __add__(self, arg):
		self.arg += arg

	#Вычитание фигур
	def __sub__(self, arg):
		local = []
		for i in self.arg:
			if (i != arg):
				local.append(i)
		self.arg = local

	#Умножение фигур
	def __mul__(self,arg):
		self.arg *= arg

	#Деление фигур
	def __floordiv__(self,arg):
		counter = len(self.arg) / arg
		a = 0
		local = []
		for i in self.arg:
			if (a < counter):
				local.append(i)
			a = a + 1
		self.arg = local

	#Обращение по индексу
	def __getitem__(self,arg):
		local = []
		a = 0
		for i in self.arg:
			if (a == arg):
				local.append(i)
			a = a + 1
		self.arg = local

	def draw(self):
		for i in self.arg:
			i.draw()

myTurtle = turtle.Turtle()

colors = ['yellow','violet','orange','blue','red','green','black'] 

tr = Triangle((random.randint(0,200),random.randint(0,200)),colors[random.randint(0,len(colors)-1)], myTurtle, size = 100)
tr2 = Triangle((random.randint(0,200),random.randint(0,200)),colors[random.randint(0,len(colors)-1)], myTurtle, size = 100)
sq = Square((random.randint(0,200),random.randint(0,200)),colors[random.randint(0,len(colors)-1)], myTurtle, size = 100)
ci = Circle((random.randint(0,200),random.randint(0,200)),colors[random.randint(0,len(colors)-1)], myTurtle, size = 5)

com = Composite(tr,sq,ci)

""" Сложение фигур (результат - 4 фигуры)
com + tr2"""

""" Вычитание фигур (результат - 2 фигуры)
com - tr"""

""" Умножение фигур (результат - 6 фигур,но на стандартных позициях :(
com * 2"""

""" Деление фигур (результат - 1 фигура)
com // 2"""

""" Обращение по индексу (результат - 1 фигура)
com[0]"""

com.draw()


raw_input()