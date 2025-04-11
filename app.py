from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'banco.db'

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
    return render_template('novidades.html')

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
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO cadastros (nome, telefone, cpf, email) VALUES (?, ?, ?, ?)",
                           (nome, telefone, cpf, email))
            conn.commit()
            mensagem = "Cadastro realizado com sucesso!"
        except sqlite3.Error as e:
            mensagem = f"Erro ao cadastrar: {e}"
        finally:
            conn.close()
        return render_template('cadastro_resultado.html', mensagem=mensagem)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5500)