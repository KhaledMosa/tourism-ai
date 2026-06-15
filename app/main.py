from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.scan import router as scan_router
from app.routes.chat import router as chat_router

app = FastAPI(title="Egypt Tourism AI Guide")

app.include_router(scan_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")