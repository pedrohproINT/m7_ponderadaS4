# Simple One-Page App (EC2 + RDS MySQL)

## Link do vídeo
https://drive.google.com/file/d/1iqQYfKAJbT8VjUTFhGYpDqNLJJf4Ttt_/view?usp=drive_link

## Arquitetura
- **Frontend + Backend**: uma única aplicação Flask servida em um **EC2 Amazon Linux** (público) por meio do `flask run` (ou Gunicorn/Nginx em produção).
- **Banco de dados**: **RDS MySQL** (privado, sem acesso público) na mesma VPC do EC2.
- **Segurança**:
  - SG do EC2: HTTP/8080 (ou 80) aberto para a internet; SSH/22 apenas para o IP do desenvolvedor.
  - SG do RDS: MySQL/3306 liberado **somente** para o SG do EC2.
- **Fluxo**: Usuário → EC2 (Flask app) → RDS (MySQL).
- **Público**: a página e as operações (POST/GET) ficam acessíveis via IP público do EC2.

## Modelo de Dados (2 tabelas relacionadas)
- `customers`  
  - id (INT, PK)  
  - name (VARCHAR)  
  - email (VARCHAR)  
  - created_at (DATETIME)  
- `orders`  
  - id (INT, PK)  
  - customer_id (FK → customers.id)  
  - amount (DECIMAL)  
  - status (VARCHAR)  
  - created_at (DATETIME)  

> Tipos usados: **INTEGER**, **VARCHAR**, **DECIMAL**, **DATETIME**.

## Requisitos Atendidos
1. Aplicação web integrada a uma base de dados (Flask ↔ MySQL RDS).  
2. Duas tabelas com ≥ 4 campos e ≥ 3 tipos de dados distintos (customers e orders).  
3. Uma página web única:
   - **Criação (POST)**: insere **um customer e um order** (as duas tabelas são atualizadas).  
   - **Listagem (GET)**: exibe um JOIN com os 100 registros mais recentes.

## Deploy (resumo)
1. Criar o **RDS MySQL** (`simpledb`), com usuário/senha e SG que permite 3306 **apenas** do SG do EC2.  
2. Criar ou usar um **EC2** existente (Amazon Linux), liberar portas 8080/80.  
3. Instalar Python, venv, Flask, SQLAlchemy, PyMySQL.  
4. App Flask em `/opt/simpleapp` com `app.py`, `templates/index.html`, `static/style.css`.  
5. Rodar com `flask run --host=0.0.0.0 --port=8080`.  
6. Acessar `http://EC2_PUBLIC_IP:8080/`.

## Uso
- **Criar**: preencher Nome, E-mail, Valor e Status e enviar.  
- **Consultar**: clicar no botão "Consultar" para atualizar a lista.  
- **Listar**: a tabela exibe os últimos 100 pedidos com dados do cliente.

## Observações
- Não exponha o RDS à internet. O EC2 é o único ponto público.  
- Para produção: usar Gunicorn + Nginx (porta 80) e HTTPS (ACM/ALB ou certbot).  
- Logs ficam disponíveis em `/opt/simpleapp/flask.log` quando rodando em background.
