from fastapi import FastAPI
app = FastAPI(title="Social Media Studio")
@app.get("/health")
def health():
    return {"status": "ok"}
