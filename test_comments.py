import json




def test_add_comment(client):
# assume task id 1 exists from fixture
rv = client.post('/tasks/1/comments', json={'content': 'hello comment'})
assert rv.status_code == 201
data = rv.get_json()
assert data['task_id'] == 1
assert data['content'] == 'hello comment'




def test_add_comment_missing_content(client):
rv = client.post('/tasks/1/comments', json={})
assert rv.status_code == 400




def test_list_comments(client):
client.post('/tasks/1/comments', json={'content': 'c1'})
client.post('/tasks/1/comments', json={'content': 'c2'})
rv = client.get('/tasks/1/comments')
assert rv.status_code == 200
data = rv.get_json()
assert len(data) == 2




def test_edit_comment(client):
rv = client.post('/tasks/1/comments', json={'content': 'original'})
cid = rv.get_json()['id']
rv2 = client.put(f'/comments/{cid}', json={'content': 'edited'})
assert rv2.status_code == 200
assert rv2.get_json()['content'] == 'edited'




def test_delete_comment(client):
rv = client.post('/tasks/1/comments', json={'content': 'to delete'})
cid = rv.get_json()['id']
rv2 = client.delete(f'/comments/{cid}')
assert rv2.status_code == 200
rv3 = client.get('/tasks/1/comments')
assert all(c['id'] != cid for c in rv3.get_json())