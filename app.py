#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
	
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    print(jsonify({'request': request.json}))
    return jsonify({'request': request.json}), 201

if __name__ == '__main__':
    app.run(debug=True)
	
