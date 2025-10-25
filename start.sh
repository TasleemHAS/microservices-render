#!/bin/bash

# Start User Service in background
echo "Starting User Service on port 5001..."
python user_service/app.py &

# Start Order Service in background
echo "Starting Order Service on port 5002..."
python order_service/app.py &

# Wait a moment for backend services to start
echo "Waiting for backend services to start..."
sleep 5

# Start Streamlit app (this runs in foreground)
echo "Starting Streamlit Dashboard on port 8501..."
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0