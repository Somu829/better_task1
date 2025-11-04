import pytest
from app import app, db, Task


@pytest.fixture
def client(tmp_path):
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
with app.test_client() as client:
with app.app_context():
db.create_all()
# create one task to associate comments with
t = Task(title='Test Task', description='task for tests')
db.session.add(t)
db.session.commit()
yield client