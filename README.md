# 🤖 BOT_MODO_IA - Gerenciador de Estados

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,docker,postgres,bootstrap,html,css,js,linux,git&theme=dark" />
</div>

<br>

Sistema Web CRUD desenvolvido para gerenciar os estados de operação da Inteligência Artificial (**Ativado, Desativado, Híbrido, Manutenção**) para clientes no WhatsApp. O projeto roda em container Docker isolado e se conecta à infraestrutura existente da **Astral Wave Label**.

## 🚀 Tecnologias

* **Backend:** Python 3.9 + Flask
* **Database:** PostgreSQL (Conexão via Docker Network)
* **Frontend:** HTML5, Bootstrap 5, JS (Fetch API)
* **Infra:** Docker & Docker Compose

## 📋 Pré-requisitos

* Docker e Docker Compose instalados.
* Rede Docker `awl_network` criada.
* Banco de dados PostgreSQL rodando na rede.

## ⚙️ Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/bot-modo-ia.git](https://github.com/seu-usuario/bot-modo-ia.git)
    cd bot-modo-ia
    ```

2.  **Configure as Variáveis de Ambiente:**
    Copie o arquivo de exemplo e edite com suas credenciais.
    ```bash
    cp .env.example .env
    nano .env
    ```
    *Certifique-se de definir `APP_PORT=5005` (ou outra porta livre).*

3.  **Suba o Container:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Crie a Tabela no Banco:**
    O projeto inclui um script Python, mas recomendamos o método via Shell abaixo para garantir a conexão direta com o container do banco.

### 🛠️ Método Recomendado: Script Shell (`make_db.sh`)

Este script executa o comando SQL diretamente dentro do container do Postgres, evitando erros de rede ou dependência.

1. Crie o arquivo `make_db.sh` e cole o conteúdo abaixo:

```bash
#!/bin/bash

# Define as cores para feedback visual
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔌 Conectando ao container awlsrvDB_postgres...${NC}"

# Executa o comando SQL diretamente dentro do container
docker exec -i awlsrvDB_postgres psql -U admin_root -d postgres <<EOF
BEGIN;

CREATE TABLE IF NOT EXISTS BOT_MODO_IA (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    modo_ia VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMIT;
EOF

# Verifica o código de saída do comando anterior
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tabela BOT_MODO_IA criada/verificada com sucesso!${NC}"
else
    echo -e "${RED}❌ Erro ao criar a tabela. Verifique se o container 'awlsrvDB_postgres' está rodando.${NC}"
fi
