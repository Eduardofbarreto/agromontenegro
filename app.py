from flask import Flask, request, render_template
import sqlite3
import logging

app = Flask(__name__)
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
        aniversario = request.form['aniversario']  # Obtém a data de aniversário do formulário

        conn = get_db()
        cursor = conn.cursor()
        mensagem = ""
        try:
            logging.debug(f"Dados recebidos do formulário: Nome={nome}, Telefone={telefone}, CPF={cpf}, Email={email}, Aniversario={aniversario}")
            sql = "INSERT INTO cadastros (nome, telefone, cpf, email, aniversario) VALUES (?, ?, ?, ?, ?)"  # Inclui a coluna aniversario
            logging.debug(f"Query SQL a ser executada: {sql}, com os valores: {(nome, telefone, cpf, email, aniversario)}")
            cursor.execute(sql, (nome, telefone, cpf, email, aniversario))
            conn.commit()
            logging.info(f"Cadastro realizado e commitado com sucesso para o email: {email} com aniversário: {aniversario}")
            # --- Bloco de teste para verificar os dados ---
            cursor.execute("SELECT * FROM cadastros WHERE email = ?", (email,))
            resultados = cursor.fetchall()
            logging.debug(f"Resultados do SELECT após o INSERT para o email {email}: {resultados}")
            # --- Fim do bloco de teste ---
            mensagem = "Cadastro realizado com sucesso!"
        except sqlite3.IntegrityError as e:
            conn.rollback()
            mensagem = f"Erro ao cadastrar (IntegrityError): {e}"
            logging.error(f"Erro de integridade ao cadastrar o email {email}: {e}")
        except sqlite3.Error as e:
            conn.rollback()
            mensagem = f"Erro ao cadastrar (Outro erro SQLite): {e}"
            logging.error(f"Erro ao cadastrar o email {email}: {e}")
        finally:
            conn.close()
        return render_template('cadastro_resultado.html', mensagem=mensagem, aniversario=aniversario)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5500)