from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad
import database

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


@router.get("")
def listar_productos():
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()
    conexion.close()

    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return dict(producto)


@router.post("", status_code=201)
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM categorias WHERE id = ?", (datos.categoria_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(status_code=400, detail="La categoria indicada no existe")

    cursor.execute(
        "INSERT INTO productos (nombre, precio, categoria_id) VALUES (?, ?, ?)",
        (datos.nombre, datos.precio, datos.categoria_id),
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid

    cursor.execute("SELECT * FROM productos WHERE id = ?", (nuevo_id,))
    nuevo = dict(cursor.fetchone())
    conexion.close()

    return {
        "mensaje": "Producto creado",
        "producto": nuevo,
        "creado_por": usuario["username"],
    }


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, categoria_id = ? WHERE id = ?",
        (datos.nombre, datos.precio, datos.categoria_id, producto_id),
    )
    conexion.commit()

    if cursor.rowcount == 0:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    actualizado = dict(cursor.fetchone())
    conexion.close()

    return {
        "mensaje": "Producto actualizado",
        "producto": actualizado,
        "actualizado_por": usuario["username"],
    }


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    admin: dict = Depends(seguridad.requerir_admin),
):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Producto eliminado",
        "producto": dict(producto),
        "eliminado_por": admin["username"],
    }
