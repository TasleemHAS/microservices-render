#!/bin/bash

# Start User Service in background
python user_service/app.py &
USER_PID=$!

# Start Order Service in background  
python order_service/app.py &
ORDER_PID=$!

# Wait a moment for services to start
sleep 5

# Start Streamlit app (this will run in foreground)
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0

# If streamlit exits, kill the background services
kill $USER_PID
kill $ORDER_PID