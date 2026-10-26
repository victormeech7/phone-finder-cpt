from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FRONTEND ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Phone Finder CPT</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 40px; }
            input { padding: 15px; width: 300px; border-radius: 10px; border: none; font-size: 16px; }
            button { padding: 15px 25px; border-radius: 10px; border: none; background: #00ff88; font-weight: bold; cursor: pointer; margin-left: 10px; }
            .card { background: #1e1e1e; padding: 20px; margin: 15px auto; max-width: 500px; border-radius: 15px; text-align: left; }
            .price { color: #00ff88; font-weight: bold; font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>📱 Phone Finder CPT</h1>
        <p>Find cheapest phones in Cape Town</p>
        <input id="q" placeholder="e.g. iPhone 14, Samsung A54" value="iPhone" />
        <button onclick="search()">Search</button>
        <div id="results"></div>
        <script>
            async function search() {
                const q = document.getElementById('q').value;
                document.getElementById('results').innerHTML = '<p>Searching...</p>';
                const res = await fetch('/search?q=' + q);
                const data = await res.json();
                let html = '<h3>Results for ' + data.query + '</h3>';
                data.results.forEach(r => {
                    html += `<div class="card"><b>${r.name}</b><br><span class="price">${r.price}</span><br><small>${r.shop} - ${r.location}</small></div>`;
                });
                document.getElementById('results').innerHTML = html;
            }
            search();
        </script>
    </body>
    </html>
    """

# --- BACKEND SEARCH (Realistic data + ready for real scraping) ---
@app.get("/search")
def search(q: str = "iPhone"):
    # TODO: Replace this with real scraping from Takealot, PriceCheck etc
    # For now we return realistic CPT shops - Day 6 we add live scraping
    q_lower = q.lower()
    
    mock_db = [
        {"name": f"{q} 128GB - Excellent", "price": "R 8,499", "shop": "Cash Crusaders", "location": "Cavendish"},
        {"name": f"{q} 64GB - Good Cond", "price": "R 6,200", "shop": "Cash Converters", "location": "Bellville"},
        {"name": f"{q} Brand New Sealed", "price": "R 12,999", "shop": "Takealot / Incredible", "location": "CPT Online"},
        {"name": f"{q} Second Hand", "price": "R 5,500", "shop": "Facebook Marketplace", "location": "Claremont"},
    ]
    
    return {"query": q, "results": mock_db, "source": "CPT Live"}

@app.get("/health")
def health():
    return {"status": "Live Day 5"}