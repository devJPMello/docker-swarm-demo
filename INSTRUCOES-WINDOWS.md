# 🪟 Instruções Específicas para Windows

## Pré-requisitos

1. **Docker Desktop for Windows** instalado e rodando
2. **PowerShell** ou **Command Prompt**
3. **Git** (opcional, para clonar repositórios)

## Verificação Inicial

```powershell
# Verificar se Docker está rodando
docker --version
docker info

# Verificar se Docker Desktop está ativo
docker ps
```

## Execução Passo a Passo

### 1. Abrir PowerShell como Administrador
- Clique com botão direito no PowerShell
- Selecione "Executar como administrador"

### 2. Navegar para o Diretório do Projeto
```powershell
cd C:\Users\joaop\docker-swarm-demo
```

### 3. Inicializar Docker Swarm
```powershell
# Verificar se já está inicializado
docker node ls

# Se não estiver, inicializar
docker swarm init
```

### 4. Fazer Deploy da Aplicação
```powershell
# Deploy da stack
docker stack deploy -c docker-compose.yml swarm-demo

# Aguardar alguns segundos e verificar
docker service ls
```

### 5. Verificar Status dos Serviços
```powershell
# Listar todos os serviços
docker service ls

# Ver detalhes do frontend
docker service ps frontend

# Ver detalhes do backend
docker service ps backend

# Ver logs (opcional)
docker service logs frontend
```

### 6. Acessar a Aplicação
- Abrir navegador
- Acessar: **http://localhost:8080**
- Recarregar página várias vezes para ver balanceamento

### 7. Executar Teste de Balanceamento
```powershell
# Executar script de teste
.\test-load-balancing.ps1
```

## Comandos de Gerenciamento

### Escalar Serviços
```powershell
# Aumentar réplicas
docker service scale frontend=5
docker service scale backend=5

# Diminuir réplicas
docker service scale frontend=2
docker service scale backend=2
```

### Monitoramento
```powershell
# Ver logs em tempo real
docker service logs -f frontend
docker service logs -f backend

# Ver estatísticas de recursos
docker stats

# Ver detalhes de um serviço
docker service inspect frontend
```

### Limpeza
```powershell
# Remover stack completa
docker stack rm swarm-demo

# Verificar se foi removido
docker service ls
```

## Solução de Problemas

### Erro: "Port already in use"
```powershell
# Verificar o que está usando a porta 8080
netstat -ano | findstr :8080

# Se necessário, matar o processo
taskkill /PID <PID_NUMBER> /F

# Ou alterar a porta no docker-compose.yml
```

### Erro: "Docker daemon not running"
1. Abrir Docker Desktop
2. Aguardar inicialização completa
3. Verificar se o ícone está verde na bandeja do sistema

### Erro: "Permission denied"
- Executar PowerShell como Administrador
- Verificar se Docker Desktop tem permissões necessárias

### Serviços não iniciam
```powershell
# Ver logs detalhados
docker service logs frontend --details
docker service logs backend --details

# Verificar se as imagens foram construídas
docker images | findstr swarm-demo
```

## Verificação de Funcionamento

### ✅ Checklist de Sucesso
- [ ] `docker service ls` mostra frontend e backend com 3 réplicas cada
- [ ] `docker service ps frontend` mostra todas as réplicas como "Running"
- [ ] Acessar http://localhost:8080 mostra a página funcionando
- [ ] Recarregar a página mostra hostnames diferentes
- [ ] Script de teste executa sem erros

### 🔍 O que Observar
1. **Hostnames diferentes**: A cada refresh, o hostname do frontend muda
2. **Container IDs diferentes**: IDs únicos para cada réplica
3. **Backend balanceamento**: As chamadas internas também alternam entre réplicas
4. **Logs**: Mostram requisições distribuídas entre réplicas

## Próximos Passos

1. **Portainer**: Instalar interface web para gerenciamento
2. **Monitoramento**: Adicionar métricas e alertas
3. **Persistência**: Implementar volumes para dados
4. **SSL**: Configurar HTTPS
5. **CI/CD**: Automatizar deploy

---

**Dica**: Mantenha o Docker Desktop rodando durante todo o teste para evitar problemas de conectividade.
