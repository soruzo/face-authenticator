# Identificação Facial com dlib
Atividade de identificação facial, para o projeto final de Visão Computacional.

---
### Integrantes:
- Anthony Carvalho
- Bruno Eduardo
- Bruno Neves
- Carla Scherer

---
## Estrutura do Projeto
- `Dockerfile`: Define o ambiente e dependências do projeto.
- `requirements.txt`: Lista as dependências Python.
- `main.py`: Script principal para identificação facial.
- `models/`: Contém modelos pré-treinados do `dlib`.
- `faces/`: Diretório com imagens de faces para reconhecimento.
- `to-identify/`: Diretório com imagens a serem identificadas.

---
## Configurando o Ambiente
#### Você precisará do docker instalado
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```
---
## Como Testar
#### 1. Coloque as imagens que deseja identificar no diretório **/to-identify**. Ex:
```bash
├── to_identify/
│   ├── {nome_do_arquivo}.jpg
│   ├── {any}.jpg
```
#### 2. Coloque imagens de referência para cada usuário no diretório **/faces**, em subdiretórios diferentes (para cada usuário). Ex:
```bash
├── faces/
│   ├── {nome_da_pasta}/
│   │   ├── {nome_do_arquivo}.jpg
│   │   └── {any}.jpg
│   └── user02/
│       ├── foto1.jpg
│       └── foto2.jpg
```
#### 3. Execute o contêiner Docker na pasta raiz do projeto.
```bash
docker build -t reconhecimento_facial .
docker run reconhecimento_facial
```

## O que esperar?
O script **main.py** processará as imagens em **/to-identify**, tentando identificar as faces com base nos embeddings extraídos das imagens em **/faces**.
E retornará (no terminal) se a foto foi identificada ou não.