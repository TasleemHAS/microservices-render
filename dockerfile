FROM python:3.9-slim

WORKDIR /app

# Copy all your service files
COPY . .

# Install dependencies
RUN pip install streamlit requests flask

# Expose ports for all services
EXPOSE 8501 5001 5002

# Start all services (you'll need a start script)
CMD ["./start_services.sh"]
