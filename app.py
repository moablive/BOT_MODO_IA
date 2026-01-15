import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY', 'chave_padrao_insegura')
app.config['API_KEY'] = os.getenv('API_SECRET_KEY')

# Configuração do Banco
DB_HOST = "awlsrvDB_postgres"
DB_NAME = "postgres"
DB_USER = "admin_root"
DB_PASS = os.getenv('DB_ROOT_PASSWORD')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# --- DECORATORS (Segurança) ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica no Header (padrão) ou na URL (?api_key=...)
        request_key = request.headers.get('x-api-key') or request.args.get('api_key')
        
        if request_key and request_key == app.config['API_KEY']:
            return f(*args, **kwargs)
        
        return jsonify({"error": "Acesso Negado", "message": "Chave de API invalida ou ausente"}), 401
    return decorated_function

# --- ROTAS WEB (Navegador) ---

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == os.getenv('APP_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Senha incorreta.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# --- ROTAS API (Protegidas por API Key) ---

@app.route('/api/registros', methods=['GET'])
@api_key_required
def api_get_registros():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Filtro opcional por telefone via query param
        telefone = request.args.get('telefone')
        
        if telefone:
            cur.execute("SELECT * FROM BOT_MODO_IA WHERE telefone = %s", (telefone,))
        else:
            cur.execute("SELECT * FROM BOT_MODO_IA ORDER BY id DESC")
            
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
        return jsonify({"error": str(e)}), 500

@app.route('/api/registro', methods=['POST'])
@api_key_required
def api_create_registro():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO BOT_MODO_IA (nome, telefone, modo_ia) VALUES (%s, %s, %s) RETURNING id",
            (data['nome'], data['telefone'], data['modo_ia'])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Criado com sucesso", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/registro/<int:id>', methods=['PUT'])
@api_key_required
def api_update_registro(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    # Atualiza apenas o que foi enviado
    fields = []
    values = []
    if 'modo_ia' in data:
        fields.append("modo_ia = %s")
        values.append(data['modo_ia'])
    if 'nome' in data:
        fields.append("nome = %s")
        values.append(data['nome'])
        
    values.append(id) # ID para o WHERE
    
    query = "UPDATE BOT_MODO_IA SET " + ", ".join(fields) + " WHERE id = %s"
    
    cur.execute(query, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Atualizado com sucesso"})

@app.route('/api/registro/<int:id>', methods=['DELETE'])
@api_key_required
def api_delete_registro(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM BOT_MODO_IA WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deletado com sucesso"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
