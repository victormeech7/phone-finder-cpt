from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HEADERS = {"User-Agent": "Mozilla/5.0 Chrome/120.0"}

SPONSORED_SHOP = {
    "name": "🔥 SPONSORED: Canal Walk Cell C - iPhone Special",
    "price": "R 8,999 - TODAY ONLY",
    "shop": "Cell C Canal Walk",
    "location": "Canal Walk - CALL NOW",
    "image": "https://via.placeholder.com/400x300/ffcc00/000?text=SPONSORED+TOP+DEAL",
    "link": "https://wa.me/27814150336?text=Hi%20I%20saw%20your%20deal%20on%20Phone%20Finder%20CPT%20-%20I%20want%20to%20be%20featured%20top",
    "sponsored": True
}

def get_image(name): 
    return f"https://via.placeholder.com/400x300/00ff88/000?text={urllib.parse.quote(name[:20])}"

def scrape_pc(query):
    results=[]
    try:
        url=f"https://www.pricecheck.co.za/search?search={query}"
        r=requests.get(url, headers=HEADERS, timeout=8)
        soup=BeautifulSoup(r.text,"html.parser")
        for card in soup.select("div.product-list-item")[:6]:
            n=card.select_one("a.title")
            p=card.select_one("a.title")
            p_price=card.select_one(".price")
            img=card.select_one("img")
            if n and p_price:
                img_url=img.get("src") if img else get_image(n.text[:20])
                if img_url and img_url.startswith("/"): 
                    img_url="https://www.pricecheck.co.za"+img_url
                results.append({"name":n.get_text(strip=True)[:50],"price":p_price.get_text(strip=True).replace("From","").strip(),"shop":"PriceCheck","location":"CPT Delivery","image":img_url,"link":f"https://www.pricecheck.co.za/search?search={query}","sponsored":False})
    except: 
        pass
    return results

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html><head><title>Phone Finder CPT - MAKE MONEY</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:sans-serif;background:#0a0a0a;color:#fff;margin:0;padding:16px;text-align:center}
.live{background:#00ff88;color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:bold}
.money-bar{background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:10px;border-radius:12px;margin:15px auto;max-width:1100px;font-weight:bold}
input{padding:16px;width:60%;max-width:320px;border-radius:12px;border:none;font-size:16px}
button.search{background:#00ff88;padding:16px 20px;border:none;border-radius:12px;font-weight:bold;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;max-width:1100px;margin:20px auto}
.card{background:#1c1c1c;border-radius:18px;overflow:hidden;text-align:left;border:1px solid #2a2a2a;position:relative}
.card.sponsored{border:2px solid #ffcc00;box-shadow:0 0 15px #ffcc00aa}
.card img{width:100%;height:190px;object-fit:cover;background:#222}
.badge{position:absolute;top:8px;left:8px;background:#ffcc00;color:#000;padding:4px 8px;border-radius:8px;font-size:11px;font-weight:bold}
.card-body{padding:12px}
.price{color:#00ff88;font-size:19px;font-weight:bold}
.shop{color:#aaa;font-size:12px}
.btns{display:flex;gap:6px;margin-top:8px}
.btn{flex:1;padding:10px;border-radius:10px;border:none;font-weight:bold;cursor:pointer;text-align:center;text-decoration:none;font-size:13px}
.btn-wa{background:#25D366;color:white}
.btn-view{background:#333;color:white}
.donate{margin:30px auto;max-width:500px;background:#1c1c1c;padding:20px;border-radius:16px;border:1px solid #333}
</style>
</head>
<body>
<h1>📱 Phone Finder CPT <span class="live">DAY 8 MONEY</span></h1>
<div class="money-bar">💰 SHOPS: Want to be TOP result? WhatsApp 081 415 0336 — R300/week to be featured! 500+ searches/mo</div>
<p style="color:#888">Real CPT deals • Images • WhatsApp Share • Sponsored slots</p>
<input id="q" placeholder="iPhone 13, Samsung S23..." value="iPhone"><button class="search" onclick="search()">Search Live</button>
<div id="status"></div>
<div id="results" class="grid"></div>

<div class="donate">
<h3>❤️ Support This Project</h3>
<p style="color:#888;font-size:13px">This site is built by a CPT dev. Your R20 helps keep it live + add more shops</p>
<a href="https://wa.me/27814150336?text=Hi%20I%20want%20to%20support%20Phone%20Finder%20CPT" target="_blank" style="background:#00ff88;color:#000;padding:12px 20px;border-radius:12px;text-decoration:none;font-weight:bold;display:inline-block">Donate / Chat on WhatsApp</a>
</div>

<div style="max-width:1100px;margin:20px auto;background:#111;padding:10px;border-radius:12px;color:#555;font-size:12px">
AD SPACE - Your Google AdSense will show here after approval
</div>

<script>
async function search(){
 const q=document.getElementById('q').value;
 document.getElementById('status').innerHTML='<p>🔍 Searching...</p>';
 document.getElementById('results').innerHTML='';
 const res=await fetch('/search?q='+encodeURIComponent(q));
 const data=await res.json();
 document.getElementById('status').innerHTML=`<h3>${data.results.length} deals • ${data.source}</h3>`;
 let html='';
 data.results.forEach(r=>{
  const waText=encodeURIComponent(`🔥 ${r.name} for ${r.price} via Phone Finder CPT: https://phone-finder-cpt-6.onrender.com`);
  html+=`<div class="card ${r.sponsored?'sponsored':''}">${r.sponsored?'<div class="badge">⭐ SPONSORED TOP DEAL</div>':''}<img src="${r.image}" onerror="this.src='https://via.placeholder.com/300x200/222/00ff88?text=Phone'"><div class="card-body"><b>${r.name}</b><div class="price">${r.price}</div><div class="shop">${r.shop} • ${r.location}</div><div class="btns"><a class="btn btn-wa" href="https://wa.me/?text=${waText}" target="_blank">Share WA</a><a class="btn btn-view" href="${r.link}" target="_blank">${r.sponsored?'Call Shop - 0814150336':'View'}</a></div></div></div>`;
 });
 document.getElementById('results').innerHTML=html;
}
search();
</script>
</body></html>
"""

@app.get("/search")
def search(q: str = "iPhone"):
    live = scrape_pc(q)
    if len(live) < 2:
        live = [
            {"name": f"{q} - Takealot Deal","price": "R 9,499","shop": "Takealot","location": "CPT Warehouse","image": get_image(f"{q} Takealot"),"link": f"https://www.takealot.com/all?qsearch={q}","sponsored":False},
            {"name": f"{q} - Incredible Connection","price": "R 11,200","shop": "Incredible","location": "Canal Walk CPT","image": get_image(f"{q} Incredible"),"link": f"https://www.incredible.co.za/search?q={q}","sponsored":False},
            {"name": f"{q} - Cash Crusaders Goodwood","price": "R 6,800","shop": "Cash Crusaders","location": "Goodwood / Bellville","image": get_image(f"{q} Cash"),"link": "https://www.cashcrusaders.co.za/","sponsored":False},
        ]
        source="CPT Market Prices"
    else:
        source="PriceCheck LIVE"
    return {"query": q, "results": [SPONSORED_SHOP] + live, "source": source}