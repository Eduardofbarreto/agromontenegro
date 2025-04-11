from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import logging
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_cliente' # Redireciona para a página de login do cliente

class Cliente(UserMixin):
    def __init__(self, id, email, cpf):
        self.id = id
        self.email = email
        self.cpf = cpf

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, cpf FROM cadastros WHERE id = ?", (user_id,))
    cliente_data = cursor.fetchone()
    conn.close()
    if cliente_data:
        return Cliente(cliente_data['id'], cliente_data['email'], cliente_data['cpf'])
    return None

@app.route('/login-cliente', methods=['GET', 'POST'])
def login_cliente():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    error = None
    if request.method == 'POST':
        identificador = request.form['identificador']
        senha = request.form['senha']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, cpf, senha FROM cadastros WHERE email = ? OR cpf = ?", (identificador, identificador))
        cliente_data = cursor.fetchone()
        conn.close()

        if cliente_data and check_password_hash(cliente_data['senha'], senha):
            cliente = Cliente(cliente_data['id'], cliente_data['email'], cliente_data['cpf'])
            login_user(cliente)
            return redirect(url_for('cliente_area'))
        else:
            error = 'Email/CPF ou senha incorretos'

    return render_template('login_cliente.html', error=error)

@app.route('/cliente-area')
@login_required
def cliente_area():
    return render_template('cliente_area.html', cliente=current_user)

@app.route('/logout-cliente')
@login_required
def logout_cliente():
    logout_user()
    return redirect(url_for('index'))

DATABASE = 'banco.db'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/racoes-e-pets')
def racoes_e_pets():
    return render_template('racoes-e-pets.html')

@app.route('/sementes')
def sementes():
    return render_template('sementes.html')

@app.route('/ferragem')
def ferragem():
    return render_template('ferragem.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/novidades')
def novidades():
    return render_template('novidades-ofertas.html')

@app.route('/cadastro', methods=['GET'])
def exibir_formulario_cadastro():
    """Exibe o formulário de cadastro."""
    return render_template('cadastro_form.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar():
    """Processa os dados do formulário de cadastro."""
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        email = request.form['email']
        aniversario = request.form['aniversario']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)

        conn = get_db()
        cursor = conn.cursor()
        mensagem = ""
        try:
            sql = "INSERT INTO cadastros (nome, telefone, cpf, email, aniversario, senha) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (nome, telefone, cpf, email, aniversario, senha_hash))
            conn.commit()
            mensagem = "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError as e:
            conn.rollback()
            mensagem = f"Erro ao cadastrar: {e}"
        finally:
            conn.close()
        return render_template('cadastro_resultado.html', mensagem=mensagem)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5500)