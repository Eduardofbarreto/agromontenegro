import os
from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2
from psycopg2 import extras
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
# Isso deve ser feito logo no início do script para que as variáveis estejam disponíveis
load_dotenv()

app = Flask(__name__, template_folder='templates')
# A SECRET_KEY é crucial para segurança do Flask (sessões, flash messages, etc.)
# Pega do .env ou usa um valor padrão se não encontrar (para desenvolvimento)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'sua_chave_secreta_padrao_e_forte_aqui') # Lembre-se de mudar isso no seu .env!


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
        return None


# --- Rotas do Site ---

@app.route('/')
def index():
    # A página inicial pode conter o formulário de cadastro, por isso o redirecionamento de cadastro GET vai para ela.
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
    # Esta página pode ser o destino de redirecionamento em caso de erro no cadastro,
    # então é importante que ela exiba as mensagens flash.
    return render_template('contato.html')

@app.route('/novidades')
def novidades():
    return render_template('novidades-ofertas.html')

# Rota para exibir o formulário de cadastro (GET)
# Esta rota simplesmente mostra a página com o formulário.
# As mensagens flash (se houver alguma de uma submissão anterior) serão exibidas.
@app.route('/cadastro', methods=['GET'])
def exibir_formulario_cadastro():
    # Renderiza a página principal que contém o formulário de cadastro
    return render_template('index.html')

# Rota para processar o cadastro (POST)
@app.route('/cadastro', methods=['POST'])
def cadastrar():
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
            return redirect(url_for('contato')) # Redireciona para contato para exibir a mensagem de erro

        conn = get_db_connection()
        if conn is None:
            flash("Erro ao conectar com o banco de dados. Tente novamente mais tarde.", "error")
            return redirect(url_for('contato')) # Redireciona para contato para exibir a mensagem de erro

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

            # --- REDIRECIONA PARA A PÁGINA DE SUCESSO, PASSANDO O NOME E ANIVERSÁRIO NA URL ---
            return redirect(url_for('cadastro_resultado', nome_usuario=nome,
                                     aniversario_dia=aniversario_dia,
                                     aniversario_mes=aniversario_mes))

        except psycopg2.IntegrityError as e:
            conn.rollback() # Desfaz a transação em caso de erro
            logging.error(f"Erro de integridade ao cadastrar: {e}")
            if "23505" in str(e): # Código de erro para violação de unicidade
                if "cadastros_email_key" in str(e) or "email" in str(e).lower():
                    flash(f"Erro: O email '{email}' já está cadastrado.", "error")
                elif "cadastros_cpf_key" in str(e) or "cpf" in str(e).lower():
                    flash(f"Erro: O CPF '{cpf}' já está cadastrado.", "error")
                else:
                    flash(f"Erro de dados duplicados: {e}", "error")
            else:
                flash(f"Erro de banco de dados: {e}", "error")
            return redirect(url_for('contato')) # Redireciona para a página de contato em caso de erro (com a mensagem flash)

        except Exception as e:
            conn.rollback() # Desfaz a transação em caso de qualquer outro erro
            logging.error(f"Ocorreu um erro inesperado: {e}")
            flash(f"Ocorreu um erro inesperado ao cadastrar: {e}", "error")
            return redirect(url_for('contato')) # Redireciona para a página de contato em caso de erro (com a mensagem flash)
        finally:
            if conn: # Garante que a conexão seja fechada
                cursor.close()
                conn.close()
                logging.info("Conexão com o PostgreSQL fechada.")
    
    # Se o método não for POST (o que não deveria acontecer aqui, mas por segurança), redireciona para o contato.
    return redirect(url_for('contato'))

# --- ROTA PARA A PÁGINA DE RESULTADO DO CADASTRO (recebe o nome e aniversário da URL) ---
@app.route('/cadastro_resultado')
def cadastro_resultado():
    nome_usuario = request.args.get('nome_usuario', 'Visitante') # Pega o nome da URL, padrão 'Visitante'
    aniversario_dia = request.args.get('aniversario_dia')
    aniversario_mes = request.args.get('aniversario_mes')
    # A página de resultado também deve exibir mensagens flash, caso venha de um erro
    return render_template('cadastro_resultado.html',
                           nome=nome_usuario,
                           aniversario_dia=aniversario_dia,
                           aniversario_mes=aniversario_mes)


if __name__ == '__main__':
    # No PostgreSQL, você deve criar seu banco de dados e a tabela 'cadastros'
    # diretamente no sistema do PostgreSQL (ex: via pgAdmin ou terminal SQL).
    # Este app.py só vai se conectar a um DB e tabela já existentes.
    app.run(debug=True, port=5001)