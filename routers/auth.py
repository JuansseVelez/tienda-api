from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import seguridad
import database

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


class RegistroUsuario(BaseModel):
    username: str
    nombre: str
    password: str


@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(
        datos.password, usuario["password_hash"]
    ):
        raise HTTPException(status_code=401, detail="Usuario o contrasena incorrectos")
    token = seguridad.crear_token(usuario["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registro", status_code=201)
def registrar(datos: RegistroUsuario):
    conexion = database.obtener_conexion()
    cursor = conexion.cursor()

    if seguridad.buscar_usuario(datos.username):
        conexion.close()
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    password_hash = seguridad.hashear_password(datos.password)

    cursor.execute(
        "INSERT INTO usuarios (username, nombre, password_hash, rol) VALUES (?, ?, ?, ?)",
        (datos.username, datos.nombre, password_hash, "cliente"),
    )
    conexion.commit()
    conexion.close()

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "username": datos.username,
            "nombre": datos.nombre,
            "rol": "cliente",
        },
    }


@router.get("/yo")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {"username": usuario["username"], "rol": usuario["rol"]}
