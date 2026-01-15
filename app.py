import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')
APP_PASSWORD = os.getenv('APP_PASSWORD', 'admin')

def get_db():
    try:
        return psycopg2.connect(
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    except: return None

def init_db():
    conn = get_db()
    if conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS BOT_MODO_IA (id SERIAL PRIMARY KEY, nome VARCHAR(255) NOT NULL, telefone VARCHAR(20) NOT NULL, modo_ia VARCHAR(100) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        conn.close()
        print("DB Check OK")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session: return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index(): return redirect(url_for('dashboard')) if 'logged_in' in session else redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        flash('Senha incorreta!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard(): return render_template('index.html')

@app.route('/api/registros', methods=['GET'])
@login_required
def get_registros():
    conn = get_db()
    if not conn: return jsonify({'error': 'DB Error'}), 500
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM BOT_MODO_IA ORDER BY id DESC")
    res = cur.fetchall()
    conn.close()
    return jsonify(res)

@app.route('/api/registro', methods=['POST'])
@login_required
def create():
    d = request.json
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO BOT_MODO_IA (nome, telefone, modo_ia) VALUES (%s, %s, %s)", (d['nome'], d['telefone'], d['modo_ia']))
        conn.commit()
        return jsonify({'msg': 'OK'}), 201
    except Exception as e: return jsonify({'error': str(e)}), 500
    finally: conn.close()

@app.route('/api/registro/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def modify(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        if request.method == 'PUT':
            d = request.json
            cur.execute("UPDATE BOT_MODO_IA SET nome=%s, telefone=%s, modo_ia=%s WHERE id=%s", (d['nome'], d['telefone'], d['modo_ia'], id))
        else:
            cur.execute("DELETE FROM BOT_MODO_IA WHERE id=%s", (id,))
        conn.commit()
        return jsonify({'msg': 'OK'})
    except Exception as e: return jsonify({'error': str(e)}), 500
    finally: conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
