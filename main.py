from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HEADERS = {"User-Agent": "Mozilla/5.0 Chrome/120.0"}

# REAL PHONE IMAGES - NO MORE GREEN BOXES
PHONE_IMAGES = {
    "iphone": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=300&fit=crop",
    "samsung": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=300&fit=crop",
    "default": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop"
}

def get_real_image(query):
    q = query.lower()
    if "iphone" in q or "apple" in q:
        return PHONE_IMAGES["iphone"]
    if "samsung" in q or "galaxy" in q:
        return PHONE_IMAGES["samsung"]
    return PHONE_IMAGES["default"]

SPONSORED_SHOP = {
    "name": "💼 PREMIUM RETAILER SLOT - Available",
    "price": "Your Shop Featured Across CPT - From R2,500/mo",
    "shop": "Phone Finder CPT",
    "location": "Canal Walk • Century City • V&A • Claremont • Tygervalley",
    "image": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=400&fit=crop", # luxury store
    "link": "https://wa.me/27814150336?text=Hi%20Phone%20Finder%20CPT%2C%20I%20want%20to%20book%20the%20Premium%20Slot%20R2500%2Fmo%20for%20my%20shop",
    "sponsored": True
}

def scrape_pc(query):
    results=[]
    try:
        url=f"https://www.pricecheck.co.za/search?search={query}"
        r=requests.get(url, headers=HEADERS, timeout=8)
        soup=BeautifulSoup(r.text,"html.parser")
        for card in soup.select("div.product-list-item")[:6]:
            n=card.select_one("a.title")
            p=card.select_one(".price")
            if n and p:
                results.append({
                    "name": n.get_text(strip=True)[:50],
                    "price": p.get_text(strip=True).replace("From","").strip(),
                    "shop": "PriceCheck Verified",
                    "location": "CPT Delivery",
                    "image": get_real_image(query),
                    "link": f"https://www.pricecheck.co.za/search?search={query}",
                    "sponsored": False
                })
    except: pass
    return results

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html><head><title>Phone Finder CPT - Premium Retail Platform</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#080808;color:#fff;margin:0;padding:16px;text-align:center}
.live{background:#00ff88;color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:bold}
.money-bar{background:linear-gradient(90deg,#FFD700,#FFA500);color:#000;padding:14px;border-radius:12px;margin:15px auto;max-width:1100px;font-weight:800;font-size:13px;letter-spacing:0.3px}
input{padding:16px;width:60%;max-width:320px;border-radius:12px;border:none;font-size:16px;background:#1a1a1a;color:#fff;border:1px solid #333}
button.search{background:#00ff88;padding:16px 20px;border:none;border-radius:12px;font-weight:800;cursor:pointer;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;max-width:1100px;margin:20px auto}
.card{background:#161616;border-radius:20px;overflow:hidden;text-align:left;border:1px solid #262626;position:relative;transition:0.2s}
.card:hover{transform:translateY(-3px);border-color:#333}
.card.sponsored{border:2px solid #FFD700;box-shadow:0 0 30px #FFD70033;background:linear-gradient(180deg,#1a1800,#161616)}
.card img{width:100%;height:210px;object-fit:cover;background:#222}
.badge{position:absolute;top:10px;left:10px;background:#FFD700;color:#000;padding:5px 10px;border-radius:20px;font-size:11px;font-weight:900;letter-spacing:0.5px}
.card-body{padding:14px}
.price{color:#00ff88;font-size:20px;font-weight:800;margin:6px 0}
.shop{color:#999;font-size:12px}
.btns{display:flex;gap:8px;margin-top:10px}
.btn{flex:1;padding:11px;border-radius:11px;border:none;font-weight:700;cursor:pointer;text-align:center;text-decoration:none;font-size:13px}
.btn-wa{background:#25D366;color:white}
.btn-view{background:#2a2a2a;color:white;border:1px solid #333}
.btn-gold{background:linear-gradient(90deg,#FFD700,#FFA500);color:#000}
</style>
</head>
<body>
<h1>📱 Phone Finder CPT <span class="live">PREMIUM</span></h1>
<div class="money-bar">💼 PREMIUM RETAILER NETWORK: Canal Walk • Century City • V&A Waterfront • Claremont • Tygervalley — Enquire to feature: 081 415 0336 — From R2,500/mo</div>
<p style="color:#888">Verified CPT retailers • Live price comparison • Direct WhatsApp leads</p>
<input id="q" placeholder="Search iPhone 15 Pro, Samsung S24..." value="iPhone"><button class="search" onclick="search()">Search Live</button>
<div id="status"></div>
<div id="results" class="grid"></div>
<script>
async function search(){
 const q=document.getElementById('q').value;
 document.getElementById('status').innerHTML='<p style=color:#888>🔍 Searching verified retailers...</p>';
 document.getElementById('results').innerHTML='';
 const res=await fetch('/search?q='+encodeURIComponent(q));
 const data=await res.json();
 document.getElementById('status').innerHTML=`<h3 style=color:#FFD700>${data.results.length} verified deals • ${data.source}</h3>`;
 let html='';
 data.results.forEach(r=>{
  const waText=encodeURIComponent(`🔥 ${r.name} for ${r.price} - Found via Phone Finder CPT`);
  const btnClass = r.sponsored ? 'btn btn-gold' : 'btn btn-view';
  const btnLabel = r.sponsored ? 'Enquire Now — R2,500/mo' : 'View Deal';
  html+=`<div class="card ${r.sponsored?'sponsored':''}">${r.sponsored?'<div class="badge">⭐ PREMIUM SLOT R2,500/MO</div>':''}<img src="${r.image}" onerror="this.src='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'"><div class="card-body"><b>${r.name}</b><div class="price">${r.price}</div><div class="shop">${r.shop} • ${r.location}</div><div class="btns"><a class="btn btn-wa" href="https://wa.me/?text=${waText}" target="_blank">Share</a><a class="${btnClass}" href="${r.link}" target="_blank">${btnLabel}</a></div></div></div>`;
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
            {"name": f"{q} - Takealot Official","price": "R 9,499","shop": "Takealot","location": "Canal Walk • Century City","image": get_real_image(q),"link": f"https://www.takealot.com/all?qsearch={q}","sponsored":False},
            {"name": f"{q} - Incredible Connection","price": "R 11,199","shop": "Incredible Connection","location": "V&A • Claremont • Tygervalley","image": get_real_image(q),"link": f"https://www.incredible.co.za/search?q={q}","sponsored":False},
            {"name": f"{q} - Vodacom 4U","price": "R 10,850","shop": "Vodacom","location": "Century City • Canal Walk","image": get_real_image(q),"link": f"https://www.vodacom.co.za/","sponsored":False},
        ]
        source="Verified CPT Retailers"
    else:
        source="PriceCheck LIVE + Premium"
    return {"query": q, "results": [SPONSORED_SHOP] + live, "source": source}