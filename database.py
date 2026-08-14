import sqlite3

NOMBRE_DB = "tienda-api.db"


def obtener_conexion():
    conexion = sqlite3.connect(NOMBRE_DB, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'cliente'
    )
    """)

    conexion.commit()
    conexion.close()


def sembrar_datos():
    import bcrypt

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        admin_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        ana_hash = bcrypt.hashpw("ana123".encode(), bcrypt.gensalt()).decode()
        cursor.executemany(
            "INSERT INTO usuarios (username, nombre, password_hash, rol) VALUES (?, ?, ?, ?)",
            [
                ("admin", "Administrador", admin_hash, "admin"),
                ("ana", "Ana Cliente", ana_hash, "cliente"),
            ],
        )

    cursor.execute("SELECT COUNT(*) FROM categorias")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO categorias (nombre) VALUES (?)",
            [("Perifericos",), ("Pantallas",), ("Audio",)],
        )

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria_id) VALUES (?, ?, ?)",
            [
                ("Teclado mecanico", 120000, 1),
                ("Mouse gamer", 85000, 1),
                ("Monitor 24", 650000, 2),
            ],
        )

    conexion.commit()
    conexion.close()
