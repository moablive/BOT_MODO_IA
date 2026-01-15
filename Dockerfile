FROM python:3.9-slim

# Evita arquivos .pyc e logs em buffer (melhor para Docker)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema e limpa cache em uma única camada
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cria um usuário não-root para segurança
RUN useradd -m appuser
USER appuser

# Copia o código com permissão para o novo usuário
COPY --chown=appuser:appuser . .

EXPOSE 5000

# Usa Gunicorn para produção (mais rápido e estável que python app.py)
# -w 4: 4 Workers (bom para o limite de CPU 0.5 que você definiu)
# -b: Bind na porta 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
