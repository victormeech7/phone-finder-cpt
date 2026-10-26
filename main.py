from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Live", "message": "Phone Finder CPT API is working!"}

@app.get("/search")
def search(q: str = "iPhone"):
    return {"query": q, "results": ["Test phone 1", "Test phone 2"], "source": "CPT"}