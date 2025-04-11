CREATE TABLE IF NOT EXISTS cadastros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    cpf TEXT UNIQUE NOT NULL,
    email TEXT, -- Alterado para TEXT (permite NULL por padrão em SQLite)
    aniversario_dia INTEGER, -- Nova coluna para o dia
    aniversario_mes INTEGER -- Nova coluna para o mês
    -- REMOVIDO: senha TEXT NOT NULL
);