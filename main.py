from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes, task_routes,user_routes
from dotenv import load_dotenv
import os

load_dotenv()

frontend_path = os.environ["FRONTEND_PATH"] | "http://localhost:3000"

app = FastAPI(
    title="Task App",  # ドキュメント上部のタイトル
    description="This is Task Management App",  # 説明
    version="1.0.0"
)

app.include_router(auth_routes.router)
app.include_router(task_routes.router)
app.include_router(user_routes.router)

# 許可するオリジン
origins = [
    "http://127.0.0.1:3000",
    frontend_path
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ここに許可するオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
