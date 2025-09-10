# 🐳 Docker Swarm Demo - Aplicação com Réplicas e Balanceamento

Este projeto demonstra a implantação de uma aplicação web containerizada em um cluster Docker Swarm, com escala horizontal (réplicas) e balanceamento de carga automático entre serviços.

## 📋 Visão Geral

A aplicação consiste em:
- **Frontend**: Serviço HTTP que exibe informações da instância e chama o backend
- **Backend**: API simples que retorna informações da instância (hostname, container ID)
- **Rede Overlay**: Comunicação entre os serviços
- **Balanceamento**: Automático entre múltiplas réplicas

## 🏗️ Arquitetura

```
Internet → Frontend (3 réplicas) → Backend (3 réplicas)
              ↓
         Rede Overlay (swarm-network)
```

### Topologia
- **Serviços**: frontend, backend
- **Rede**: swarm-network (overlay)
- **Portas**: 8080 (frontend) → 5000 (interno)
- **Réplicas**: 3 frontend, 3 backend (configurável)

## 🚀 Como Executar

### Pré-requisitos
- Docker Desktop ou Docker Engine
- Docker Compose
- Acesso ao terminal/PowerShell

### 1. Inicializar o Docker Swarm

```bash
# Inicializar o swarm (se ainda não estiver inicializado)
docker swarm init

# Verificar status
docker node ls
```

### 2. Fazer Deploy da Aplicação

```bash
# Deploy da stack completa
docker stack deploy -c docker-compose.yml swarm-demo

# Verificar serviços
docker service ls
```

### 3. Verificar Status

```bash
# Listar serviços
docker service ls

# Ver detalhes do frontend
docker service ps frontend

# Ver detalhes do backend
docker service ps backend

# Ver logs
docker service logs frontend
docker service logs backend
```

### 4. Acessar a Aplicação

Abra seu navegador em: **http://localhost:8080**

## 🧪 Testando o Balanceamento

### Teste Manual
1. Acesse http://localhost:8080
2. Recarregue a página várias vezes (F5)
3. Observe as mudanças nos hostnames e container IDs
4. Note que tanto frontend quanto backend alternam entre réplicas

### Teste Automatizado

**Windows (PowerShell):**
```powershell
.\test-load-balancing.ps1
```

**Linux/Mac (Bash):**
```bash
./test-load-balancing.sh
```

### Teste com cURL
```bash
# Múltiplas requisições para ver balanceamento
for i in {1..10}; do
  echo "Requisição $i:"
  curl -s http://localhost:8080 | grep -E "(Hostname|Container ID)"
  sleep 1
done
```

## 📈 Escalando os Serviços

### Aumentar Réplicas
```bash
# Escalar frontend para 5 réplicas
docker service scale frontend=5

# Escalar backend para 5 réplicas
docker service scale backend=5

# Verificar escalonamento
docker service ps frontend
docker service ps backend
```

### Diminuir Réplicas
```bash
# Reduzir para 2 réplicas
docker service scale frontend=2
docker service scale backend=2
```

## 🔧 Comandos Úteis

### Monitoramento
```bash
# Status dos serviços
docker service ls

# Detalhes de um serviço
docker service inspect frontend

# Logs em tempo real
docker service logs -f frontend

# Estatísticas de recursos
docker stats
```

### Gerenciamento
```bash
# Atualizar serviço
docker service update --image swarm-demo-frontend:latest frontend

# Remover serviço
docker service rm frontend

# Remover stack completa
docker stack rm swarm-demo
```

### Rede
```bash
# Listar redes
docker network ls

# Inspecionar rede overlay
docker network inspect swarm-demo_swarm-network
```

## 🐳 Portainer (Opcional)

Para visualização via interface web:

1. Instalar Portainer:
```bash
docker service create \
  --name portainer \
  --publish 9000:9000 \
  --constraint 'node.role == manager' \
  --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
  portainer/portainer-ce
```

2. Acessar: http://localhost:9000

## 📁 Estrutura do Projeto

```
docker-swarm-demo/
├── frontend/
│   ├── app.py              # Aplicação Flask frontend
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile         # Imagem Docker frontend
├── backend/
│   ├── app.py             # Aplicação Flask backend
│   ├── requirements.txt   # Dependências Python
│   └── Dockerfile        # Imagem Docker backend
├── configs/
│   └── app-config.yml    # Configurações da aplicação
├── secrets/
│   └── api-key.txt       # Chave API (demonstração)
├── docker-compose.yml    # Stack Docker Swarm
├── test-load-balancing.sh    # Script de teste (Linux/Mac)
├── test-load-balancing.ps1   # Script de teste (Windows)
└── README.md             # Esta documentação
```

## 🔍 O que Observar

### Balanceamento de Carga
- **Frontend**: Cada refresh mostra hostname/container ID diferente
- **Backend**: Chamadas internas distribuem entre réplicas
- **Algoritmo**: Round-robin do Docker Swarm

### Alta Disponibilidade
- **Restart**: Containers reiniciam automaticamente em falhas
- **Rolling Updates**: Atualizações sem downtime
- **Health Checks**: Monitoramento automático de saúde

### Escalabilidade
- **Horizontal**: Aumentar/diminuir réplicas dinamicamente
- **Recursos**: Limites de CPU/memória configurados
- **Rede**: Comunicação eficiente via overlay

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Porta 8080 ocupada**:
   ```bash
   # Verificar processos na porta
   netstat -ano | findstr :8080
   # Alterar porta no docker-compose.yml
   ```

2. **Serviços não iniciam**:
   ```bash
   # Verificar logs
   docker service logs frontend
   docker service logs backend
   ```

3. **Rede não funciona**:
   ```bash
   # Verificar rede overlay
   docker network ls
   docker network inspect swarm-demo_swarm-network
   ```

### Limpeza
```bash
# Remover stack
docker stack rm swarm-demo

# Remover imagens
docker image rm swarm-demo-frontend:latest
docker image rm swarm-demo-backend:latest

# Limpar sistema (cuidado!)
docker system prune -a
```

## 📚 Conceitos Demonstrados

- ✅ **Docker Swarm**: Cluster nativo do Docker
- ✅ **Overlay Networks**: Comunicação entre nós
- ✅ **Service Discovery**: Resolução automática de nomes
- ✅ **Load Balancing**: Distribuição automática de tráfego
- ✅ **Health Checks**: Monitoramento de saúde
- ✅ **Rolling Updates**: Atualizações sem downtime
- ✅ **Scaling**: Escalonamento horizontal
- ✅ **High Availability**: Alta disponibilidade

## 🎯 Próximos Passos

- Implementar persistência de dados
- Adicionar monitoramento (Prometheus/Grafana)
- Configurar SSL/TLS
- Implementar CI/CD
- Adicionar testes automatizados

---

**Desenvolvido para demonstração de Docker Swarm com balanceamento de carga e alta disponibilidade.**
