CREATE TABLE IF NOT EXISTS cadastros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    cpf TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    aniversario TEXT,
    senha TEXT NOT NULL -- Adicionando a coluna para a senha
);