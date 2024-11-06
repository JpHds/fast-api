# Usa uma imagem Python como base
FROM python:3.9-slim

# Instala as dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner
COPY . .

# Define a porta que a aplicação vai usar
EXPOSE 5431

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
