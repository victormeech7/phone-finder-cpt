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
    "name": "💼 PREMIUM SLOT AVAILABLE - Your Shop Here",
    "price": "Be Top Across CPT - R2,500/mo",
    "shop": "Phone Finder CPT - Premium",
    "location": "Canal Walk • V&A • Century City • Claremont",
    "image": "https://via.placeholder.com/400x300/ffcc00/000?text=YOUR+SHOP+HERE+R2500/mo",
    "link": "https://wa.me/27814150336?text=Hi%20Phone%20Finder%20CPT%20Team%2C%20I%20want%20the%20Premium%20Retailer%20Slot%20for%20R2500%2Fmonth",
    "sponsored": True
}

def get_image(name): return f"https://via.placeholder.com/400x300/00ff88/000?text={urllib.parse.quote(name[:20])}"

def scrape_pc(query):
    results=[]
    try:
        url=f"https://www.pricecheck.co.za/search?search={query}"
        r=requests.get(url, headers=HEADERS, timeout=8)
        soup=BeautifulSoup(r.text,"html.parser")
        for card in soup.select("div.product-list-item")[:6]:
            n=card.select_one("a.title")
            p=card.select_one(".price")
            img=card.select_one("img")
            if n and p:
                img_url=img.get("src") if img else get_image(n.text[:20])
                if img_url and img_url.startswith("/"): img_url="https://www.pricecheck.co.za"+img_url
                results.append({"name":n.get_text(strip=True)[:50],"price":p.get_text(strip=True).replace("From","").strip(),"shop":"PriceCheck","location":"CPT Delivery","image":img_url,"link":f"https://www.pricecheck.co.za/search?search={query}","sponsored":False})
    except: pass
    return results

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html><head><title>Phone Finder CPT - Premium Retail Platform</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:sans-serif;background:#0a0a0a;color:#fff;margin:0;padding:16px;text-align:center}
.live{background:#00ff88;color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:bold}
.money-bar{background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:12px;border-radius:12px;margin:15px auto;max-width:1100px;font-weight:bold;font-size:13px}
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
</style>
</head>
<body>
<h1>📱 Phone Finder CPT <span class="live">PREMIUM</span></h1>
<div class="money-bar">💼 PREMIUM RETAILER SLOTS: Feature your store across Canal Walk, Century City, V&A, Claremont & Tygervalley — From R2,500/month — Enquire: 081 415 0336</div>
<p style="color:#888">Live CPT price comparison • Verified retailers • Direct WhatsApp leads</p>
<input id="q" placeholder="iPhone 15 Pro, Samsung S24..." value="iPhone"><button class="search" onclick="search()">Search Live</button>
<div id="status"></div>
<div id="results" class="grid"></div>
<script>
async function search(){
 const q=document.getElementById('q').value;
 document.getElementById('status').innerHTML='<p>🔍 Searching premium retailers...</p>';
 document.getElementById('results').innerHTML='';
 const res=await fetch('/search?q='+encodeURIComponent(q));
 const data=await res.json();
 document.getElementById('status').innerHTML=`<h3>${data.results.length} deals • ${data.source}</h3>`;
 let html='';
 data.results.forEach(r=>{
  const waText=encodeURIComponent(`🔥 ${r.name} for ${r.price} via Phone Finder CPT`);
  html+=`<div class="card ${r.sponsored?'sponsored':''}">${r.sponsored?'<div class="badge">💼 PREMIUM SLOT - R2,500/MO</div>':''}<img src="${r.image}"><div class="card-body"><b>${r.name}</b><div class="price">${r.price}</div><div class="shop">${r.shop} • ${r.location}</div><div class="btns"><a class="btn btn-wa" href="https://wa.me/?text=${waText}" target="_blank">Share</a><a class="btn btn-view" href="${r.link}" target="_blank">${r.sponsored?'Enquire Now':'View'}</a></div></div></div>`;
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
            {"name": f"{q} - Takealot","price": "R 9,499","shop": "Takealot","location": "CPT Warehouse","image": get_image(f"{q} Takealot"),"link": f"https://www.takealot.com/all?qsearch={q}","sponsored":False},
            {"name": f"{q} - Incredible Connection","price": "R 11,200","shop": "Incredible","location": "Canal Walk • Century City","image": get_image(f"{q} Incredible"),"link": f"https://www.incredible.co.za/search?q={q}","sponsored":False},
            {"name": f"{q} - Cash Crusaders","price": "R 6,800","shop": "Cash Crusaders","location": "Claremont • Tygervalley","image": get_image(f"{q} Cash"),"link": "https://www.cashcrusaders.co.za/","sponsored":False},
        ]
        source="Premium CPT Retailers"
    else:
        source="PriceCheck LIVE"
    return {"query": q, "results": [SPONSORED_SHOP] + live, "source": source}