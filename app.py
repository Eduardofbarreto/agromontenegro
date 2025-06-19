import os
from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2 # Importa o driver PostgreSQL
from psycopg2 import extras # Para acessar resultados como dicionários (Rows)
import logging
from dotenv import load_dotenv # Para carregar variáveis de ambiente

# Carrega variáveis de ambiente do arquivo .env
# Isso deve ser feito logo no início do script para que as variáveis estejam disponíveis
load_dotenv()

app = Flask(__name__, template_folder='templates')
# A SECRET_KEY é crucial para segurança do Flask (sessões, flash messages, etc.)
# Pega do .env ou usa um valor padrão se não encontrar (para desenvolvimento)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'sua_chave_secreta_padrao_e_forte_aqui')


# Configurações do banco de dados PostgreSQL carregadas do .env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'agroferragem') # Nome do seu DB no Postgres: 'agroferragem'
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root') # Sua senha do PostgreSQL
DB_PORT = os.getenv('DB_PORT', '5432') # Porta padrão do PostgreSQL

# Configuração de logging para ver mensagens no terminal do servidor
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Função para obter conexão com o banco de dados PostgreSQL
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        # Permite acessar os resultados da consulta por nome da coluna (como dicionários)
        conn.cursor_factory = extras.RealDictCursor
        logging.info("Conexão com o PostgreSQL estabelecida com sucesso.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
        # flash("Erro interno do servidor: Não foi possível conectar ao banco de dados.", "error")
        return None # Retorna None para indicar falha na conexão


# --- Rotas do Site ---

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

# Rota para exibir o formulário de cadastro (GET)
@app.route('/cadastro', methods=['GET'])
def exibir_formulario_cadastro():
    # Renderiza a página principal que contém o formulário de cadastro
    return render_template('index.html')

# Rota para processar o cadastro (POST)
@app.route('/cadastro', methods=['POST'])
def cadastrar(): # <-- O endpoint para url_for('cadastrar')
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        aniversario_dia = request.form.get('aniversario_dia')
        aniversario_mes = request.form.get('aniversario_mes')

        # Validação básica dos campos obrigatórios
        if not all([nome, telefone, cpf, email]):
            flash("Por favor, preencha todos os campos obrigatórios: Nome, Telefone, CPF e Email.", "error")
            return redirect(url_for('index'))

        conn = get_db_connection()
        if conn is None:
            # A mensagem de erro de conexão já foi logada/tratada em get_db_connection
            flash("Erro ao conectar com o banco de dados. Tente novamente mais tarde.", "error")
            return redirect(url_for('index'))

        try:
            cursor = conn.cursor()
            # SQL para inserir dados no PostgreSQL usando placeholders %s
            sql = """
                INSERT INTO cadastros (nome, telefone, cpf, email, aniversario_dia, aniversario_mes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nome, telefone, cpf, email, aniversario_dia, aniversario_mes))
            conn.commit() # Confirma a transação no banco de dados
            flash("Pessoa cadastrada com sucesso!", "success") # Mensagem de sucesso
            logging.info(f"Novo cadastro: {email} - {cpf}")

        except psycopg2.IntegrityError as e:
            conn.rollback() # Desfaz a transação em caso de erro
            logging.error(f"Erro de integridade ao cadastrar: {e}")
            # Códigos de erro SQLSTATE para integridade (23505 é violação de unicidade)
            if "23505" in str(e):
                if "cadastros_email_key" in str(e) or "email" in str(e).lower():
                    flash(f"Erro: O email '{email}' já está cadastrado.", "error")
                elif "cadastros_cpf_key" in str(e) or "cpf" in str(e).lower():
                    flash(f"Erro: O CPF '{cpf}' já está cadastrado.", "error")
                else:
                    flash(f"Erro de dados duplicados: {e}", "error")
            else:
                flash(f"Erro de banco de dados: {e}", "error")

        except Exception as e:
            conn.rollback() # Desfaz a transação em caso de qualquer outro erro
            logging.error(f"Ocorreu um erro inesperado: {e}")
            flash(f"Ocorreu um erro inesperado ao cadastrar: {e}", "error")
        finally:
            if conn: # Garante que a conexão seja fechada
                cursor.close()
                conn.close()
                logging.info("Conexão com o PostgreSQL fechada.")

        return redirect(url_for('index')) # Redireciona de volta para a página inicial


if __name__ == '__main__':
    # No PostgreSQL, você deve criar seu banco de dados e a tabela 'cadastros'
    # diretamente no sistema do PostgreSQL (ex: via pgAdmin ou terminal SQL).
    # Este app.py só vai se conectar a um DB e tabela já existentes.
    app.run(debug=True, port=5001) # Mantém a porta 5500 para desenvolvimento