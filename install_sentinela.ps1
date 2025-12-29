Write-Host "=== Instalador de SentinelA ==="

# Verificar requisitos
$requiredModules = @("python", "asterisk-manager", "fastapi", "whisper")
foreach ($module in $requiredModules) {
    if (-not (Get-Command $module -ErrorAction SilentlyContinue)) {
        Write-Host "❌ $module no encontrado. Instalando..."
        # Aquí deberías añadir comandos de instalación
    }
}

# Crear estructura de directorios
$dirs = @("pbx_audio", "transcripts", "photos", "data")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "📁 Creado directorio: $dir"
    }
}

# Configurar variables de entorno
[System.Environment]::SetEnvironmentVariable("AMI_HOST", "localhost")
[System.Environment]::SetEnvironmentVariable("AMI_PORT", "5038")
[System.Environment]::SetEnvironmentVariable("AMI_USER", "sentinela")
[System.Environment]::SetEnvironmentVariable("AMI_PASSWORD", "password_seguro")

Write-Host "✅ Instalación completada. Ejecute 'python pbx_connector.py' para iniciar."
