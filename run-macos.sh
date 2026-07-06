#!/usr/bin/env bash
# Auto‑build & run on macOS (with XQuartz)

# 1) Build if missing
if [ -z "$(docker images -q pscs-app 2>/dev/null)" ]; then
  echo "🔨 Building pscs-app..."
  docker build --no-cache -t pscs-app . || { echo "Build failed"; exit 1; }
fi

# 2) Get host IP and allow XQuartz
IP=$(ifconfig en0 | awk '/inet /{print $2}')
xhost + $IP

# 3) Launch
docker run -it --rm \
  -e DISPLAY=${IP}:0 \
  pscs-app
