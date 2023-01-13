from src.adapters.web_server.controller.Dados_FastAPI import app
# consumir do OCR e treinar com um contrato real
# authocraudicon
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app"
    )