# Script PowerShell para testar o balanceamento de carga
# Execute este script após fazer o deploy da aplicação

Write-Host "🐳 Testando Balanceamento de Carga - Docker Swarm Demo" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$FRONTEND_URL = "http://localhost:8080"

Write-Host "1. Testando Frontend (múltiplas requisições para ver balanceamento):" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------------------" -ForegroundColor Yellow

for ($i = 1; $i -le 10; $i++) {
    Write-Host "Requisição $i:" -ForegroundColor Green
    try {
        $response = Invoke-WebRequest -Uri $FRONTEND_URL -UseBasicParsing
        $content = $response.Content
        
        # Extrair informações do frontend
        if ($content -match "Frontend Instance Info.*?<p><strong>Hostname:</strong> ([^<]+).*?<p><strong>Container ID:</strong> ([^<]+)") {
            Write-Host "  Frontend Hostname: $($matches[1])" -ForegroundColor White
            Write-Host "  Frontend Container ID: $($matches[2])" -ForegroundColor White
        }
        
        # Extrair informações do backend
        if ($content -match "Backend Response.*?<p><strong>Backend Hostname:</strong> ([^<]+).*?<p><strong>Backend Container ID:</strong> ([^<]+)") {
            Write-Host "  Backend Hostname: $($matches[1])" -ForegroundColor White
            Write-Host "  Backend Container ID: $($matches[2])" -ForegroundColor White
        }
        
        Write-Host ""
    }
    catch {
        Write-Host "  Erro na requisição: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "2. Testando Health Checks:" -ForegroundColor Yellow
Write-Host "-------------------------" -ForegroundColor Yellow
Write-Host "Frontend Health:" -ForegroundColor Green
try {
    $healthResponse = Invoke-WebRequest -Uri "$FRONTEND_URL/health" -UseBasicParsing
    Write-Host $healthResponse.Content -ForegroundColor White
}
catch {
    Write-Host "Erro ao acessar health check: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "3. Verificando Status dos Serviços:" -ForegroundColor Yellow
Write-Host "----------------------------------" -ForegroundColor Yellow
Write-Host "Execute: docker service ls" -ForegroundColor White
Write-Host "Execute: docker service ps frontend" -ForegroundColor White
Write-Host "Execute: docker service ps backend" -ForegroundColor White

Write-Host ""
Write-Host "4. Para escalar os serviços:" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow
Write-Host "docker service scale frontend=5" -ForegroundColor White
Write-Host "docker service scale backend=5" -ForegroundColor White

Write-Host ""
Write-Host "5. Para visualizar logs:" -ForegroundColor Yellow
Write-Host "----------------------" -ForegroundColor Yellow
Write-Host "docker service logs frontend" -ForegroundColor White
Write-Host "docker service logs backend" -ForegroundColor White

Write-Host ""
Write-Host "✅ Teste concluído! Verifique as respostas acima para ver o balanceamento em ação." -ForegroundColor Green
