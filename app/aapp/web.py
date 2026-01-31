import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

def get_port() -> int:
    return int(os.getenv("PORT", "8080"))
