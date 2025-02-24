import pytest
from main import app, reset_data

# This fixture resets the application data before every test
@pytest.fixture(autouse=True)
def run_before_tests():
    reset_data()

def test_get_empty_tasks():
    """
    Test that the task list is empty initially.
    """
    client = app.test_client()
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_add_task():
    """
    Test that adding a task works correctly.
    """
    client = app.test_client()
    response = client.post('/tasks', json={'title': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['title'] == 'Test Task'
    assert data['done'] is False

def test_update_task():
    """
    Test updating an existing task.
    """
    client = app.test_client()
    # First, add a task
    post_response = client.post('/tasks', json={'title': 'Initial Title'})
    task = post_response.get_json()
    task_id = task['id']
    # Now, update the task
    response = client.put(f'/tasks/{task_id}', json={'title': 'Updated Title', 'done': True})
    assert response.status_code == 200
    updated_task = response.get_json()
    assert updated_task['title'] == 'Updated Title'
    assert updated_task['done'] is True

def test_delete_task():
    """
    Test deleting a task.
    """
    client = app.test_client()
    # Add a task to delete
    post_response = client.post('/tasks', json={'title': 'Task to Delete'})
    task = post_response.get_json()
    task_id = task['id']
    # Delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    # Verify that the task list no longer contains the deleted task
    get_response = client.get('/tasks')
    all_tasks = get_response.get_json()
    assert all(task['id'] != task_id for task in all_tasks)

def test_error_on_updating_nonexistent_task():
    """
    Test that updating a task that does not exist returns a 404 error.
    """
    client = app.test_client()
    response = client.put('/tasks/999', json={'title': 'Nonexistent'})
    assert response.status_code == 404
