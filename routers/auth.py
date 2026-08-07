from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import seguridad

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


# LOGIN: recibe un formulario usuario/contrasena y devuelve el token
@router.post("/login")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(
        datos.password, usuario["password"]
    ):
        raise HTTPException(status_code=401, detail="Usuario o contrasena incorrectos")
    token = seguridad.crear_token(usuario["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registro", status_code=201)
def registrar(datos: RegistroUsuario):

    # Verificar si el usuario ya existe
    if seguridad.buscar_usuario(datos.username):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    # Crear el nuevo usuario
    nuevo_usuario = {
        "username": datos.username,
        "nombre": datos.nombre,
        "password": seguridad.hashear_password(datos.password),
        "rol": "cliente",
    }

    # Guardar el usuario
    seguridad.usuarios.append(nuevo_usuario)

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "username": nuevo_usuario["username"],
            "nombre": nuevo_usuario["nombre"],
            "rol": nuevo_usuario["rol"],
        },
    }


# QUIEN SOY: endpoint protegido de ejemplo
@router.get("/yo")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {"username": usuario["username"], "rol": usuario["rol"]}


class RegistroUsuario(BaseModel):
    username: str
    nombre: str
    password: str
