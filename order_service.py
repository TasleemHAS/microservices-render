from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

orders = [
    {"id": 1, "user_id": 1, "product": "Laptop", "quantity": 1, "amount": 999.99, "status": "completed", "created_at": "2024-01-01"},
    {"id": 2, "user_id": 2, "product": "Mouse", "quantity": 2, "amount": 49.99, "status": "pending", "created_at": "2024-01-02"}
]

@app.route('/health')
def health():
    return jsonify({"service": "order-service", "status": "healthy"})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders})

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = {
        "id": len(orders) + 1,
        "user_id": data.get('user_id'),
        "product": data.get('product'),
        "quantity": data.get('quantity'),
        "amount": data.get('amount'),
        "status": data.get('status', 'pending'),
        "created_at": datetime.datetime.now().isoformat()
    }
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
