from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.chat import router as chat_router
import os

app = FastAPI(title="Egypt Tourism AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. تفعيل الـ API Routes أولاً
app.include_router(chat_router)

# 2. دالة صريحة لفتح ملف الـ HTML فوراً عند الدخول على الرابط الرئيسي
@app.get("/")
async def read_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "مجلد static أو ملف index.html غير موجود في مسار المشروع الأساسي!"}

# 3. خدمة الملفات الفرعية والأصول الثابتة داخل مجلد static
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static"), name="static")