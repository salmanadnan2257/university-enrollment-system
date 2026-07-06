#!/usr/bin/env bash
# Auto‑build & run on Linux (Ubuntu)

# 1) Build if missing
if [[ -z "$(docker images -q pscs-app 2> /dev/null)" ]]; then
  echo "🔨 Building pscs-app..."
  docker build --no-cache -t pscs-app . || { echo "Build failed"; exit 1; }
fi

# 2) Allow X11 from container
xhost +local:docker

# 3) Launch
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  pscs-app
