#!/bin/bash

# Script para testar o balanceamento de carga
# Execute este script após fazer o deploy da aplicação

echo "🐳 Testando Balanceamento de Carga - Docker Swarm Demo"
echo "=================================================="
echo ""

FRONTEND_URL="http://localhost:8080"
BACKEND_URL="http://localhost:8080"

echo "1. Testando Frontend (múltiplas requisições para ver balanceamento):"
echo "-------------------------------------------------------------------"

for i in {1..10}; do
    echo "Requisição $i:"
    curl -s "$FRONTEND_URL" | grep -E "(Frontend Instance Info|Backend Response)" -A 2
    echo ""
    sleep 1
done

echo ""
echo "2. Testando Health Checks:"
echo "-------------------------"
echo "Frontend Health:"
curl -s "$FRONTEND_URL/health" | jq '.' 2>/dev/null || curl -s "$FRONTEND_URL/health"
echo ""

echo ""
echo "3. Verificando Status dos Serviços:"
echo "----------------------------------"
echo "Execute: docker service ls"
echo "Execute: docker service ps frontend"
echo "Execute: docker service ps backend"
echo ""

echo "4. Para escalar os serviços:"
echo "---------------------------"
echo "docker service scale frontend=5"
echo "docker service scale backend=5"
echo ""

echo "5. Para visualizar logs:"
echo "----------------------"
echo "docker service logs frontend"
echo "docker service logs backend"
echo ""

echo "✅ Teste concluído! Verifique as respostas acima para ver o balanceamento em ação."
