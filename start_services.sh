#!/bin/bash
# Start User Service
python user_service.py &
# Start Order Service  
python order_service.py &
# Start Streamlit
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
