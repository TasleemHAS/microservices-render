import requests
import sys

def health_check():
    services = {
        "User Service": "http://localhost:5001/health",
        "Order Service": "http://localhost:5002/health", 
        "Streamlit App": "http://localhost:8501/"
    }
    
    all_healthy = True
    
    for service_name, url in services.items():
        try:
            if service_name == "Streamlit App":
                response = requests.get(url, timeout=5)
                status = "✅ HEALTHY" if response.status_code == 200 else "❌ UNHEALTHY"
            else:
                response = requests.get(url, timeout=5)
                data = response.json()
                status = "✅ HEALTHY" if data.get('status') == 'healthy' else "❌ UNHEALTHY"
            
            print(f"{service_name}: {status}")
            
        except Exception as e:
            print(f"{service_name}: ❌ ERROR - {e}")
            all_healthy = False
    
    return all_healthy

if __name__ == "__main__":
    print("🔍 Running Health Checks...")
    print("-" * 40)
    
    if health_check():
        print("-" * 40)
        print("🎉 ALL SERVICES ARE HEALTHY!")
        sys.exit(0)
    else:
        print("-" * 40)
        print("💥 SOME SERVICES ARE DOWN!")
        sys.exit(1)