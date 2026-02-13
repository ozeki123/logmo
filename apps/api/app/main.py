from fastapi import FastAPI

app = FastAPI(title="Logmo API")

@app.get("/")
def root():
    return {"name": "logmo-api", "status": "ok"}
@app.get("/health")
def health():
    return {"status": "ok"}
