import threading, webbrowser, uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from duckduckgo_search import DDGS

app = FastAPI(title="Desk Setup Pro V2")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

@app.get("/api/research/{name}")
async def research(name: str):
    try:
        with DDGS() as ddgs:
            res = list(ddgs.text(f"{name} 최저가 최신 뉴스 동향", max_results=3))
            return {"status": "success", "result": "\n".join([r['body'] for r in res])}
    except: return {"status": "error"}

@app.get("/", response_class=HTMLResponse)
async def ui():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DESK SETUP PRO V2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>body { background-color: #030712; } .glass { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(255,255,255,0.1); }</style>
</head>
<body class="text-slate-100 pb-24 font-sans">
    <header class="sticky top-0 z-30 bg-slate-950/90 backdrop-blur border-b border-slate-800 p-5">
        <h1 class="font-black text-white">데스크 셋업 프로 V2</h1>
        <p class="text-[11px] text-slate-400">자산: <span id="totalAsset" class="text-cyan-400 font-bold">0원</span> | 위시: <span id="wishTotal" class="text-purple-400 font-bold">0원</span></p>
    </header>

    <div id="banner" class="m-4 p-3 rounded-xl bg-purple-900/30 border border-purple-500/30 text-[11px] hidden text-purple-200"></div>

    <div class="px-5 py-2 flex gap-2 overflow-x-auto">
        <button onclick="render('전체')" class="px-4 py-2 bg-slate-800 rounded-xl text-xs font-black">전체보기</button>
        <button onclick="render('게이밍')" class="px-4 py-2 bg-slate-800 rounded-xl text-xs font-bold">게이밍</button>
        <button onclick="render('사무용')" class="px-4 py-2 bg-slate-800 rounded-xl text-xs font-bold">사무용</button>
        <button onclick="viewDeals()" class="px-4 py-2 bg-amber-600 rounded-xl text-xs font-black">세일캘린더</button>
    </div>

    <main id="itemList" class="p-4 space-y-4"></main>

    <div id="modal" class="fixed inset-0 bg-black/80 hidden z-50 p-5 flex items-center justify-center">
        <div class="glass w-full p-5 rounded-2xl">
            <h2 class="font-black mb-4">제품 추가</h2>
            <input id="inName" placeholder="제품명" class="w-full bg-slate-900 p-2 rounded mb-2">
            <input id="inPrice" type="number" placeholder="가격" class="w-full bg-slate-900 p-2 rounded mb-4">
            <div class="flex gap-2"><button onclick="add()" class="bg-cyan-500 flex-1 py-2 rounded font-black">추가</button><button onclick="closeModal()" class="bg-slate-700 flex-1 py-2 rounded">취소</button></div>
        </div>
    </div>

    <script>
        let items = JSON.parse(localStorage.getItem('db')) || [
            {id:1, name:"Razer Basilisk V3 Pro 35K", base_price:239000, category:"게이밍", sub:"마우스"},
            {id:2, name:"Maono PD200X", base_price:89160, category:"게이밍", sub:"마이크"},
            {id:3, name:"Logitech MX Master 4", base_price:179000, category:"사무용", sub:"마우스"},
            {id:4, name:"Glorious GMP2 XXL", base_price:49900, category:"공용", sub:"마우스 패드"},
            {id:5, name:"Desk Shelf (Wood)", base_price:30000, category:"공용", sub:"데스크 선반"},
            {id:6, name:"AZLA SednaEarfit", base_price:89100, category:"게이밍", sub:"이어폰"},
            {id:7, name:"Maonocaster G1", base_price:63850, category:"게이밍", sub:"오인페"},
            {id:8, name:"Elgato StreamDeck", base_price:133300, category:"게이밍", sub:"키보드"},
            {id:9, name:"Edifier MR4", base_price:76410, category:"공용", sub:"스피커"},
            {id:10, name:"Zeuslap Z16P", base_price:150700, category:"공용", sub:"모니터"},
            {id:11, name:"Keychron Q1", base_price:239000, category:"게이밍", sub:"키보드"}
        ];

        function save() { localStorage.setItem('db', JSON.stringify(items)); render(); }
        
        async function render(cat='전체') {
            const list = document.getElementById('itemList');
            const data = cat==='전체'?items:items.filter(i=>i.category===cat);
            document.getElementById('totalAsset').textContent = data.reduce((s,i)=>s+i.base_price,0).toLocaleString() + '원';
            list.innerHTML = data.map(i => `
                <div class="glass p-4 rounded-2xl flex flex-col gap-3">
                    <div class="flex justify-between items-center">
                        <div><h3 class="font-bold text-sm">${i.name}</h3><p class="text-[10px] text-slate-500">${i.sub}</p></div>
                        <span class="text-cyan-400 font-mono text-xs font-bold">${i.base_price.toLocaleString()}원</span>
                    </div>
                    <div class="grid grid-cols-4 gap-1 text-center text-[10px]">
                        <a href="https://search.shopping.naver.com/search/all?query=${i.name}" target="_blank" class="bg-green-500/20 text-green-400 p-1 rounded font-black">N</a>
                        <a href="https://search.danawa.com/dsearch.php?query=${i.name}" target="_blank" class="bg-blue-500/20 text-blue-400 p-1 rounded font-black">D</a>
                        <a href="https://www.amazon.com/s?k=${i.name}" target="_blank" class="bg-amber-500/20 text-amber-400 p-1 rounded font-black">Amz</a>
                        <a href="https://ko.aliexpress.com/w/wholesale-${i.name}.html" target="_blank" class="bg-red-500/20 text-red-400 p-1 rounded font-black">Ali</a>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="window.open('https://www.perplexity.ai/search?q=${encodeURIComponent(i.name + ' 가격 분석')}')" class="bg-blue-600 flex-1 py-1 rounded text-[10px] font-black">AI 분석</button>
                        <button onclick="price(${i.id})" class="bg-slate-700 flex-1 py-1 rounded text-[10px]">가격 변경</button>
                    </div>
                </div>
            `).join('');
        }

        function viewDeals() {
            document.getElementById('itemList').innerHTML = `
                <div class="glass p-5 rounded-2xl text-amber-400 text-xs">
                    <h2 class="font-black mb-3">글로벌 세일 캘린더</h2>
                    <div class='space-y-2'>
                        <p>알리 광군제: D-84</p><p>블랙프라이데이: D-100</p>
                    </div>
                </div>`;
        }

        function price(id) { const i = items.find(x=>x.id===id); const v = prompt("새 가격:", i.base_price); if(v) { i.base_price=Number(v); save(); }}
        function openAddModal() { document.getElementById('modal').classList.remove('hidden'); }
        function closeModal() { document.getElementById('modal').classList.add('hidden'); }
        function add() { items.push({id:Date.now(), name:document.getElementById('inName').value, base_price:Number(document.getElementById('inPrice').value), sub:"기타", category:"공용"}); closeModal(); save(); }
        
        window.onload = () => { render(); fetch('/api/research/'+items[0].name).then(r=>r.json()).then(d=>{if(d.status==='success'){document.getElementById('banner').classList.remove('hidden'); document.getElementById('banner').innerText = d.result.substring(0,80);}}); };
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
