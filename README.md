# API de la Tienda

Proyecto desarrollado con **FastAPI** como parte del curso de desarrollo de APIs del programa **Análisis y Desarrollo de Software (SENA)**.

La aplicación implementa un CRUD para productos y categorías, además de un sistema de autenticación y autorización utilizando JWT y roles de usuario.

---

# Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- Bcrypt
- PyJWT
- python-multipart

---

# Trabajo 1 - CRUD de la API

En el primer trabajo se desarrolló una API REST para administrar una tienda utilizando almacenamiento en memoria.

Se implementaron los siguientes recursos:

- Productos
- Categorías

Cada recurso cuenta con las operaciones CRUD:

- Crear
- Consultar
- Actualizar
- Eliminar

Los datos se almacenan temporalmente mientras la aplicación está en ejecución.

---

# Trabajo 2 - Autenticación y Autorización

En el segundo trabajo se agregó seguridad a la API mediante autenticación con JWT.

## Funcionalidades implementadas

- Registro de usuarios.
- Inicio de sesión.
- Hashing de contraseñas con Bcrypt.
- Generación de Tokens JWT.
- Validación de usuarios autenticados.
- Autorización mediante roles.

## Protección de Productos

| Método | Protección |
|---------|------------|
| GET | Público |
| GET por ID | Público |
| POST | Usuario autenticado |
| PUT | Usuario autenticado |
| DELETE | Solo administrador |

## Protección de Categorías

| Método | Protección |
|---------|------------|
| GET | Público |
| GET por ID | Público |
| POST | Usuario autenticado |
| PUT | Usuario autenticado |
| DELETE | Solo administrador |

---

# Usuarios de prueba

## Administrador

- Usuario: **admin**
- Contraseña: **admin123**

## Cliente

- Usuario: **ana**
- Contraseña: **ana123**

---

# Instalación del proyecto

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
```

Entrar a la carpeta del proyecto:

```bash
cd Tienda-Api
```

---

## 2. Crear el entorno virtual

Windows:

```bash
python -m venv venv
```

---

## 3. Activar el entorno virtual

Símbolo del sistema (CMD):

```bash
venv\Scripts\activate
```

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source venv/Scripts/activate
```

---

## 4. Instalar las dependencias

```bash
pip install fastapi
pip install uvicorn
pip install bcrypt
pip install PyJWT
pip install python-multipart
```

O también:

```bash
pip install fastapi uvicorn bcrypt PyJWT python-multipart
```

---

## 5. Ejecutar la API

```bash
python -m uvicorn main:app --reload
```

Si utilizas el entorno virtual directamente:

```bash
./venv/Scripts/python.exe -m uvicorn main:app --reload
```

---

## 6. Abrir la documentación

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Documentación ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Autenticación

Para utilizar los endpoints protegidos:

1. Abrir `/docs`.
2. Presionar **Authorize**.
3. Iniciar sesión con un usuario registrado.
4. Swagger obtendrá automáticamente el token JWT.
5. Ya se podrán consumir los endpoints protegidos.

---

# Autor

**Juan Sebastián Ramírez**

Tecnólogo en Análisis y Desarrollo de Software

SENA
