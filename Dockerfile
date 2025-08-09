FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 安装中文字体（文泉驿正黑）
RUN apt-get update && \
    apt-get install -y \
        fonts-wqy-zenhei \
        libfreetype6-dev \
        libpng-dev \
        libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN uv sync

ENV SENDER_EMAIL=
ENV SENDER_PASSWORD=
ENV RECEIVER_EMAIL=
ENV SMTP_SERVER=
ENV SMTP_PORT=

CMD ["uv", "run", "python", "src/main.py"]