<?php

// Caminho para o seu arquivo de banco de dados SQLite
$databasePath = '/opt/lampp/htdocs/agromontenegro/banco.db';

try {
    // Conectar ao banco de dados SQLite
    $pdo = new PDO("sqlite:" . $databasePath);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Criar a tabela 'cadastros' se ela não existir
    $pdo->exec("CREATE TABLE IF NOT EXISTS cadastros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE
    )");

    // Verificar se o formulário foi enviado
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Obter os dados do formulário
        $nome = $_POST['nome'];
        $telefone = $_POST['telefone'];
        $cpf = $_POST['cpf'];
        $email = $_POST['email'];

        // Preparar a instrução SQL para inserção
        $stmt = $pdo->prepare("INSERT INTO cadastros (nome, telefone, cpf, email) VALUES (:nome, :telefone, :cpf, :email)");
       

        // Vincular os parâmetros
        $stmt->bindParam(':nome', $nome);
        $stmt->bindParam(':telefone', $telefone);
        $stmt->bindParam(':cpf', $cpf);
        $stmt->bindParam(':email', $email);

        // Executar a instrução SQL
        if ($stmt->execute()) {
            echo "<p>Cadastro realizado com sucesso!</p>";
            echo "<p><a href='contato.php'>Voltar para Contato</a></p>"; // Ajuste o link conforme necessário
        } else {
            echo "<p>Erro ao cadastrar:</p>";
            echo "<pre>";
            print_r($stmt->errorInfo());
            echo "</pre>";
            echo "<p><a href='contato.php'>Voltar para Contato</a></p>"; // Ajuste o link conforme necessário
        }
    } else {
        // Se o formulário não foi enviado, você pode exibir uma mensagem ou redirecionar
        echo "<p>Nenhum dado de formulário recebido.</p>";
        echo "<p><a href='contato.php'>Voltar para Contato</a></p>"; // Ajuste o link conforme necessário
    }

} catch (PDOException $e) {
    echo "<p>Erro de conexão com o banco de dados: " . $e->getMessage() . "</p>";
    echo "<p><a href='contato.php'>Voltar para Contato</a></p>"; // Ajuste o link conforme necessário
}

?>