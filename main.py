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
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CPT Web Studio | Websites That Bring Customers in Cape Town</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0A0A0B;--card:#111113;--border:#1F1F23;--text:#FFFFFF;--muted:#A1A1AA;--gold:#FFC700;--gold2:#FFB800}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.container{max-width:1120px;margin:0 auto;padding:0 24px}
nav{border-bottom:1px solid var(--border);padding:20px 0;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:800;letter-spacing:-0.02em}.logo span{color:var(--gold)}
.badge{font-size:12px;background:var(--card);border:1px solid var(--border);padding:6px 12px;border-radius:100px;color:var(--muted)}
.hero{padding:100px 0 60px;display:grid;grid-template-columns:1.2fr 0.8fr;gap:60px;align-items:center}
@media(max-width:900px){.hero{grid-template-columns:1fr;padding:60px 0 40px}}
.h1{font-size:64px;line-height:0.95;letter-spacing:-0.04em;font-weight:800;margin-bottom:20px}
@media(max-width:900px){.h1{font-size:40px}}
.h1 em{color:var(--gold);font-style:normal}
.sub{color:var(--muted);font-size:18px;max-width:520px;margin-bottom:32px}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{padding:14px 24px;border-radius:12px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:.2s}
.btn-gold{background:var(--gold);color:#000}.btn-gold:hover{background:var(--gold2);transform:translateY(-1px)}
.btn-dark{background:var(--card);border:1px solid var(--border);color:var(--text)}
.stats{display:flex;gap:24px;margin-top:36px;border-top:1px solid var(--border);padding-top:24px}
.stat b{font-size:20px;display:block}.stat span{font-size:13px;color:var(--muted)}
.proof-card{background:linear-gradient(180deg,#161618 0%,#111113 100%);border:1px solid var(--border);border-radius:20px;padding:24px;position:relative;overflow:hidden}
.proof-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}
.live-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;display:inline-block;animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,.4)}70%{box-shadow:0 0 0 10px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:80px 0}
@media(max-width:900px){.grid3{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px}
.card h3{margin-bottom:8px;font-size:18px}.card p{color:var(--muted);font-size:14px}
.pricing{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:60px 0}
@media(max-width:900px){.pricing{grid-template-columns:1fr}}
.price-card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:32px;position:relative}
.price-card.featured{border-color:var(--gold);background:linear-gradient(180deg,#1A1808 0%,#111113 100%)}
.price{font-size:36px;font-weight:800;margin:12px 0}.price small{font-size:16px;color:var(--muted);font-weight:500}
ul{list-style:none;margin:20px 0}ul li{padding:8px 0;font-size:14px;color:var(--muted);display:flex;gap:10px}ul li::before{content:'✓';color:var(--gold);font-weight:700}
.footer{border-top:1px solid var(--border);padding:40px 0;margin-top:80px;color:var(--muted);font-size:13px;display:flex;justify-content:space-between}
</style>
</head>
<body>
<div class="container">
<nav>
<div class="logo">CPT WEB STUDIO <span>.</span></div>
<div class="badge">● Available for 2 new clients — June 2026</div>
</nav>

<section class="hero">
<div>
<h1 class="h1">Websites that <em>bring customers</em> — not just views.</h1>
<p class="sub">We help Cape Town phone shops & local businesses turn Google searches into WhatsApp messages and walk-ins. No templates. No fluff. Just revenue.</p>
<div class="btns">
<a class="btn btn-gold" href="https://wa.me/27814150336?text=Hi%20Victor,%20I%20saw%20CPT%20Web%20Studio%20—%20I%20want%20a%20website%20that%20brings%20customers">Chat on WhatsApp →</a>
<a class="btn btn-dark" href="#work">See live work</a>
</div>
<div class="stats">
<div class="stat"><b>R12k+</b><span>Client revenue tracked</span></div>
<div class="stat"><b>#1-3</b><span>Google ranking CPT</span></div>
<div class="stat"><b>48h</b><span>Average delivery</span></div>
</div>
</div>

<div class="proof-card" id="work">
<div style="display:flex;justify-content:space-between;margin-bottom:16px;font-size:12px;color:var(--muted)"><span><span class="live-dot"></span> LIVE PROJECT</span><span>phonefindercpt.co.za</span></div>
<img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600" style="width:100%;border-radius:12px;margin-bottom:16px;opacity:.9">
<h3 style="font-size:20px;margin-bottom:6px">PROJECT 01 — Phone Finder CPT</h3>
<p style="color:var(--muted);font-size:14px;margin-bottom:16px">The #1 iPhone price comparison in Cape Town. Built to rank, built to convert. 300+ daily searches, direct leads to shops.</p>
<a href="/" class="btn btn-dark" style="width:100%;justify-content:center">View Live Site →</a>
<div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border);display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:12px;color:var(--muted)">
<div>✔ SEO Optimized<br>✔ Mobile-first</div><div>✔ Ranks on Google<br>✔ Lead capture</div>
</div>
</div>
</section>

<div class="grid3">
<div class="card"><h3>Google-First Build</h3><p>We don't design for Dribbble. We design to rank for "iPhone shop Cape Town", "phone repair Bellville" — terms that bring buyers.</p></div>
<div class="card"><h3>WhatsApp Conversion</h3><p>Every page pushes to WhatsApp in 1 tap. No forms that kill leads. We track clicks, not vanity metrics.</p></div>
<div class="card"><h3>48 Hour Launch</h3><p>No 6-week agency nonsense. You get a live site in 48 hours. You sell while competitors are still in meetings.</p></div>
</div>

<h2 style="font-size:32px;letter-spacing:-0.02em;margin-top:20px">Simple pricing. Real ROI.</h2>
<div class="pricing">
<div class="price-card">
<div style="font-size:12px;letter-spacing:.1em;color:var(--muted)">STARTER</div>
<div class="price">R2,500 <small>once-off</small></div>
<p style="color:var(--muted);font-size:14px">Perfect to test if your shop needs online leads.</p>
<ul>
<li>1-page high-converting landing</li><li>WhatsApp + Call buttons</li><li>Google Business setup</li><li>Live in 48 hours</li>
</ul>
<a href="https://wa.me/27814150336?text=Starter%20R2500" class="btn btn-dark" style="width:100%;justify-content:center">Get Starter</a>
</div>

<div class="price-card featured">
<div style="font-size:12px;letter-spacing:.1em;color:var(--gold)">MOST POPULAR — SHOPS</div>
<div class="price">R5,500 <small>+ R497/mo</small></div>
<p style="color:var(--muted);font-size:14px">For shops that want to dominate Google in their area.</p>
<ul>
<li>Everything in Starter +</li><li>Price comparison / inventory system</li><li>SEO for 10+ keywords</li><li>Monthly ranking report + edits</li><li>Featured on Phone Finder CPT</li>
</ul>
<a href="https://wa.me/27814150336?text=Most%20Popular%20R5500" class="btn btn-gold" style="width:100%;justify-content:center">Get Dominance Package →</a>
</div>
</div>

<div class="footer">
<div>CPT Web Studio — Cape Town, SA — Building for local businesses.</div>
<div>© 2026 — We build sites that bring customers.</div>
</div>
</div>
</body>
</html>
    """