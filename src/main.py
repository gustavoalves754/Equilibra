from fastapi import FastAPI

app = FastAPI(
    title="API Equilibra",
    description="Backend para gestão de planos alimentares e saúde.",
    version="1.0.0"
)

@app.get("/", tags=["Base"])
def root():
    return {"mensagem": "A API do Equilibra está online."}

@app.get("/health", tags=["Base"])
def health_check():
    return {"status": "ok", "servico": "equilibra-api"}