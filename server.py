from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Modelo de Logs
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    service_name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

# Asegurarse de que se ejecute dentro del contexto de la aplicación
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error al crear tabla {e}")

valid_tokens = [
    'Bearer abcd1234efgh5678ijkl',
    'Bearer mnop9012qrst3456uvwx',
    'Bearer yzab6789cdef0123ghij'
]

# Endpoint para recibir logs
@app.route('/logs', methods=['POST'])
def receive_log():
    auth_header = request.headers.get('Authorization')
    if auth_header not in valid_tokens:
        return jsonify({'error': 'Unauthorized'}), 401
    
    log_data = request.get_json()
    required_keys = {'timestamp', 'service_name', 'level', 'message'}
    if not required_keys.issubset(log_data):
        return jsonify({'error': 'Invalid log data'}), 400

    try:
        new_log = Log(
            timestamp=datetime.datetime.strptime(log_data['timestamp'], '%Y-%m-%dT%H:%M:%S'),
            service_name=log_data['service_name'],
            level=log_data['level'],
            message=log_data['message']
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Log received'}), 201

# Endpoint para obtener logs
@app.route('/logs', methods=['GET'])
def get_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Log.query

    if start_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
        query = query.filter(Log.timestamp >= start_date)
    if end_date:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')
        query = query.filter(Log.timestamp <= end_date)
    
    logs = query.all()
    return jsonify([{
        'timestamp': log.timestamp.isoformat(),
        'service_name': log.service_name,
        'level': log.level,
        'message': log.message,
        'received_at': log.received_at.isoformat()
    } for log in logs])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
