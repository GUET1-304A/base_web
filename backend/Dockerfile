FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p /app/uploads

EXPOSE 5000

# 2核机器: preload 共享内存, threads 提升并发, worker-class=gthread 避免阻塞
CMD ["gunicorn", "-w", "2", "--threads", "4", "--worker-class", "gthread", "-b", "0.0.0.0:5000", "--timeout", "30", "--keep-alive", "5", "--preload", "app:create_app()"]
