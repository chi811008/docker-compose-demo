from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=1)

@app.route('/hello/<name>')
def hello(name):
    visitor = Visitor.query.filter_by(name=name).first()
    if visitor:
        visitor.visits += 1
    else:
        visitor = Visitor(name=name)
        db.session.add(visitor)
    db.session.commit()
    return f'Hello, {name}! You have visited {visitor.visits} times.'

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')