from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import auth, productos, categorias
import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.crear_tablas()
    database.sembrar_datos()
    yield


app = FastAPI(title="API de la Tienda", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
