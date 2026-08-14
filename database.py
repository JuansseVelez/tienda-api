# database.py
import sqlite3

NOMBRE_DB = "tienda.db"


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
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'cliente'
    )
    """)

    conexion.commit()
    conexion.close()
