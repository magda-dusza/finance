from flask import Flask, request, jsonify
# from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
# auth = HTTPBasicAuth()

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

# User Model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(100), nullable=False)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    bank = db.Column(db.String(100), nullable=False)

# Authenticate
# @auth.verify_password
# def verify_password(username, password):
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         return user

# Add User (for testing)
# @app.route('/add_user', methods=['POST'])
# def add_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         return jsonify({"message": "Missing arguments"}), 400
#     if User.query.filter_by(username=username).first() is not None:
#         return jsonify({"message": "User already exists"}), 400
#     user = User(username=username)
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'username': user.username}), 201

# Add Transaction
@app.route('/transactions', methods=['POST'])
# @auth.login_requiredŔ
def add_transaction():
    # user = auth.current_user()
    user = request.json.get('user')
    amount = request.json.get('amount')
    description = request.json.get('description')
    date = request.json.get('date')
    parsedDate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    bank = request.json.get('bank')
    if not all([amount, parsedDate, bank]):
        return jsonify({"message": "Missing data"}), 400
    transaction = Transaction(user=user, amount=amount, description=description, date=parsedDate, bank=bank)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 201

# Route to get all transactions
@app.route('/transactions', methods=['GET'])
# @auth.login_required
def get_transactions():
    # user = auth.current_user()
    transactions = Transaction.query.all()  # Fetch transactions 
    transactions_list = []
    for transaction in transactions:
        transactions_list.append({
            'id': transaction.id,
            'amount': transaction.amount,
            'description': transaction.description,
            'date': transaction.date.isoformat(),  # Convert datetime to string
            'bank': transaction.bank,
            'user': transaction.user
        })
    return jsonify(transactions_list)

# Health check
@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"message": "server is working"}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)