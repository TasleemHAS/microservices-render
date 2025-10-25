from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)

# In-memory storage for orders
orders = [
    {"id": 1, "user_id": 1, "product": "Laptop", "quantity": 1, "amount": 999.99, "status": "completed", "created_at": "2024-01-15"},
    {"id": 2, "user_id": 2, "product": "Mouse", "quantity": 2, "amount": 49.98, "status": "pending", "created_at": "2024-01-16"}
]

@app.route('/')
def home():
    return jsonify({
        "service": "Order Service",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "running"
    })

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({
        "orders": orders,
        "count": len(orders)
    })

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    user_orders = [o for o in orders if o['user_id'] == user_id]
    return jsonify({
        "orders": user_orders,
        "count": len(user_orders)
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    required_fields = ['user_id', 'product', 'quantity', 'amount']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "user_id, product, quantity, and amount are required"}), 400
    
    new_order = {
        "id": len(orders) + 1,
        "user_id": data['user_id'],
        "product": data['product'],
        "quantity": data['quantity'],
        "amount": data['amount'],
        "status": data.get('status', 'pending'),
        "created_at": datetime.datetime.now().isoformat()
    }
    
    orders.append(new_order)
    return jsonify(new_order), 201

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    data = request.get_json()
    updatable_fields = ['product', 'quantity', 'amount', 'status']
    for field in updatable_fields:
        if field in data:
            order[field] = data[field]
    
    return jsonify(order)

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    global orders
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    orders = [o for o in orders if o['id'] != order_id]
    return jsonify({"message": "Order deleted successfully"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "order-service"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)