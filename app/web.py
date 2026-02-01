from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/")
async def root():
    return {"service": "NoFAT API", "status": "running"}
