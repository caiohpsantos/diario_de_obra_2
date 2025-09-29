import sqlite3

db = sqlite3.connect("db.sqlite3")

cursor = db.cursor()

cursor.execute("""CREATE TABLE produtos_produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    descricao VARCHAR(200) NOT NULL UNIQUE,
    qtde_caixa INTEGER NULL,
    foto_produto VARCHAR(100) NOT NULL,  -- Armazena o caminho da imagem
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias_produtos(id) ON DELETE NO ACTION
);
""")