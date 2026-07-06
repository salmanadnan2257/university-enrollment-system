# 1) Base image
FROM python:3.10-slim

# 2) System deps for PyQt6 & SQLite
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libx11-6 libxext6 libxrender1 libxi6 libxcb1 libdbus-1-3 sqlite3 \
 && rm -rf /var/lib/apt/lists/*

# 3) Set workdir
WORKDIR /app

# 4) Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy your code (including the seeded demo student.db)
COPY . .

# 6) Use the host X11 on Linux/macOS
ENV QT_QPA_PLATFORM=xcb

# 7) Default run
ENTRYPOINT ["python", "login_page.py"]
