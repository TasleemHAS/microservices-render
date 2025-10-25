from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": "2024-01-02"}
]

@app.route('/health')
def health():
    return jsonify({"service": "user-service", "status": "healthy"})

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"users": users})

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data.get('name'),
        "email": data.get('email'),
        "created_at": datetime.datetime.now().isoformat()
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
