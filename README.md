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
    O projeto inclui um script automático, mas você pode forçar a criação:
    ```bash
    docker-compose exec bot-modo-ia python make_db.py
    ```

## 🖥️ Acesso ao Dashboard

Após subir o container, acesse:

* **URL:** `http://localhost:5005` (ou IP do servidor)
* **Login Padrão:** Definido no `.env` (Default: `admin`)

## 🛣️ Rotas da API

O sistema expõe uma API RESTful para integração com **n8n** ou **WPPConnect**:

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/registros` | Lista todos os clientes e status |
| `POST` | `/api/registro` | Cria novo registro |
| `PUT` | `/api/registro/<id>` | Atualiza status (ex: mudar para 'Desativado') |
| `DELETE` | `/api/registro/<id>` | Remove um cliente |

## 📁 Estrutura de Arquivos

```text
bot-modo-ia/
├── app.py              # Aplicação Flask (Backend)
├── make_db.py          # Script de setup do Banco
├── requirements.txt    # Dependências Python
├── Dockerfile          # Imagem Docker
├── docker-compose.yml  # Orquestração
├── static/             # CSS e JS customizados
└── templates/          # HTML (Login e Dashboard)

<div align="center"> Desenvolvido por <b>Astral Wave Label</b> 🎹 </div>
