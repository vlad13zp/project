# -*- coding: utf-8 -*-
import todo_new
from bottle import route, run, request

my_task = todo_new.Todo()

@route('/todo/tasks')
def tasks_list():
    return my_task.printMe()

@route('/todo/tasks/<task_id:int>')
def get_task(task_id):
	local = my_task.printMe()
	for k,v in local.iteritems():
		if (int(k) == task_id):
			return v
	return {'404' : 'Not Found'}

@route('/todo/tasks/<task_id:int>', method='PUT')
def edit_task(task_id):
	des = request.forms.get('description')
	dead = request.forms.get('deadline')
	impor = request.forms.get('importance')
	if (des != '' and dead != '' and 
		impor != ''):
		if (my_task.edit(task_id,des,dead,impor)):
			return {'200' : 'OK'}
		else :
			return {'500' : 'Server error'}

@route('/todo/tasks', method='POST')
def create_task():
	des = request.forms.get('description')
	dead = request.forms.get('deadline')
	impor = request.forms.get('importance')
	if (des != '' and dead != '' and 
		impor != ''):
		if (my_task.add(des,dead,impor)):
			return {'201' : 'Create'}
		else :
			return {'500' : 'Server error'}

@route('/todo/tasks/<task_id:int>', method='DELETE')
def delete_task(task_id):
	if (my_task.delete(task_id)):
		return {'200' : 'OK'}
	else :
		return {'404' : 'Not Found'}


run(host='localhost', port=1234, debug=True)