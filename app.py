from fastapi import FastAPI
from routes.api import router as api_router
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis do arquivo .env

app = FastAPI(title="Sistema de Recomendação de Energia Solar")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

