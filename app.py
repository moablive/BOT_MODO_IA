import os
import sys
import logging
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO DE LOGS (Essencial para Debug) ---
# Configura o log para sair no terminal do Docker (stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("AstralBot")

# --- 2. CARREGAMENTO DE AMBIENTE ---
logger.info("🚀 Iniciando a aplicação...")
load_dotenv()

app = Flask(__name__)

# Verifica variáveis críticas
REQUIRED_VARS = ['APP_SECRET_KEY', 'API_SECRET_KEY', 'APP_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing_vars:
    logger.critical(f"❌ ERRO FATAL: Variáveis de ambiente faltando: {missing_vars}")
    sys.exit(1)

app.secret_key = os.getenv('APP_SECRET_KEY')
app.config['API_KEY'] = os.getenv('API_SECRET_KEY')
APP_PASSWORD = os.getenv('APP_PASSWORD')

# Config do Banco
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')

logger.info(f"🔧 Configuração de DB carregada: Host={DB_HOST}, Port={DB_PORT}, User={DB_USER}")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        logger.error(f"❌ FALHA DE CONEXÃO COM BANCO: {e}")
        raise e

# --- 3. INICIALIZAÇÃO DO BANCO ---
def init_db():
    logger.info("🔄 Verificando integridade da tabela 'bot_modo_ia'...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bot_modo_ia (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(50) NOT NULL UNIQUE,
                modo_ia VARCHAR(20) DEFAULT 'Ativado',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Banco de Dados verificado e pronto.")
    except Exception as e:
        logger.warning(f"⚠️ Aviso na inicialização do DB (pode ser temporário): {e}")

init_db()

# --- DECORATORS ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            logger.warning(f"⛔ Acesso negado: Usuário não logado tentou acessar {request.path}")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_key = request.headers.get('x-api-key') or request.args.get('api_key')
        if request_key and request_key == app.config['API_KEY']:
            return f(*args, **kwargs)
        
        logger.warning(f"⛔ API Key Inválida ou Ausente. IP: {request.remote_addr}")
        return jsonify({"error": "Acesso Negado", "message": "Chave de API invalida"}), 401
    return decorated_function

# --- ROTAS WEB ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == APP_PASSWORD:
            session['logged_in'] = True
            logger.info("🔓 Login realizado com sucesso (Painel Web)")
            return redirect(url_for('dashboard'))
        else:
            logger.warning("🔒 Tentativa de login com senha incorreta")
            error = 'Senha incorreta.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    logger.info("🔒 Logout realizado")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# --- ROTAS API ---

@app.route('/api/registros', methods=['GET'])
@api_key_required
def api_get_registros():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        telefone = request.args.get('telefone')

        if telefone:
            logger.info(f"📡 API GET /registros - Filtrando por: {telefone}")
            cur.execute("SELECT * FROM bot_modo_ia WHERE telefone = %s", (telefone,))
        else:
            logger.info("📡 API GET /registros - Buscando todos")
            cur.execute("SELECT * FROM bot_modo_ia ORDER BY id DESC")

        rows = cur.fetchall()
        registros = []
        for row in rows:
            registros.append({
                "id": row[0],
                "nome": row[1],
                "telefone": row[2],
                "modo_ia": row[3],
                "created_at": row[4],
                "updated_at": row[5]
            })
        cur.close()
        conn.close()
        return jsonify(registros)
    except Exception as e:
        logger.error(f"❌ Erro na API GET: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/registro', methods=['POST'])
@api_key_required
def api_create_registro():
    data = request.get_json()
    logger.info(f"📝 API POST /registro - Payload: {data}")
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO bot_modo_ia (nome, telefone, modo_ia) VALUES (%s, %s, %s) RETURNING id",
            (data.get('nome'), data.get('telefone'), data.get('modo_ia', 'Ativado'))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Registro criado com sucesso. ID: {new_id}")
        return jsonify({"message": "Criado com sucesso", "id": new_id}), 201
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Erro ao criar registro: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/registro/<int:id>', methods=['PUT'])
@api_key_required
def api_update_registro(id):
    data = request.get_json()
    logger.info(f"✏️ API PUT /registro/{id} - Payload: {data}")
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        fields = []
        values = []
        if 'modo_ia' in data:
            fields.append("modo_ia = %s")
            values.append(data['modo_ia'])
        if 'nome' in data:
            fields.append("nome = %s")
            values.append(data['nome'])

        if not fields:
             return jsonify({"message": "Nada para atualizar"}), 200

        values.append(id)
        query = "UPDATE bot_modo_ia SET " + ", ".join(fields) + " WHERE id = %s"
        
        cur.execute(query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Registro {id} atualizado com sucesso.")
        return jsonify({"message": "Atualizado com sucesso"})
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Erro ao atualizar registro {id}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/registro/<int:id>', methods=['DELETE'])
@api_key_required
def api_delete_registro(id):
    logger.info(f"🗑️ API DELETE /registro/{id}")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM bot_modo_ia WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"✅ Registro {id} deletado.")
        return jsonify({"message": "Deletado com sucesso"})
    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Erro ao deletar registro {id}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Se rodar direto (python app.py), ativa debug do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
