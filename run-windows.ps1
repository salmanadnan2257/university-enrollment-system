# Auto‑build & run on Windows (PowerShell + VcXsrv/Xming)

# 1) Build if missing
if (-not (docker images -q pscs-app)) {
  Write-Host "🔨 Building pscs-app..."
  docker build --no-cache -t pscs-app . `
    || { Write-Error "Build failed"; exit 1 }
}

# 2) Set DISPLAY for your X server
$Env:DISPLAY = "host.docker.internal:0.0"

# 3) Launch
docker run -it --rm `
  -e DISPLAY=$Env:DISPLAY `
  pscs-app
