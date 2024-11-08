# FastAPI Project

Este é um projeto de exemplo usando FastAPI. Abaixo estão as instruções para configurar o ambiente e executar o projeto em diferentes sistemas operacionais e utilizando Docker.


## Descrição

**FastAPI Project** é uma aplicação desenvolvida para demonstrar o uso do framework FastAPI, uma das ferramentas mais rápidas para criar APIs com Python. O projeto oferece uma API simples, com endpoints básicos para **GET**, **POST**, e outros métodos HTTP.

### Funcionalidades
- Exemplo de CRUD.
- Autenticação de usuários com **JWT** (JSON Web Tokens).
- Documentação interativa gerada automaticamente com **Swagger UI**.
- Configuração simples e rápida, utilizando Docker.

### Tecnologias Utilizadas
- **FastAPI**: Framework moderno e rápido para APIs.
- **Uvicorn**: Servidor ASGI de alta performance.
- **SQLAlchemy**: ORM para banco de dados.
- **JWT**: Autenticação com tokens.
- **Docker**: Para containerização e fácil execução do projeto.


## Testando a Aplicação
### A aplicação gerencia três tipos de usuários, cada um com diferentes permissões:

1. **Superadmin**
- **Criação automática**: O **superadmin** é criado automaticamente quando a aplicação é iniciada, usando as informações fornecidas no arquivo `.env`.
-  **Permissões**:
    - Criar **admins**.
    - Atualizar e excluir **clientes**.
    - Atualizar e excluir **admins**.
    - Tem todas as permissões de um **admin**.

2. **Admin**
- **Permissões**:
    - Criar e consultar **clientes**.
    - Não pode gerenciar **admins** ou alterar usuários com papel superior.
3. Cliente
- **Permissões**:
    - Apenas pode ser gerenciado pelos **admins** ou **superadmins**.

## Autenticação
- **JWT** (JSON Web Tokens) é usado para autenticação.
- As permissões de cada tipo de usuário são separadas por roles definidas no sistema:
    - **superadmin**: Permissões completas (criação de **admins**, gerenciamento de **clientes**, etc.).
    - **admin**: Permissões limitadas (criação e consulta de **clientes**).
    - **cliente**: Somente visualização e gerência pelos **admins**.

## Testando a aplicação
- Após iniciar a aplicação, o **superadmin** será criado automaticamente. Você pode utilizar as credenciais fornecidas no `.env` para se autenticar como **superadmin**.
- Use a API para testar as permissões:
    - Superadmin pode criar **admins**, atualizar e excluir **clientes**.
    - Admin pode criar e consultar **clientes**, mas não pode criar **admins** ou fazer alterações em outros **admins**.
    - Clientes são gerenciados apenas pelos **admins** e **superadmins**.

## Acessando a Documentação da API (Swagger)
 Você pode acessar a documentação interativa da API gerada automaticamente pelo Swagger UI para testar os endpoints da aplicação.

- Acesse a documentação em: http://localhost:8000/docs (ou na URL configurada para a aplicação).
A interface do Swagger permitirá que você visualize todos os endpoints disponíveis, faça chamadas de teste e veja a resposta da API de maneira fácil e intuitiva.


## Pré-requisitos

Certifique-se de ter o **Git**, **Python** e **Docker** (caso opte por usá-lo) instalados em seu sistema.


## Instruções para Windows

1. **Clone o repositório**:

   ```cmd
   git clone https://github.com/JpHds/fast-api.git

2. **Crie um arquivo `.env`** na raiz do projeto e configure-o baseado no arquivo `.env.example`.

3. **Acesse o diretório do projeto**:

    ```console
    cd fast-api

4. **Crie e ative um ambiente virtual**:

    ```cmd
    python -m venv nome_do_ambiente_aqui
    nome_do_ambiente_aqui\Scripts\activate


5. **Instale as dependências**:

    ```cmd
    pip install -r requirements.txt

6. **Execute o script principal**:
    python main.py

## Instruções para Linux

1. **Clone o repositório**:

    ```cmd
    git clone https://github.com/JpHds/fast-api.git

2. **Acesse o diretório do projeto**:

    ```console
    cd fast-api

3. **Crie um arquivo `.env`** na raiz do projeto e configure-o baseado no arquivo `.env.example`.
   
4. **Crie e ative um ambiente virtual**:

    ```cmd
    python3 -m venv env
    source env/bin/activate

5. **Instale as dependências necessárias**:

    ```cmd
    pip install -r requirements.txt

6. **Execute o script principal**:

    ```cmd
    python main.py

## Usando Docker

### Passos para qualquer sistema operacional (Windows, Linux ou macOS)

1. **Clone o repositório**:

    ```console
    git clone https://github.com/JpHds/fast-api.git
    cd fast-api

2. **Crie um arquivo .env na raiz do projeto e configure-o baseado no arquivo .env.example**.

3. **Construa a imagem Docker**:

    ```cmd
    docker build -t nome-da-imagem .

4. **Acesse a aplicação**:

    Após o contêiner iniciar, você pode acessar a aplicação no navegador em http://localhost:8000 (ou na porta configurada em seu arquivo `.env`).

---

Pronto! Agora você tem o projeto configurado e em execução.
