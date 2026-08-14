from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad
import database
import sqlite3

router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str


@router.get("")
def listar_categorias():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM categorias")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
    categoria = cursor.fetchone()
    conexion.close()

    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return dict(categoria)


@router.post("", status_code=201)
def crear_categoria(
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO categorias (nombre) VALUES (?)",
            (datos.nombre,),
        )
        conexion.commit()
    except sqlite3.IntegrityError:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="Ya existe una categoria con ese nombre"
        )

    nuevo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (nuevo_id,))
    nueva = dict(cursor.fetchone())
    conexion.close()

    return {
        "mensaje": "Categoria creada",
        "categoria": nueva,
        "creado_por": usuario["username"],
    }


@router.put("/{categoria_id}")
def actualizar_categoria(
    categoria_id: int,
    datos: CategoriaEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "UPDATE categorias SET nombre = ? WHERE id = ?",
            (datos.nombre, categoria_id),
        )
        conexion.commit()
    except sqlite3.IntegrityError:
        conexion.close()
        raise HTTPException(
            status_code=400, detail="Ya existe una categoria con ese nombre"
        )

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
    actualizada = dict(cursor.fetchone())
    conexion.close()

    return {
        "mensaje": "Categoria actualizada",
        "categoria": actualizada,
        "actualizado_por": usuario["username"],
    }


@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    cursor.execute(
        "SELECT COUNT(*) FROM productos WHERE categoria_id = ?", (categoria_id,)
    )
    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos > 0:
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar: la categoria tiene {cantidad_productos} producto(s) asociado(s)",
        )

    cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Categoria eliminada",
        "categoria": dict(categoria),
        "eliminado_por": admin["username"],
    }


@router.get("/{categoria_id}/productos")
def obtener_categoria_con_productos(categoria_id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
    categoria = cursor.fetchone()

    if categoria is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    cursor.execute(
        """
        SELECT productos.* FROM productos
        JOIN categorias ON productos.categoria_id = categorias.id
        WHERE categorias.id = ?
        """,
        (categoria_id,),
    )
    productos = [dict(fila) for fila in cursor.fetchall()]
    conexion.close()

    return {
        "id": categoria["id"],
        "nombre": categoria["nombre"],
        "productos": productos,
    }
