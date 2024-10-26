from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///home_energy_tracker.db"  # Example: SQLite database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class EnergyUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    energy_consumption = db.Column(db.Float, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/energy_usage', methods=['POST'])
def energy_usage():
    if request.method == 'POST':
        data = request.json
        if 'timestamp' not in data:
            return jsonify({'error': 'Timestamp field is missing'}), 400
        new_energy_data = EnergyUsage(timestamp=data['timestamp'], energy_consumption=data.get('energy_consumption'))
        db.session.add(new_energy_data)
        db.session.commit()
        return jsonify({'message': 'Energy data added successfully'}), 201


@app.route('/energy_usage/<int:id>', methods=['DELETE', 'PUT'])
def manage_energy_usage(id):
    with app.app_context():
        energy_data = EnergyUsage.query.get_or_404(id)
        if request.method == 'DELETE':
            db.session.delete(energy_data)
            db.session.commit()
            return jsonify({'message': 'Energy data deleted successfully'}), 200
        elif request.method == 'PUT':
            data = request.json
            energy_data.timestamp = data.get('timestamp', energy_data.timestamp)
            energy_data.energy_consumption = data.get('energy_consumption', energy_data.energy_consumption)
            db.session.commit()
            return jsonify({'message': 'Energy data updated successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables based on defined models
    app.run(debug=True)
