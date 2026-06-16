FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    RESOLUTION=1600x1000x24 \
    APP_ENTRY=run_.py \
    RUNNING_IN_DOCKER=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    fluxbox \
    libglib2.0-0 \
    libgl1 \
    libice6 \
    libsm6 \
    libx11-6 \
    libxcursor1 \
    libxext6 \
    libxi6 \
    libxinerama1 \
    libxrandr2 \
    libxrender1 \
    novnc \
    python3-tk \
    tk \
    websockify \
    x11-utils \
    x11vnc \
    xauth \
    xclip \
    xfonts-base \
    xvfb \
    && ln -sf /usr/share/novnc/vnc.html /usr/share/novnc/index.html \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN if [ ! -f run_.py ] && [ -f run.py ]; then cp run.py run_.py; fi \
    && test -f run_.py \
    && rm -f brains*.pyd brains*.so brains.c \
    && python setup.py build_ext --inplace \
    && chmod +x docker/start.sh

EXPOSE 6080

CMD ["docker/start.sh"]
