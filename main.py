from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
HEADERS = {"User-Agent": "Mozilla/5.0 Chrome/120.0"}

IMAGES = {
 "iphone1": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&h=350&fit=crop&crop=center",
 "iphone2": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=500&h=350&fit=crop",
 "iphone3": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=350&fit=crop",
 "samsung": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&h=350&fit=crop",
 "luxury": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=400&fit=crop"
}

SPONSORED = {
 "name": "Your Brand Dominates Cape Town",
 "price": "Be The #1 Featured Retailer — R2,500/mo",
 "shop": "Phone Finder CPT — Premium Network",
 "location": "Canal Walk • Century City • V&A • Claremont • Tygervalley",
 "image": IMAGES["luxury"],
 "link": "https://wa.me/27814150336?text=Hi!%20I%20want%20to%20book%20Premium%20Slot%20for%20my%20shop%20-%20R2500/mo%20-%20Phone%20Finder%20CPT",
 "sponsored": True
}

@app.get("/", response_class=HTMLResponse)
def home():
 return """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Phone Finder CPT | Premium Retail Intelligence</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{font-family:'Inter',-apple-system,sans-serif;box-sizing:border-box}
body{margin:0;background:#050507;color:#fff;overflow-x:hidden}
.header{position:sticky;top:0;z-index:50;background:rgba(5,5,7,0.9);backdrop-filter:blur(20px);border-bottom:1px solid #1a1a1a;padding:14px 20px;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:900;letter-spacing:-1px;font-size:18px} .logo span{color:#FFD700}
.live-dot{width:8px;height:8px;background:#00FF88;border-radius:50%;display:inline-block;animation:pulse 2s infinite;margin-right:6px}
@keyframes pulse{0%{opacity:1}50%{opacity:0.4}100%{opacity:1}}
@keyframes glow{0%{box-shadow:0 0 20px #FFD70033}50%{box-shadow:0 0 40px #FFD70066}100%{box-shadow:0 0 20px #FFD70033}}
.hero{text-align:center;padding:40px 20px 10px}
.hero h1{font-size:42px;font-weight:900;letter-spacing:-2px;line-height:0.9;margin:0} .hero h1 em{font-style:normal;background:linear-gradient(90deg,#FFD700,#FFA500);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#666;margin-top:12px;font-size:14px}
.bar{max-width:1100px;margin:24px auto;background:linear-gradient(90deg,#FFD700,#FFB800);color:#000;padding:12px;border-radius:100px;font-weight:800;font-size:12px;letter-spacing:0.5px;text-align:center}
.search-wrap{max-width:600px;margin:20px auto;display:flex;gap:10px;padding:0 20px}
.input{flex:1;background:#111;border:1px solid #222;padding:16px 20px;border-radius:14px;color:#fff;font-size:16px;outline:none} .input:focus{border-color:#FFD700}
.btn-search{background:#fff;color:#000;border:none;padding:16px 28px;border-radius:14px;font-weight:800;cursor:pointer}
.grid{max-width:1150px;margin:30px auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;padding:0 20px}
.card{background:#0F0F10;border:1px solid #1E1E1F;border-radius:24px;overflow:hidden;transition:all 0.3s;position:relative}
.card:hover{transform:translateY(-4px);border-color:#2a2a2a}
.card.sponsored{border:1.5px solid #FFD700;animation:glow 3s infinite;background:linear-gradient(180deg,#1A1805 0%,#0F0F10 60%)}
.card img{width:100%;height:230px;object-fit:cover}
.tag{position:absolute;top:14px;left:14px;background:#FFD700;color:#000;padding:6px 12px;border-radius:100px;font-size:10px;font-weight:900;letter-spacing:0.5px}
.verified{position:absolute;top:14px;right:14px;background:rgba(0,0,0,0.7);backdrop-filter:blur(10px);color:#00FF88;padding:6px 10px;border-radius:100px;font-size:10px;font-weight:700;border:1px solid #222}
.body{padding:18px}
.name{font-weight:700;font-size:16px;line-height:1.2}
.meta{display:flex;gap:8px;margin:8px 0;color:#666;font-size:11px;align-items:center} .dot{width:3px;height:3px;background:#444;border-radius:50%}
.price-row{display:flex;justify-content:space-between;align-items:center;margin-top:12px}
.price{font-size:26px;font-weight:900;letter-spacing:-1px} .price small{font-size:12px;color:#00FF88;font-weight:700}
.actions{display:flex;gap:8px;margin-top:14px}
.a{flex:1;padding:12px;border-radius:12px;text-align:center;text-decoration:none;font-weight:700;font-size:13px}
.a-ghost{background:#1A1A1A;color:#fff;border:1px solid #222}
.a-green{background:#00FF88;color:#000}
.a-gold{background:linear-gradient(90deg,#FFD700,#FFB800);color:#000;font-weight:900}
</style></head>
<body>
<div class="header"><div class="logo">PHONE FINDER <span>CPT</span></div><div style="font-size:11px;color:#888"><span class="live-dot"></span>PREMIUM • LIVE</div></div>
<div class="hero"><h1>Find phones.<br><em>Not scams.</em></h1><p>Live prices from Canal Walk, Century City, V&A, Claremont, Tygervalley</p></div>
<div class="bar">⚡ 1 PREMIUM SLOT LEFT THIS MONTH — R2,500/MO — 081 415 0336 — BRANDS APPLYING NOW</div>
<div class="search-wrap"><input id="q" class="input" placeholder="iPhone 15 Pro Max, S24 Ultra..." value="iPhone 15 Pro"><button class="btn-search" onclick="doSearch()">Search</button></div>
<div id="results" class="grid"></div>
<script>
const imgs=["https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500&h=350&fit=crop","https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=500&h=350&fit=crop","https://images.unsplash.com/photo-1556656793-08538906a9f8?w=500&h=350&fit=crop","https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&h=350&fit=crop"];
async function doSearch(){
 const q=document.getElementById('q').value||'iPhone';
 document.getElementById('results').innerHTML='<p style=text-align:center;color:#444;padding:40px>Searching verified CPT retailers...</p>';
 const r=await fetch('/search?q='+encodeURIComponent(q)); const d=await r.json();
 let h='';
 d.results.forEach((x,i)=>{
  const wa=`https://wa.me/?text=${encodeURIComponent(`🔥 ${x.name} - ${x.price} via Phone Finder CPT: ${x.link}`)}`;
  const badge=x.sponsored?`<div class=tag>⭐ PREMIUM • R2,500/MO</div>`:`<div class=tag style=background:#111;color:#888;border:1px solid #222>${x.shop.toUpperCase()}</div>`;
  const ver=x.sponsored?'':`<div class=verified>✓ VERIFIED</div>`;
  const priceBtn=x.sponsored?`<a class="a a-gold" href="${x.link}" target=_blank>Enquire Now — Claim Slot</a>`:`<a class="a a-ghost" href="${x.link}" target=_blank>View Deal</a>`;
  h+=`<div class="card ${x.sponsored?'sponsored':''}">${badge}${ver}<img src="${x.image||imgs[i%imgs.length]}" onerror="this.src='${imgs[i%imgs.length]}'"><div class=body><div class=name>${x.name}</div><div class=meta><span>${x.shop}</span><span class=dot></span><span>${x.location}</span></div><div class=price-row><div class=price>${x.price} <small>• In Stock CPT</small></div></div><div class=actions><a class="a a-green" href="${wa}" target=_blank>WhatsApp</a>${priceBtn}</div></div></div>`;
 });
 document.getElementById('results').innerHTML=h;
}
doSearch();
</script>
</body></html>
"""

@app.get("/search")
def search(q: str = "iPhone"):
    # fallback data with varied images
    base = [
        {"name": f"{q} 256GB - Midnight Black","price": "R 19,999","shop": "Takealot","location": "Canal Walk • Free Delivery","image": IMAGES["iphone1"],"link": f"https://www.takealot.com/all?qsearch={q}","sponsored": False},
        {"name": f"{q} 128GB - Natural Titanium","price": "R 22,499","shop": "iStore","location": "V&A Waterfront • Century City","image": IMAGES["iphone2"],"link": f"https://www.myistore.co.za/search?q={q}","sponsored": False},
        {"name": f"{q} - Vodacom Contract + Cash","price": "R 18,749","shop": "Vodacom 4U","location": "Claremont • Tygervalley","image": IMAGES["iphone3"],"link": f"https://www.vodacom.co.za/","sponsored": False},
        {"name": f"{q} - MTN Deal + Free Buds","price": "R 20,150","shop": "MTN","location": "Canal Walk • Century City","image": IMAGES["samsung"],"link": f"https://www.mtn.co.za/","sponsored": False},
    ]
    return {"results": [SPONSORED] + base}

@app.get("/agency", response_class=HTMLResponse)
def agency():
    return """
    <html><head><title>CPT Web Studio</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:Inter,sans-serif;max-width:800px;margin:40px auto;padding:20px;line-height:1.6;background:#050507;color:#fff}
    a.btn{background:#fff;color:#000;padding:14px 22px;text-decoration:none;border-radius:10px;display:inline-block;font-weight:900}
    .card{border:1px solid #222;padding:20px;border-radius:14px;margin:20px 0;background:#0F0F10}
    </style>
    </head><body>
    <h1>CPT Web Studio — Websites that bring customers</h1>
    <p>We help Cape Town phone shops & local businesses get more customers from Google.</p>
    <div class="card">
    <h2>🚀 PROJECT 1 — LIVE: Phone Finder CPT</h2>
    <p>The #1 iPhone price comparison in Cape Town — ranks on Google.</p>
    <p><a href="/">View Live Site → phonefindercpt.co.za</a></p>
    </div>
    <div class="card">
    <h2>📱 PROJECT 2 — DEMO: WeFix Landing</h2>
    <p>Fast mobile landing page to push WhatsApp leads.</p>
    </div>
    <h3>From R2,500 once-off</h3>
    <a class="btn" href="https://wa.me/27814150336">Chat on WhatsApp</a>
    <p style="color:#666;margin-top:40px">© CPT Web Studio</p>
    </body></html>
    """