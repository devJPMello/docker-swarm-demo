# 🐳 Guia Passo a Passo - Docker Swarm Demo

## 📋 Visão Geral

Este guia demonstra a implementação de uma aplicação web containerizada em um cluster Docker Swarm, com foco em balanceamento de carga, escalabilidade e alta disponibilidade.

### 🎯 Objetivos
- Inicializar e operar um cluster Docker Swarm
- Criar e usar redes overlay para comunicação entre serviços
- Implantar serviços com múltiplas réplicas
- Demonstrar balanceamento de carga automático
- Visualizar tudo via Portainer

---

## 🏗️ Topologia da Aplicação

### Serviços
- **Frontend**: 3 réplicas (Flask) - Porta 8080
- **Backend**: 3 réplicas (Flask API) - Porta interna 5000
- **Portainer**: 1 réplica - Porta 9000 (opcional)

### Rede
- **Nome**: `swarm-network`
- **Driver**: `overlay`
- **Subnet**: `10.0.1.0/24`
- **Comunicação**: Frontend ↔ Backend via service discovery

### Portas
- **8080**: Frontend (entrada do usuário)
- **9000**: Portainer (gerenciamento)
- **5000**: Backend (apenas interna)

---

## 🚀 Como Iniciar o Swarm e a Rede

### 1. Verificar Pré-requisitos
```bash
# Verificar se Docker está rodando
docker --version
docker info
```

### 2. Inicializar Docker Swarm
```bash
# Inicializar o swarm (se ainda não estiver ativo)
docker swarm init

# Verificar status do swarm
docker node ls
```

### 3. Verificar Rede Overlay
```bash
# Listar redes (a rede overlay será criada automaticamente)
docker network ls

# A rede swarm-network será criada durante o deploy
```

---

## 📦 Como Fazer Deploy e Escalar

### 1. Construir as Imagens
```bash
# Construir imagem do frontend
docker build -t swarm-demo-frontend:latest ./frontend

# Construir imagem do backend
docker build -t swarm-demo-backend:latest ./backend
```

### 2. Deploy da Stack
```bash
# Deploy completo da aplicação
docker stack deploy -c docker-stack.yml swarm-demo

# Verificar status dos serviços
docker service ls
```

### 3. Verificar Deploy
```bash
# Ver detalhes das réplicas
docker service ps swarm-demo_frontend
docker service ps swarm-demo_backend

# Verificar logs
docker service logs swarm-demo_frontend
docker service logs swarm-demo_backend
```

### 4. Acessar a Aplicação
- **Frontend**: http://localhost:8080
- **Portainer**: http://localhost:9000

---

## ⚖️ Como Reproduzir os Testes de Balanceamento

### Teste Manual (Navegador)
1. Acesse http://localhost:8080
2. Recarregue a página múltiplas vezes (F5)
3. Observe as mudanças nos hostnames e container IDs
4. Note que tanto frontend quanto backend alternam entre réplicas

### Teste Automatizado (Script)
```bash
# Linux/Mac
./demonstracao-escopo.sh

# Windows
.\demonstracao-escopo.ps1
```

### Teste com cURL
```bash
# Múltiplas requisições para ver balanceamento
for i in {1..10}; do
  echo "Requisição $i:"
  curl -s http://localhost:8080 | grep -E "(Frontend Hostname|Backend Hostname)"
  sleep 1
done
```

### O que Observar
- **Frontend**: Hostname e Container ID diferentes a cada requisição
- **Backend**: Hostname e Container ID diferentes nas chamadas internas
- **Algoritmo**: Round-robin do Docker Swarm
- **Distribuição**: Uniforme entre todas as réplicas

---

## 📈 Como Executar Scaling

### Escalar Serviços
```bash
# Escalar frontend para 5 réplicas
docker service scale swarm-demo_frontend=5

# Escalar backend para 5 réplicas
docker service scale swarm-demo_backend=5

# Escalar ambos simultaneamente
docker service scale swarm-demo_frontend=5 swarm-demo_backend=5
```

### Verificar Escalonamento
```bash
# Ver status dos serviços
docker service ls

# Ver detalhes das réplicas
docker service ps swarm-demo_frontend
docker service ps swarm-demo_backend

# Ver logs em tempo real
docker service logs -f swarm-demo_frontend
```

### Reduzir Réplicas
```bash
# Reduzir frontend para 2 réplicas
docker service scale swarm-demo_frontend=2

# Reduzir backend para 2 réplicas
docker service scale swarm-demo_backend=2
```

### Impacto no Balanceamento
- **Mais réplicas**: Maior distribuição de carga
- **Menos réplicas**: Menor distribuição, mas ainda funcional
- **Zero downtime**: Scaling acontece sem interrupção

---

## 🔄 Atualizações sem Downtime

### Rolling Updates
```bash
# Atualizar imagem do frontend
docker service update --image swarm-demo-frontend:latest swarm-demo_frontend

# Atualizar imagem do backend
docker service update --image swarm-demo-backend:latest swarm-demo_backend
```

### Configuração de Updates
- **Paralelismo**: 1 réplica por vez (configurado no docker-stack.yml)
- **Delay**: 10 segundos entre atualizações
- **Rollback**: Automático em caso de falha
- **Health checks**: Verificação de saúde antes de considerar atualizada

---

## 📊 Monitoramento e Gerenciamento

### Comandos Úteis
```bash
# Status geral
docker service ls

# Detalhes de um serviço
docker service inspect swarm-demo_frontend

# Logs em tempo real
docker service logs -f swarm-demo_frontend

# Estatísticas de recursos
docker stats

# Listar redes
docker network ls

# Inspecionar rede overlay
docker network inspect swarm-demo_swarm-network
```

### Portainer (Interface Web)
1. Acesse http://localhost:9000
2. Crie usuário admin no primeiro acesso
3. Navegue pelas seções:
   - **Dashboard**: Visão geral do cluster
   - **Containers**: Lista e status dos containers
   - **Services**: Gerenciamento de serviços
   - **Networks**: Configuração de redes
   - **Logs**: Visualização de logs

---

## 🧪 Scripts de Teste

### Deploy Automatizado
```bash
# Deploy completo (Linux/Mac)
./deploy-complete.sh

# Deploy completo (Windows)
.\deploy-complete.ps1
```

### Demonstração do Escopo
```bash
# Demonstração completa (Linux/Mac)
./demonstracao-escopo.sh

# Demonstração completa (Windows)
.\demonstracao-escopo.ps1
```

### Teste de Balanceamento
```bash
# Teste simples (Linux/Mac)
./test-load-balancing.sh

# Teste simples (Windows)
.\test-load-balancing.ps1
```

---

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. Porta 8080 ocupada
```bash
# Verificar processos na porta
netstat -ano | findstr :8080

# Alterar porta no docker-stack.yml
# ports:
#   - "8081:5000"  # Usar porta 8081
```

#### 2. Serviços não iniciam
```bash
# Verificar logs
docker service logs swarm-demo_frontend
docker service logs swarm-demo_backend

# Verificar status
docker service ps swarm-demo_frontend
```

#### 3. Rede não funciona
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

---

## ✅ Critérios de Aceite - Verificação

### ✅ Aplicação permanece acessível durante updates
- **Rolling updates** configurados (parallelism: 1)
- **Health checks** verificam saúde antes de considerar atualizada
- **Zero downtime** durante escalonamento

### ✅ Balanceamento visível no frontend e backend
- **Frontend**: Hostname/Container ID alternam a cada refresh
- **Backend**: Hostname/Container ID alternam nas chamadas internas
- **Algoritmo**: Round-robin do Docker Swarm

### ✅ Documentação completa
- **Topologia**: Serviços, rede e portas documentados
- **Testes**: Scripts automatizados para balanceamento
- **Scaling**: Comandos e exemplos de escalonamento

---

## 📚 Próximos Passos

### Melhorias Sugeridas
1. **Monitoramento**: Prometheus + Grafana
2. **Segurança**: SSL/TLS e certificados
3. **Persistência**: Volumes para dados
4. **CI/CD**: Pipeline automatizado
5. **Testes**: Suíte automatizada

### Aplicações Reais
- **E-commerce** com alta disponibilidade
- **APIs** com escalabilidade automática
- **Microserviços** distribuídos
- **Aplicações críticas** 24/7

---

**🎉 Guia concluído! A aplicação está pronta para demonstração e uso em produção.**

**Desenvolvido para demonstração prática de Docker Swarm com balanceamento de carga e alta disponibilidade.**
