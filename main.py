from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)

# In-memory storage for tasks and auto-increment id
tasks = []
next_id = 1

# Helper function to reset application data (useful for tests)
def reset_data():
    global tasks, next_id
    tasks.clear()
    next_id = 1

@app.route('/')
def index():
    """
    Render the main page with the tasks.
    """
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    API endpoint to retrieve all tasks.
    """
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def add_task():
    """
    API endpoint to add a new task.
    Requires a JSON payload with at least a 'title' key.
    """
    global next_id
    if not request.json or 'title' not in request.json:
        abort(400)  # Bad Request if no title is provided
    task = {
        'id': next_id,
        'title': request.json['title'],
        'done': False
    }
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    API endpoint to update an existing task.
    Allows updating the 'title' and/or 'done' status.
    """
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404)  # Task not found
    data = request.json
    if 'title' in data:
        task['title'] = data['title']
    if 'done' in data:
        task['done'] = data['done']
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    API endpoint to delete an existing task.
    """
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404)
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'result': True}), 200

if __name__ == '__main__':
    # Pre-populate some tasks for a more engaging demo when running locally.
    if not tasks:
        tasks.extend([
            {'id': 1, 'title': 'Buy groceries', 'done': False},
            {'id': 2, 'title': 'Call the plumber', 'done': False},
            {'id': 3, 'title': 'Finish the Python project', 'done': False}
        ])
        next_id = 4

    # Run the Flask development server with debug mode enabled.
    app.run(host="0.0.0.0", port=5000, debug=True)
