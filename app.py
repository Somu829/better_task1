from flask import Flask, request, jsonify, abort
return jsonify(t.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
t = Task.query.get_or_404(task_id)
data = request.get_json() or {}
title = data.get('title')
if title:
t.title = title
if 'description' in data:
t.description = data.get('description')
db.session.commit()
return jsonify(t.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
t = Task.query.get_or_404(task_id)
db.session.delete(t)
db.session.commit()
return jsonify({'message': 'deleted'}), 200


# Routes: Comments for a given task
@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
task = Task.query.get_or_404(task_id)
data = request.get_json() or {}
content = data.get('content')
if not content:
return jsonify({'error': 'content is required'}), 400
c = Comment(task_id=task.id, content=content)
db.session.add(c)
db.session.commit()
return jsonify(c.to_dict()), 201


@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def list_comments(task_id):
Task.query.get_or_404(task_id)
comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.asc()).all()
return jsonify([c.to_dict() for c in comments]), 200


@app.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
c = Comment.query.get_or_404(comment_id)
data = request.get_json() or {}
content = data.get('content')
if content is None:
return jsonify({'error': 'content is required'}), 400
c.content = content
db.session.commit()
return jsonify(c.to_dict()), 200


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
c = Comment.query.get_or_404(comment_id)
db.session.delete(c)
db.session.commit()
return jsonify({'message': 'deleted'}), 200


if __name__ == '__main__':
with app.app_context():
db.create_all()
app.run(debug=True)