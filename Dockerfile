# Use uma imagem base oficial do Python
FROM python:3.8-slim

# Defina variável de ambiente para desativar o uso do CUDA
ENV DLIB_USE_CUDA=0

# Instale as dependências necessárias do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libopenblas-dev \
        liblapack-dev \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instale as bibliotecas Python adicionais
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie os modelos, o código fonte e o diretório de faces para o contêiner
COPY models/ /app/models/
COPY faces/ /app/faces/
COPY . /app
WORKDIR /app

# Comando para executar ao iniciar o contêiner
CMD ["python", "main.py"]
