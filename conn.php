<?php

require_once 'vendor/autoload.php'; // Se estiver usando Composer

use Flask\Response;
use Flask\Request;
use Flask\Templating\Environment;
use Flask\Templating\Loader\FilesystemLoader;

$app = new Flask(__DIR__);
$app->config['SECRET_KEY'] = 'sua_chave_secreta_aqui';
$app->template_folder = 'templates';

// Configuração do Twig (se estiver usando)
$loader = new FilesystemLoader($app->template_folder);
$twig = new Environment($loader);

$database = 'banco.db';

function get_db(): SQLite3
{
    global $database;
    return new SQLite3($database);
}

function init_db(): void
{
    global $app, $database;
    $db = get_db();
    $sql = file_get_contents('schema.sql');
    $db->exec($sql);
    $db->close();
}

$app->route('/', function () use ($twig): Response {
    return new Response($twig->render('index.html'));
});

$app->route('/racoes-e-pets', function () use ($twig): Response {
    return new Response($twig->render('racoes-e-pets.html'));
});

$app->route('/sementes', function () use ($twig): Response {
    return new Response($twig->render('sementes.html'));
});

$app->route('/ferragem', function () use ($twig): Response {
    return new Response($twig->render('ferragem.html'));
});

$app->route('/contato', function () use ($twig): Response {
    return new Response($twig->render('contato.html'));
});

$app->route('/novidades', function () use ($twig): Response {
    return new Response($twig->render('novidades-ofertas.html'));
});

$app->route('/cadastro', function () use ($twig): Response {
    /**
     * Exibe o formulário de cadastro.
     */
    return new Response($twig->render('cadastro_form.html'));
}, methods: ['GET']);

$app->route('/cadastro', function (Request $request) use ($twig): Response {
    /**
     * Processa os dados do formulário de cadastro.
     */
    if ($request->getMethod() === 'POST') {
        $nome = $request->get('nome');
        $telefone = $request->get('telefone');
        $cpf = $request->get('cpf');
        $email = $request->get('email');
        $aniversario_dia = $request->get('aniversario_dia');
        $aniversario_mes = $request->get('aniversario_mes');

        $db = get_db();
        $mensagem = "";
        try {
            $stmt = $db->prepare("INSERT INTO cadastros (nome, telefone, cpf, email, aniversario_dia, aniversario_mes) VALUES (:nome, :telefone, :cpf, :email, :aniversario_dia, :aniversario_mes)");
            $stmt->bindValue(':nome', $nome, SQLITE3_TEXT);
            $stmt->bindValue(':telefone', $telefone, SQLITE3_TEXT);
            $stmt->bindValue(':cpf', $cpf, SQLITE3_TEXT);
            $stmt->bindValue(':email', $email, SQLITE3_TEXT);
            $stmt->bindValue(':aniversario_dia', $aniversario_dia, SQLITE3_TEXT);
            $stmt->bindValue(':aniversario_mes', $aniversario_mes, SQLITE3_TEXT);
            $result = $stmt->execute();

            if ($result) {
                $mensagem = "Cadastro realizado com sucesso!";
            } else {
                $mensagem = "Erro ao cadastrar.";
            }
        } catch (SQLite3Exception $e) {
            $mensagem = "Erro ao cadastrar: " . $e->getMessage();
        } finally {
            $db->close();
        }
        return new Response($twig->render('cadastro_resultado.html', [
            'mensagem' => $mensagem,
            'aniversario_dia' => $aniversario_dia,
            'aniversario_mes' => $aniversario_mes,
        ]));
    }
    // Se não for POST, redireciona para o formulário (opcional)
    return new Response($twig->render('cadastro_form.html'));
}, methods: ['POST']);

// Inicializar o banco de dados se não existir
if (!file_exists($database)) {
    init_db();
}

$app->run(port: 5500, debug: true);

?>
