from flask import Flask, request, jsonify
from models import db, Reminder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ✅ Create tables once at startup
with app.app_context():
    db.create_all()

@app.route('/api/reminder', methods=['POST'])
def create_reminder():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    message = data.get('message')
    remind_via = data.get('remind_via')

    if remind_via not in ['SMS', 'Email']:
        return jsonify({'error': 'Invalid remind_via. Use SMS or Email only.'}), 400

    reminder = Reminder(date=date, time=time, message=message, remind_via=remind_via)
    db.session.add(reminder)
    db.session.commit()

    return jsonify({'message': 'Reminder saved successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
