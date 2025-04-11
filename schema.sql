-- Cria a tabela cadastros
CREATE TABLE IF NOT EXISTS cadastros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    aniversario TEXT  -- Adicionando a coluna de aniversário (tipo TEXT para armazenar como 'YYYY-MM-DD')
);