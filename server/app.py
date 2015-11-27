from flask import Flask, render_template, jsonify, request
from server.models import db, Entry, EntrySchema, EntryFactory
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'flaskstream.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

db.init_app(app)

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True, only=('posted', 'text'))

@app.route('/')
def index():
    # create_entry()
    return render_template('index.html', text='Hello world')


@app.route('/entries', methods=['GET'])
def entries():
    entries = Entry.query.order_by(Entry.posted.desc()).all()
    result = entries_schema.dump(entries)
    return jsonify({'entries': result.data})

@app.route('/entries/', methods=['POST'])
def new_entry():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No imput data provided'}), 400
    data, errors = entry_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    text = data.get('text')
    entry = Entry(text=text)
    db.session.add(entry)
    db.session.commit()
    result = entry_schema.dump(Entry.query.get(entry.id))
    return jsonify({'message': 'Created new entry.',
                    'entry': result.data})

def create_entry():
    entry = EntryFactory(posted=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()
    print str(entry)
