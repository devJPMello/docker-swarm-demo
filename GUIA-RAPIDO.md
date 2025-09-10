# 🚀 Guia Rápido - Docker Swarm Demo

## Execução em 5 Passos

### 1. Inicializar Swarm
```bash
docker swarm init
```

### 2. Deploy da Aplicação
```bash
docker stack deploy -c docker-compose.yml swarm-demo
```

### 3. Verificar Status
```bash
docker service ls
```

### 4. Acessar Aplicação
Abrir: **http://localhost:8080**

### 5. Testar Balanceamento
```powershell
# Windows
.\test-load-balancing.ps1

# Linux/Mac
./test-load-balancing.sh
```

## Comandos Essenciais

```bash
# Ver serviços
docker service ls

# Ver réplicas
docker service ps frontend
docker service ps backend

# Escalar
docker service scale frontend=5
docker service scale backend=5

# Logs
docker service logs frontend
docker service logs backend

# Remover
docker stack rm swarm-demo
```

## O que Observar

- ✅ Hostnames diferentes a cada refresh
- ✅ Container IDs alternando
- ✅ Balanceamento automático
- ✅ Alta disponibilidade
