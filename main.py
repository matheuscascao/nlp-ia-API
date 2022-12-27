from src.adapters.web_server.controller.Dados_FastAPI import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app"
    )