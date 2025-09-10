#!/usr/bin/env python3
import os
import requests
import socket
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Configurações do backend
BACKEND_SERVICE = os.getenv('BACKEND_SERVICE', 'backend')
BACKEND_PORT = os.getenv('BACKEND_PORT', '5000')

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Docker Swarm Demo - Frontend</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .instance-info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .backend-info { background: #f0f8e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .error { background: #ffe8e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .refresh-btn { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Docker Swarm Demo - Frontend</h1>
        
        <div class="instance-info">
            <h3>Frontend Instance Info:</h3>
            <p><strong>Hostname:</strong> {{ frontend_hostname }}</p>
            <p><strong>Container ID:</strong> {{ container_id }}</p>
            <p><strong>Timestamp:</strong> {{ timestamp }}</p>
        </div>
        
        {% if backend_data %}
        <div class="backend-info">
            <h3>Backend Response (Load Balanced):</h3>
            <p><strong>Backend Hostname:</strong> {{ backend_data.hostname }}</p>
            <p><strong>Backend Container ID:</strong> {{ backend_data.container_id }}</p>
            <p><strong>Backend Timestamp:</strong> {{ backend_data.timestamp }}</p>
            <p><strong>Message:</strong> {{ backend_data.message }}</p>
        </div>
        {% else %}
        <div class="error">
            <h3>Backend Error:</h3>
            <p>{{ error_message }}</p>
        </div>
        {% endif %}
        
        <div class="refresh-btn">
            <button onclick="location.reload()">🔄 Refresh Page</button>
        </div>
        
        <p><em>Refresh the page multiple times to see load balancing in action!</em></p>
    </div>
</body>
</html>
"""

def get_backend_data():
    """Chama o serviço backend e retorna os dados"""
    try:
        backend_url = f"http://{BACKEND_SERVICE}:{BACKEND_PORT}/api/info"
        response = requests.get(backend_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Erro ao conectar com backend: {e}")
        return None

@app.route('/')
def index():
    """Página principal que mostra informações do frontend e backend"""
    from datetime import datetime
    
    # Informações da instância frontend
    frontend_hostname = socket.gethostname()
    container_id = os.getenv('HOSTNAME', 'unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Chama o backend
    backend_data = get_backend_data()
    error_message = "Unable to connect to backend service"
    
    return render_template_string(
        HTML_TEMPLATE,
        frontend_hostname=frontend_hostname,
        container_id=container_id,
        timestamp=timestamp,
        backend_data=backend_data,
        error_message=error_message
    )

@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'frontend',
        'hostname': socket.gethostname(),
        'container_id': os.getenv('HOSTNAME', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
