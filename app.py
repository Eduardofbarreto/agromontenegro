from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'cadastros.db'

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

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
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
    app.run(debug=True)
