# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

tasks = { '1' : { 'description': 'Some description', 'deadline': '2015-04-15', 'importance' : '10' }, 
			'2' : { 'description': 'Some description', 'deadline': '2015-04-15', 'importance' : '8' } }

@app.route('/todo/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/todo/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
	task = dict()
	for k,v in tasks.iteritems():
		if (k == str(task_id)):
			task = v
	if (len(task) == 0):
		abort(404)
	return jsonify(task)

@app.route('/todo/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'description' in request.json:
        abort(400)
    last = len(tasks) + 1
    tasks[last] = dict(description = request.json.get('description'),
    		deadline = request.json.get('deadline'), importance = request.json.get('importance'))
    return jsonify(tasks[last]), 201

@app.route('/todo/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = dict()
    for k,v in tasks.iteritems():
    	if (k == str(task_id)):
    		task = v
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'deadline' in request.json and type(request.json['deadline']) is not unicode:
        abort(400)
    if 'importance' in request.json and type(request.json['importance']) is not int:
        abort(400)
    tasks.pop(str(task_id))
    tasks[task_id] = dict(description = request.json.get('description'),
    		deadline = request.json.get('deadline'), importance = request.json.get('importance'))
    return jsonify(tasks[task_id])

@app.route('/todo/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = dict()
    for k,v in tasks.iteritems():
    	if (k == str(task_id)):
    		task = v
    if len(task) == 0:
        abort(404)
    tasks.pop(str(task_id))
    return jsonify({'System': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Bad request'}), 400)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'Error': 'Method not found'}), 405)

if __name__ == '__main__':
    app.run(debug=True)