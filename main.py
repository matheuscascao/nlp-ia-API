from src.adapters.web_server.controller.Dados_FastAPI import app
#teste
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app"
    )