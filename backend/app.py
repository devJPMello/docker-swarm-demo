#!/usr/bin/env python3
import os
import socket
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Configurações
SERVICE_NAME = os.getenv('SERVICE_NAME', 'backend')
MESSAGE = os.getenv('MESSAGE', 'Hello from Docker Swarm Backend!')

@app.route('/api/info')
def api_info():
    """Endpoint que retorna informações da instância do backend"""
    hostname = socket.gethostname()
    container_id = os.getenv('HOSTNAME', 'unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'service': SERVICE_NAME,
        'hostname': hostname,
        'container_id': container_id,
        'timestamp': timestamp,
        'message': MESSAGE,
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_NAME,
        'hostname': socket.gethostname(),
        'container_id': os.getenv('HOSTNAME', 'unknown')
    })

@app.route('/')
def root():
    """Endpoint raiz com informações básicas"""
    return jsonify({
        'message': 'Backend API is running',
        'service': SERVICE_NAME,
        'hostname': socket.gethostname(),
        'endpoints': ['/api/info', '/health']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
