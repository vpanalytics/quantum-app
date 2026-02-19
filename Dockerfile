# Use a imagem oficial do Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Expõe a porta que o Flask usará (padrão para desenvolvimento)
EXPOSE 5000

# Comando para inicializar a aplicação com Gunicorn
# O Render injeta a variável PORT automaticamente
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-5000}", "app:app"]
