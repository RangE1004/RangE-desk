import os
import json
import threading
import webbrowser
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from duckduckgo_search import DDGS

app = FastAPI(title="Desk Setup Pro V2")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_FILE = "products_master_final.json"
RECOMMENDATIONS_FILE = "recommendations_master.json"

MASTER_ITEMS = [
    {"id": 1, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마우스", "name": "Razer Basilisk V3 Pro 35K", "query": "Razer Basilisk V3 Pro 35K", "global_query": "Razer Basilisk V3 Pro 35K", "base_price": 239000, "target_price": 210000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800", "icon": "fa-computer-mouse"},
    {"id": 2, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "이어폰", "name": "AZLA SednaEarfit Azel Edition G Gen 3", "query": "아즈라 아젤 에디션 G 3세대", "global_query": "AZLA SednaEarfit Azel Edition G Gen 3", "base_price": 89100, "target_price": 80000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800", "icon": "fa-headphones"},
    {"id": 3, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마이크", "name": "Maono DM40 Pro", "query": "마오노 DM40 Pro", "global_query": "Maono DM40 Pro", "base_price": 139000, "target_price": 120000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800", "icon": "fa-microphone"},
    {"id": 4, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마이크", "name": "Maono PD200X", "query": "마오노 PD200X", "global_query": "Maono PD200X", "base_price": 89160, "target_price": 80000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800", "icon": "fa-microphone"},
    {"id": 5, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "오디오 인터페이스", "name": "Maonocaster G1 NEO", "query": "마오노 G1 NEO", "global_query": "Maonocaster G1 NEO", "base_price": 63850, "target_price": 60000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800", "icon": "fa-sliders"},
    {"id": 6, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "키보드/스트림덱", "name": "Elgato Stream Deck Neo", "query": "엘가토 스트림덱 네오", "global_query": "Elgato Stream Deck Neo", "base_price": 133300, "target_price": 120000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800", "icon": "fa-keyboard"},
    {"id": 7, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "사무용", "sub_group": "마우스", "name": "Logitech MX Master 4", "query": "로지텍 MX master 4", "global_query": "Logitech MX Master 4", "base_price": 179000, "target_price": 160000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800", "icon": "fa-computer-mouse"},
    {"id": 8, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "스피커", "name": "Edifier MR4", "query": "edifier mr4", "global_query": "Edifier MR4", "base_price": 76410, "target_price": 70000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800", "icon": "fa-volume-high"},
    {"id": 9, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "포터블 모니터", "name": "Zeuslap Z16P", "query": "제우스랩 Z16P", "global_query": "Zeuslap Z16P", "base_price": 150700, "target_price": 140000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800", "icon": "fa-display"},
    {"id": 10, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "마우스 패드", "name": "Glorious GMP2 XXL White", "query": "글로리어스 GMP2 화이트 XXL", "global_query": "Glorious GMP2 XXL White", "base_price": 49900, "target_price": 45000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=800", "icon": "fa-square"},
    {"id": 11, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "데스크 선반", "name": "Desk Shelf (White/Wood)", "query": "데스크 선반 모니터 받침대 원목", "global_query": "Desk Shelf Monitor Stand Timber", "base_price": 30000, "target_price": 25000, "last_updated": "등록일", "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800", "icon": "fa-table"}
]

RECOMMENDATION_POOL = [
    {"id": 201, "name": "Logitech G Pro X Superlight 2", "sub_group": "마우스", "base_price": 199000, "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800"},
    {"id": 202, "name": "Keychron Q1 Max 무선 기계식 키보드", "sub_group": "키보드/스트림덱", "base_price": 239000, "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"},
    {"id": 203, "name": "Sony WH-1000XM5 무선 노이즈캔슬링 헤드셋", "sub_group": "이어폰", "base_price": 479000, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"},
    {"id": 204, "name": "BenQ ScreenBar Halo 모니터 조명", "sub_group": "데스크 선반", "base_price": 189000, "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800"},
    {"id": 205, "name": "Dell UltraSharp U2723QE 4K 모니터", "sub_group": "포터블 모니터", "base_price": 750000, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"}
]

def init_files():
    try:
        if not os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
                json.dump(MASTER_ITEMS, f, ensure_ascii=False, indent=4)
        if not os.path.exists(RECOMMENDATIONS_FILE):
            with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(RECOMMENDATION_POOL, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("File init error:", e)

@app.on_event("startup")
async def startup_event():
    init_files()
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

@app.get("/api/items")
async def get_items():
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return MASTER_ITEMS
    return MASTER_ITEMS

@app.get("/api/recommendations")
async def get_recommendations(sub_group: str = Query(...)):
    if os.path.exists(RECOMMENDATIONS_FILE):
        try:
            with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
                recs = json.load(f)
        except:
            recs = RECOMMENDATION_POOL
    else:
        recs = RECOMMENDATION_POOL
    matched = [r for r in recs if r["sub_group"] == sub_group]
    if not matched:
        matched = recs[:3]
    return matched

@app.get("/api/research/{name}")
async def research(name: str):
    try:
        with DDGS() as ddgs:
            res = list(ddgs.text(f"{name} 최저가 최신 뉴스 하락세", max_results=2))
            if res:
                summary = "🔥 [실시간 누적 리서치]\n" + "\n".join([f"- {r['body']}" for r in res])
                return {"status": "success", "result": summary}
            else:
                return {"status": "error"}
    except: 
        return {"status": "error"}

# 🔥 안드로이드 바탕화면 아이콘을 강제로 씌우는 전용 서버 경로 추가
@app.get("/manifest.json")
async def get_manifest():
    return {
        "name": "Desk Setup Pro V2",
        "short_name": "Setup Pro",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#030712",
        "theme_color": "#030712",
        "icons": [
            {
                "src": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=512&h=512&fit=crop",
                "sizes": "512x512",
                "type": "image/jpeg",
                "purpose": "any maskable"
            }
        ]
    }

@app.get("/", response_class=HTMLResponse)
async def serve_mobile_ui():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DESK SETUP PRO V2</title>
    
    <!-- 정식 앱 매니페스트 호출 (버전 쿼리를 달아서 안드로이드 강제 새로고침 유도) -->
    <meta name="theme-color" content="#030712">
    <link rel="manifest" href="/manifest.json?v=3">
    <link rel="icon" type="image/jpeg" sizes="512x512" href="https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=512&h=512&fit=crop">
    <link rel="apple-touch-icon" href="https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=512&h=512&fit=crop">

    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { 
            -webkit-tap-highlight-color: transparent; 
            background: linear-gradient(135deg, #030712 0%, #0f172a 100%);
            min-height: 100vh;
        }
        
        .glass-card { 
            background: rgba(15, 23, 42, 0.75); 
            backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); 
        }
        
        input, select { transition: all 0.3s ease; }
        input:focus, select:focus { box-shadow: 0 0 10px rgba(34, 211, 238, 0.3); }

        @keyframes urgent-glow {
            0% { border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.7); }
            50% { border-color: #ef4444; box-shadow: 0 0 25px rgba(239, 68, 68, 0.9); }
            100% { border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.7); }
        }
        .urgent-border { animation: urgent-glow 1.5s infinite linear; border-width: 2px !important; }
        
        @keyframes glamorous-glow {
            0% { border-color: #34d399; box-shadow: 0 0 20px rgba(52, 211, 153, 0.7), inset 0 0 10px rgba(52, 211, 153, 0.3); }
            50% { border-color: #6ee7b7; box-shadow: 0 0 35px rgba(110, 231, 183, 1), inset 0 0 20px rgba(110, 231, 183, 0.6); }
            100% { border-color: #34d399; box-shadow: 0 0 20px rgba(52, 211, 153, 0.7), inset 0 0 10px rgba(52, 211, 153, 0.3); }
        }
        .purchase-glow-card { animation: glamorous-glow 1.5s infinite ease-in-out; border-width: 2px !important; }

        .buy-stamp {
            position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%) rotate(-12deg);
            border: 4px dashed #dc2626; color: #dc2626; font-weight: 900; font-size: 2.2rem; padding: 6px 20px;
            letter-spacing: 4px; text-transform: uppercase; pointer-events: none; z-index: 30; opacity: 0.95;
            box-shadow: inset 0 0 15px rgba(220, 38, 38, 0.3), 0 0 25px rgba(220, 38, 38, 0.5); border-radius: 12px;
            background-color: rgba(3, 7, 18, 0.6); font-family: monospace; text-shadow: 0 0 4px rgba(220, 38, 38, 0.8);
        }

        .modal-enter { animation: fadeIn 0.3s ease-out forwards; }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
        
        .toast-enter { animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes slideUp { from { opacity: 0; transform: translate(-50%, 100%); } to { opacity: 1; transform: translate(-50%, 0); } }
    </style>
</head>
<body class="text-slate-100 pb-24 font-sans selection:bg-cyan-500/30">
    <header class="sticky top-0 z-30 bg-slate-950/80 backdrop-blur-2xl border-b border-slate-800/80 px-5 py-4 shadow-xl">
        <div class="flex justify-between items-center">
            <div>
                <h1 class="text-lg font-black bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-emerald-400 flex items-center gap-2 tracking-widest font-mono drop-shadow-md">
                    <i class="fa-solid fa-layer-group text-cyan-400 drop-shadow-none"></i> DESK SETUP PRO
                </h1>
                <p class="text-[11px] text-slate-400 font-mono mt-1">보유 자산: <span id="totalAsset" class="text-cyan-400 font-bold">0원</span> | 위시 총액: <span id="wishTotal" class="text-purple-400 font-bold">0원</span></p>
            </div>
            <button onclick="openAddModal()" class="bg-gradient-to-r from-cyan-400 to-blue-600 text-slate-950 text-xs font-black px-3.5 py-2 rounded-xl shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all flex items-center gap-1.5 active:scale-95 hover:shadow-[0_0_20px_rgba(34,211,238,0.5)]">
                <i class="fa-solid fa-plus text-[11px]"></i> 제품 추가
            </button>
        </div>
        <div class="mt-4 pt-3 border-t border-slate-800/60">
            <div class="flex justify-between text-[10px] text-slate-300 font-mono mb-1.5 items-center">
                <span class="flex items-center gap-1">
                    <i class="fa-solid fa-bullseye text-emerald-400"></i> 전역 셋업 예산금 (<span id="budgetText">0원 / 1,000,000원</span>) 
                    <button onclick="editBudget()" class="text-[9px] bg-slate-800 hover:bg-slate-700 text-cyan-400 px-2 py-0.5 rounded-lg border border-slate-700 ml-1 transition-colors"><i class="fa-solid fa-pen"></i> 수정</button>
                </span>
                <span id="budgetPercent" class="text-emerald-400 font-bold text-xs">0%</span>
            </div>
            <div class="w-full bg-slate-900/90 h-2.5 rounded-full overflow-hidden border border-slate-800/80 shadow-inner">
                <div id="budgetBar" class="bg-gradient-to-r from-cyan-400 to-emerald-400 h-full transition-all duration-700 ease-out shadow-[0_0_10px_rgba(16,185,129,0.5)]" style="width: 0%"></div>
            </div>
        </div>
    </header>
    
    <div class="px-5 pt-4 pb-2.5 flex gap-2 bg-slate-950/40 backdrop-blur-md border-b border-slate-900/50">
        <button onclick="switchView('main')" id="view-main" class="flex-1 py-2.5 rounded-xl bg-cyan-400 text-slate-950 font-black text-[11px] shadow-lg shadow-cyan-500/20 transition-all hover:opacity-90">보유 셋업</button>
        <button onclick="switchView('wishlist')" id="view-wishlist" class="flex-1 py-2.5 rounded-xl glass-card text-slate-300 font-bold text-[11px] border border-slate-700/50 transition-all hover:bg-slate-800/50">위시리스트</button>
        <button onclick="switchView('deals')" id="view-deals" class="flex-1 py-2.5 rounded-xl glass-card text-amber-400 font-bold text-[11px] border border-slate-700/50 transition-all hover:bg-slate-800/50">타임딜 & 쿠폰</button>
    </div>

    <div class="px-5 py-3 flex gap-2 overflow-x-auto scrollbar-none text-xs bg-transparent" id="catTabsContainer">
        <button onclick="filterCategory('전체')" id="tab-전체" class="category-btn px-4 py-2 rounded-xl bg-slate-800 text-cyan-400 font-black border border-cyan-500/40 transition-all shrink-0 shadow-lg shadow-cyan-500/10">전체보기</button>
        <button onclick="filterCategory('게이밍')" id="tab-게이밍" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition-all shrink-0 hover:text-white">게이밍</button>
        <button onclick="filterCategory('사무용')" id="tab-사무용" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition-all shrink-0 hover:text-white">사무용</button>
        <button onclick="filterCategory('공용')" id="tab-공용" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition-all shrink-0 hover:text-white">공용</button>
    </div>

    <main id="itemList" class="p-4 space-y-6 max-w-xl mx-auto"></main>
    
    <div id="toast" class="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50 hidden bg-slate-900/95 border border-emerald-500/50 text-white px-5 py-3.5 rounded-2xl shadow-2xl backdrop-blur-xl text-xs font-bold flex items-center gap-3 transition-all">
        <i id="toastIcon" class="fa-solid fa-circle-check text-emerald-400 text-base"></i>
        <span id="toastMessage" class="tracking-wide">메시지 내용</span>
    </div>

    <div id="budgetModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="glass-card w-full max-w-sm rounded-3xl p-6 relative border border-slate-700 shadow-2xl modal-enter">
            <div class="flex justify-between items-center mb-5 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-wallet text-cyan-400"></i> 총 예산금 설정</h3>
                <button onclick="closeBudgetModal()" class="text-slate-400 hover:text-white text-xl px-2 transition-colors"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-4 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1.5 font-bold">새로운 총 예산금 (원)</label>
                    <input type="number" id="budgetInputModal" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none font-mono font-bold focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all shadow-inner">
                </div>
                <div class="flex gap-3 pt-2">
                    <button onclick="saveBudgetModal()" class="bg-gradient-to-r from-cyan-400 to-blue-500 hover:opacity-90 text-slate-950 flex-1 py-3 rounded-xl font-black text-xs transition-all shadow-lg shadow-cyan-500/20">저장하기</button>
                    <button onclick="closeBudgetModal()" class="bg-slate-800 hover:bg-slate-700 text-white flex-1 py-3 rounded-xl text-xs font-bold transition-all border border-slate-700">취소</button>
                </div>
            </div>
        </div>
    </div>

    <div id="editModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="glass-card w-full max-w-sm rounded-3xl p-6 relative border border-slate-700 shadow-2xl modal-enter">
            <div class="flex justify-between items-center mb-5 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-pen text-cyan-400"></i> 가격 및 희망가 수정</h3>
                <button onclick="closeEditModal()" class="text-slate-400 hover:text-white text-xl px-2 transition-colors"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-4 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1.5 font-bold">현재 가격 (원)</label>
                    <input type="number" id="editPriceInput" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none font-mono font-bold focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all shadow-inner">
                </div>
                <div>
                    <label class="block text-emerald-400 mb-1.5 font-bold">희망 구매가 목표 (원)</label>
                    <input type="number" id="editTargetInput" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none font-mono font-bold focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-400 transition-all shadow-inner">
                </div>
                <div class="flex gap-3 pt-2">
                    <button onclick="saveEditedPrice()" class="bg-gradient-to-r from-cyan-400 to-blue-500 hover:opacity-90 text-slate-950 flex-1 py-3 rounded-xl font-black text-xs transition-all shadow-lg shadow-cyan-500/20">수정 완료</button>
                    <button onclick="closeEditModal()" class="bg-slate-800 hover:bg-slate-700 text-white flex-1 py-3 rounded-xl text-xs font-bold transition-all border border-slate-700">취소</button>
                </div>
            </div>
        </div>
    </div>

    <div id="addModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-md rounded-3xl p-6 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto modal-enter scrollbar-none" style="scrollbar-width: none;">
            <div class="flex justify-between items-center mb-5 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-circle-plus text-cyan-400"></i> 새 제품 등록</h3>
                <button onclick="closeAddModal()" class="text-slate-400 hover:text-white text-xl px-2 transition-colors"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <form id="addProductForm" onsubmit="submitNewProduct(event)" class="space-y-4 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1.5 font-bold">제품명</label>
                    <input type="text" id="addName" required class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all" placeholder="예: 로지텍 마우스">
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-slate-400 mb-1.5 font-bold">카테고리</label>
                        <select id="addCategory" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all">
                            <option value="게이밍">게이밍</option>
                            <option value="사무용">사무용</option>
                            <option value="공용">공용</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1.5 font-bold">분류 그룹</label>
                        <input type="text" id="addSubGroup" required class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all" placeholder="예: 마우스">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-slate-400 mb-1.5 font-bold">현재 가격 (원)</label>
                        <input type="number" id="addPrice" required class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all" placeholder="150000">
                    </div>
                    <div>
                        <label class="block text-emerald-400 mb-1.5 font-bold">희망 구매가 (원)</label>
                        <input type="number" id="addTargetPrice" required class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-400 transition-all" placeholder="130000">
                    </div>
                </div>
                <div>
                    <label class="block text-slate-400 mb-1.5 font-bold">최저가 검색 쿼리</label>
                    <input type="text" id="addQuery" required class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-400 transition-all" placeholder="예: 로지텍 마우스">
                </div>
                <div class="space-y-3 pt-2 border-t border-slate-800">
                    <div class="flex items-center gap-2">
                        <input type="checkbox" id="addWishlist" class="w-4 h-4 accent-cyan-400 rounded cursor-pointer">
                        <label for="addWishlist" class="text-slate-300 font-bold cursor-pointer">구매 예정 (위시리스트로 등록)</label>
                    </div>
                    <div class="flex items-center gap-2">
                        <input type="checkbox" id="addDeal" class="w-4 h-4 accent-amber-400 rounded cursor-pointer">
                        <label for="addDeal" class="text-amber-300 font-bold cursor-pointer">타임딜 및 특가 상품 등록</label>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <input type="number" id="addDiscount" placeholder="타임할인율(%)" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-400 transition-all">
                    <input type="text" id="addCoupon" placeholder="쿠폰명" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-400 transition-all">
                </div>
                <div>
                    <label class="block text-amber-400 mb-1.5 font-bold">타임딜 마감 일시</label>
                    <input type="datetime-local" id="addExpires" class="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl px-4 py-3 text-white outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-400 transition-all">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-cyan-400 to-emerald-500 text-slate-950 font-black py-3.5 rounded-xl shadow-lg mt-3 transition-all hover:opacity-90 tracking-widest text-sm">등록 완료</button>
            </form>
        </div>
    </div>

    <div id="chartModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4 transition-opacity">
        <div class="glass-card w-full max-w-lg rounded-3xl p-6 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto modal-enter scrollbar-none" style="scrollbar-width: none;">
            <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
                <h3 id="modalTitle" class="text-sm font-black text-white truncate pr-2">제품 상세 및 AI 팩트 체크</h3>
                <button onclick="closeChartModal()" class="text-slate-400 hover:text-white text-xl px-2 transition-colors"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <div class="mb-5">
                <label class="block text-purple-400 text-[11px] font-bold mb-2.5"><i class="fa-solid fa-wand-magic-sparkles"></i> AI 팩트 기반 가격 예측 및 타이밍 분석 (누적 메모리 & 전역 타임라인 반영)</label>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="openAiSearch('Gemini')" class="bg-blue-600 hover:bg-blue-500 text-white font-black py-3 rounded-xl text-xs shadow-md transition-all hover:shadow-[0_0_15px_rgba(37,99,235,0.5)] flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-gem"></i> Gemini
                    </button>
                    <button onclick="openAiSearch('ChatGPT')" class="bg-emerald-600 hover:bg-emerald-500 text-white font-black py-3 rounded-xl text-xs shadow-md transition-all hover:shadow-[0_0_15px_rgba(5,150,105,0.5)] flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-robot"></i> ChatGPT
                    </button>
                    <button onclick="openAiSearch('Perplexity')" class="bg-purple-600 hover:bg-purple-500 text-white font-black py-3 rounded-xl text-xs shadow-md transition-all hover:shadow-[0_0_15px_rgba(147,51,234,0.5)] flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-compass"></i> Perplexity
                    </button>
                </div>
            </div>
            
            <div class="relative w-full h-40 bg-slate-900/90 rounded-2xl p-3 border border-slate-700/80 shadow-inner mb-5">
                <canvas id="priceChart"></canvas>
            </div>

            <div class="pt-4 border-t border-slate-800">
                <h4 class="text-xs font-black text-cyan-400 mb-3 flex items-center gap-1.5">
                    <i class="fa-solid fa-star text-amber-400"></i> 추천 제품 풀 (인기 데스크 셋업)
                </h4>
                <div id="independentRecsList" class="space-y-2"></div>
            </div>
        </div>
    </div>

    <script>
        let items = [];
        let currentItem = null;
        let currentView = 'main';
        let currentFilter = '전체';
        let priceChartInstance = null;
        let editingItemId = null;
        const STORAGE_KEY = 'desk_setup_pro_v2_storage';
        
        let TOTAL_BUDGET = Number(localStorage.getItem('desk_budget')) || 1000000;

        function showToast(msg, isSuccess = true) {
            const toast = document.getElementById('toast');
            const messageEl = document.getElementById('toastMessage');
            const iconEl = document.getElementById('toastIcon');
            messageEl.textContent = msg;
            
            toast.classList.remove('hidden');
            toast.classList.remove('toast-enter');
            void toast.offsetWidth; 
            
            if(isSuccess) {
                iconEl.className = "fa-solid fa-circle-check text-emerald-400 text-sm";
                toast.className = "fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50 bg-slate-900/95 border border-emerald-500/50 text-white px-5 py-3.5 rounded-full shadow-2xl backdrop-blur-xl text-[11px] font-black flex items-center gap-2.5 transition-all toast-enter";
            } else {
                iconEl.className = "fa-solid fa-bullseye text-cyan-400 text-sm";
                toast.className = "fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50 bg-slate-900/95 border border-cyan-500/50 text-white px-5 py-3.5 rounded-full shadow-2xl backdrop-blur-xl text-[11px] font-black flex items-center gap-2.5 transition-all toast-enter";
            }
            
            setTimeout(() => { toast.classList.add('hidden'); }, 3000);
        }

        function editBudget() {
            document.getElementById('budgetInputModal').value = TOTAL_BUDGET;
            document.getElementById('budgetModal').classList.remove('hidden');
        }

        function closeBudgetModal() { document.getElementById('budgetModal').classList.add('hidden'); }

        function saveBudgetModal() {
            const val = Number(document.getElementById('budgetInputModal').value);
            if(!isNaN(val) && val > 0) {
                TOTAL_BUDGET = val;
                try { localStorage.setItem('desk_budget', TOTAL_BUDGET); } catch(e){}
                updateTotalsAndRender();
                closeBudgetModal();
                showToast("총 예산금이 성공적으로 변경되었습니다.");
            }
        }

        async function loadItems() {
            try {
                const savedData = localStorage.getItem(STORAGE_KEY);
                if (savedData) {
                    items = JSON.parse(savedData);
                } else {
                    const res = await fetch('/api/items');
                    items = await res.json();
                    items.forEach(i => { 
                        if(!i.target_price) i.target_price = Math.round(i.base_price * 0.9); 
                        if(!i.last_updated) i.last_updated = "등록일";
                    });
                    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); } catch(e){}
                }
                updateTotalsAndRender();
            } catch(e) { console.error("데이터 로드 오류:", e); }
        }

        function saveAndRender() {
            try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); } catch(e) { console.error("저장 공간 오류"); }
            updateTotalsAndRender();
        }

        function updateTotalsAndRender() {
            const total = items.filter(i => i.is_main && !i.is_bought).reduce((sum, i) => sum + i.base_price, 0);
            const wishTotal = items.filter(i => i.is_wishlist).reduce((sum, i) => sum + i.base_price, 0);
            const boughtTotal = items.filter(i => i.is_bought).reduce((sum, i) => sum + i.base_price, 0);
            
            document.getElementById('totalAsset').textContent = total.toLocaleString() + '원';
            document.getElementById('wishTotal').textContent = wishTotal.toLocaleString() + '원';

            const percent = Math.min(Math.round((boughtTotal / TOTAL_BUDGET) * 100), 100);
            document.getElementById('budgetText').textContent = `${boughtTotal.toLocaleString()}원 / ${TOTAL_BUDGET.toLocaleString()}원`;
            document.getElementById('budgetPercent').textContent = `${percent}%`;
            document.getElementById('budgetBar').style.width = `${percent}%`;

            render();
        }

        function toggleWishlist(id) {
            const item = items.find(i => i.id === id);
            if(item) {
                item.is_wishlist = !item.is_wishlist;
                saveAndRender();
                if(item.is_wishlist) showToast(`"${item.name}" 위시리스트 추가됨`);
            }
        }

        function toggleBuy(id) {
            const item = items.find(i => i.id === id);
            if(item) {
                item.is_bought = !item.is_bought;
                saveAndRender();
                if(item.is_bought) {
                    showToast(`"${item.name}" 구매 완료! 스탬프 획득.`);
                }
            }
        }

        function switchView(view) {
            currentView = view;
            const tabContainer = document.getElementById('catTabsContainer');
            
            const inactiveClass = "flex-1 py-2.5 rounded-xl glass-card text-slate-400 font-bold text-[11px] border border-slate-700/50 transition-all hover:bg-slate-800/50";
            
            document.getElementById('view-main').className = inactiveClass;
            document.getElementById('view-wishlist').className = inactiveClass;
            document.getElementById('view-deals').className = inactiveClass;

            if(view === 'main') {
                document.getElementById('view-main').className = "flex-1 py-2.5 rounded-xl bg-cyan-400 text-slate-950 font-black text-[11px] shadow-lg shadow-cyan-500/20 transition-all";
                tabContainer.style.display = 'flex';
            } else if(view === 'wishlist') {
                document.getElementById('view-wishlist').className = "flex-1 py-2.5 rounded-xl bg-purple-500 text-white font-black text-[11px] shadow-lg shadow-purple-500/20 transition-all";
                tabContainer.style.display = 'flex';
            } else {
                document.getElementById('view-deals').className = "flex-1 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-black text-[11px] shadow-lg shadow-amber-500/20 transition-all";
                tabContainer.style.display = 'none';
            }
            render();
        }

        function openAddModal() { document.getElementById('addModal').classList.remove('hidden'); }
        function closeAddModal() { document.getElementById('addModal').classList.add('hidden'); }

        function submitNewProduct(event) {
            event.preventDefault();
            const name = document.getElementById('addName').value;
            const category = document.getElementById('addCategory').value;
            const sub_group = document.getElementById('addSubGroup').value;
            const base_price = Number(document.getElementById('addPrice').value);
            const target_price = Number(document.getElementById('addTargetPrice').value);
            const query = document.getElementById('addQuery').value;
            const is_wishlist = document.getElementById('addWishlist').checked;
            const is_deal = document.getElementById('addDeal').checked;
            const discount_rate = Number(document.getElementById('addDiscount').value) || 0;
            const coupon_name = document.getElementById('addCoupon').value || '';
            const expires_at = document.getElementById('addExpires').value || '';

            const now = new Date();
            const todayStr = `${now.getMonth() + 1}월 ${now.getDate()}일`;

            const newId = items.length > 0 ? Math.max(...items.map(p => p.id)) + 1 : 1;
            const newProduct = {
                id: newId,
                is_main: !is_deal && !is_wishlist,
                is_wishlist: is_wishlist,
                is_deal: is_deal,
                is_bought: false,
                discount_rate: discount_rate,
                coupon_name: coupon_name,
                expires_at: expires_at,
                category: category,
                sub_group: sub_group,
                name: name,
                query: query,
                global_query: name,
                base_price: base_price,
                target_price: target_price,
                last_updated: todayStr,
                image: "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
                icon: "fa-box"
            };

            items.push(newProduct);
            saveAndRender();
            closeAddModal();
            document.getElementById('addProductForm').reset();
            showToast('새 제품이 성공적으로 추가되었습니다!');
        }

        function manualRecord(id) {
            const item = items.find(i => i.id === id);
            if(!item) return;
            editingItemId = id;
            document.getElementById('editPriceInput').value = item.base_price;
            document.getElementById('editTargetInput').value = item.target_price || 0;
            document.getElementById('editModal').classList.remove('hidden');
        }

        function closeEditModal() {
            document.getElementById('editModal').classList.add('hidden');
            editingItemId = null;
        }

        function saveEditedPrice() {
            if(editingItemId === null) return;
            const item = items.find(i => i.id === editingItemId);
            const newPrice = Number(document.getElementById('editPriceInput').value);
            const newTarget = Number(document.getElementById('editTargetInput').value);

            if(!isNaN(newPrice)) item.base_price = newPrice;
            if(!isNaN(newTarget)) item.target_price = newTarget;

            const now = new Date();
            item.last_updated = `${now.getMonth() + 1}월 ${now.getDate()}일`;

            saveAndRender();
            closeEditModal();

            if(item.target_price && item.base_price <= item.target_price) {
                showToast('🎯 희망 구매가 도달! 지금이 최적의 구매시기입니다.', false);
            } else {
                showToast('가격/희망가 및 변동 일자가 저장되었습니다.');
            }
        }

        function openAiSearch(aiName) {
            if(!currentItem) return;
            const contextKey = 'ai_context_' + currentItem.name;
            const previousHistory = localStorage.getItem(contextKey) || "이전 분석 기록 없음 (최초 분석)";

            const q = `[전문가 간결 분석 리포트]
제품명: '${currentItem.name}'
현재 등록가: ${currentItem.base_price.toLocaleString()}원 / 희망 구매가: ${(currentItem.target_price || 0).toLocaleString()}원
사용자 상황: 앞으로 1년 ~ 1년 4개월 내에 전역 전 최종 구매 완료 예정.

[이전 참고 맥락]
${previousHistory}

요청 사항: 
위 데이터를 바탕으로 가장 최근의 시장 동향(환율, 유통가 등)을 반영하여 아래 내용만 간결하게 핵심 위주로 요약해 주세요.
1. [현재 가격 평가]: 현재 가격이 적정한가?
2. [예상 타이밍]: 1년~1년 4개월 내 전역 전까지 가장 저렴해질 시점 (구체적 시기)
3. [최종 결론]: 지금 사야 하는가? 기다려야 하는가?`;

            try { localStorage.setItem(contextKey, `직전 분석가: ${currentItem.base_price}원, 목표가: ${currentItem.target_price || 0}원 반영됨.`); } catch(e){}

            let url = "";
            if(aiName === 'Gemini') url = `https://gemini.google.com/app?q=${encodeURIComponent(q)}`;
            else if(aiName === 'ChatGPT') url = `https://chatgpt.com/?q=${encodeURIComponent(q)}`;
            else if(aiName === 'Perplexity') url = `https://www.perplexity.ai/search?q=${encodeURIComponent(q)}`;
            window.open(url, '_blank');
        }

        async function openChartModal(item) {
            currentItem = item;
            document.getElementById('modalTitle').textContent = item.name;
            document.getElementById('chartModal').classList.remove('hidden');
            
            const historyDates = ['등록일', '현재'];
            const historyPrices = [item.base_price * 1.05, item.base_price];

            const ctx = document.getElementById('priceChart').getContext('2d');
            if(priceChartInstance) priceChartInstance.destroy();
            priceChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: historyDates,
                    datasets: [{ label: '가격 추이', data: historyPrices, borderColor: '#22d3ee', borderWidth: 2.5, tension: 0.2, fill: false }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', font: { size: 10 } } },
                        y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8', font: { size: 10 } } }
                    }
                }
            });

            const recRes = await fetch(`/api/recommendations?sub_group=${encodeURIComponent(item.sub_group)}`);
            const recs = await recRes.json();
            
            const recContainer = document.getElementById('independentRecsList');
            if(recs.length > 0) {
                recContainer.innerHTML = recs.map(rec => `
                    <div class="bg-slate-900/90 p-2.5 rounded-xl border border-slate-700/80 flex justify-between items-center transition-all hover:bg-slate-800">
                        <div class="flex items-center gap-2.5 truncate pr-2">
                            <img src="${rec.image}" class="w-8 h-8 object-cover rounded-lg shrink-0 border border-slate-600/50" onerror="this.style.display='none';">
                            <span class="text-xs font-bold text-slate-200 truncate">${rec.name}</span>
                        </div>
                        <span class="text-xs font-mono font-black text-cyan-400 shrink-0">${rec.base_price.toLocaleString()}원</span>
                    </div>
                `).join('');
            } else {
                recContainer.innerHTML = '<div class="text-[11px] text-slate-500 text-center py-3">추천 제품이 없습니다.</div>';
            }
        }

        function closeChartModal() { document.getElementById('chartModal').classList.add('hidden'); }

        function filterCategory(cat) { 
            currentFilter = cat; 
            ['전체', '게이밍', '사무용', '공용'].forEach(t => {
                const btn = document.getElementById('tab-' + t);
                if(btn) {
                    btn.className = (t === cat) ? "category-btn px-4 py-2 rounded-xl bg-slate-800 text-cyan-400 font-black border border-cyan-500/40 transition-all shrink-0 shadow-lg shadow-cyan-500/10" : "category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition-all shrink-0 hover:text-white";
                }
            });
            render(); 
        }

        function render() {
            const listEl = document.getElementById('itemList');
            let targetItems = [];
            if(currentView === 'main') targetItems = items.filter(i => i.is_main === true);
            else if(currentView === 'wishlist') targetItems = items.filter(i => i.is_wishlist === true);
            else targetItems = items.filter(i => i.is_deal === true);

            let salesBannerHTML = "";
            if(currentView === 'deals') {
                const now = new Date();
                const salesEvents = [
                    { name: "알리익스프레스 광군제", date: new Date('2026-11-11T00:00:00') },
                    { name: "블랙프라이데이", date: new Date('2026-11-27T00:00:00') },
                    { name: "연말 결산 감사제", date: new Date('2026-12-15T00:00:00') },
                    { name: "신년 맞이 특가전", date: new Date('2027-01-01T00:00:00') }
                ];
                
                salesBannerHTML = `
                <div class="glass-card rounded-2xl p-4 border border-amber-500/40 mb-4 bg-amber-950/10 shadow-[0_0_15px_rgba(245,158,11,0.05)]">
                    <h3 class="text-xs font-black text-amber-400 mb-3 flex items-center gap-1.5">
                        <i class="fa-solid fa-calendar-days"></i> 글로벌 대형 세일 예상 D-Day
                    </h3>
                    <div class="grid grid-cols-2 gap-2.5">
                        ${salesEvents.map(ev => {
                            const diffDays = Math.ceil((ev.date - now) / (1000 * 60 * 60 * 24));
                            return `
                                <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-700/80 flex justify-between items-center transition-all hover:bg-slate-800/80">
                                    <span class="text-[11px] font-bold text-slate-300 truncate pr-1">${ev.name}</span>
                                    <span class="text-xs font-mono font-black text-amber-400 shrink-0">${diffDays > 0 ? `D-${diffDays}` : '종료'}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
                `;
            }

            const filtered = (currentView === 'deals' || currentFilter === '전체') ? targetItems : targetItems.filter(i => i.category === currentFilter);
            const groups = [...new Set(filtered.map(i => i.sub_group))];
            
            if(groups.length === 0 && currentView !== 'deals') {
                listEl.innerHTML = salesBannerHTML + '<div class="text-center text-slate-500 py-20 text-xs font-bold bg-slate-900/30 rounded-2xl border border-slate-800 border-dashed">등록된 제품이 없습니다.</div>';
                return;
            }

            const nowTime = new Date().getTime();
            const itemsHTML = groups.map(g => {
                const groupItems = filtered.filter(i => i.sub_group === g);
                return `
                <div>
                    <h3 class="text-[11px] text-cyan-400 font-black uppercase tracking-widest mb-2.5 ml-1.5 flex items-center gap-1.5 drop-shadow-md">
                        <i class="fa-solid fa-layer-group text-[10px]"></i> ${g}
                    </h3>
                    <div class="grid grid-cols-2 gap-3">
                        ${groupItems.map(item => {
                            const naverLink = `https://msearch.shopping.naver.com/search/all?query=${encodeURIComponent(item.query)}`;
                            const danawaLink = `https://www.google.com/search?q=site:danawa.com+${encodeURIComponent(item.query)}`;
                            const amazonLink = `https://www.amazon.com/s?k=${encodeURIComponent(item.global_query)}`;
                            const aliLink = `https://ko.aliexpress.com/w/wholesale-${encodeURIComponent(item.global_query)}.html`;

                            const isPurchaseTime = item.target_price && item.base_price <= item.target_price;

                            let isUrgent = false;
                            if(item.is_deal && item.expires_at) {
                                const expTime = new Date(item.expires_at).getTime();
                                const diffHours = (expTime - nowTime) / (1000 * 60 * 60);
                                if(diffHours > 0 && diffHours <= 12) { isUrgent = true; }
                            }

                            let cardClass = "glass-card rounded-3xl overflow-hidden flex flex-col justify-between relative border border-slate-700/60 transition-all duration-300 hover:shadow-2xl hover:border-slate-600/80";
                            if(isUrgent) { 
                                cardClass = "glass-card rounded-3xl overflow-hidden urgent-border flex flex-col justify-between relative transition-all duration-300"; 
                            } else if(isPurchaseTime && !item.is_bought) {
                                cardClass = "glass-card rounded-3xl overflow-hidden purchase-glow-card flex flex-col justify-between relative transition-all duration-300";
                            }
                            
                            // 구매 완료 시 카드 자체는 모노톤 흑백 처리 (빨간 스탬프는 별도 유지)
                            if(item.is_bought) { cardClass += " grayscale opacity-70"; }

                            let finalPrice = item.base_price;
                            if(item.is_deal && item.discount_rate > 0) {
                                finalPrice = Math.round(item.base_price * (1 - item.discount_rate / 100));
                            }

                            return `
                            <div class="${cardClass}">
                                <!-- 강렬한 붉은색 스탬프 디자인 -->
                                ${item.is_bought ? '<div class="buy-stamp">BUY</div>' : ''}
                                
                                <!-- 타임딜 마감 배너 -->
                                ${isUrgent ? '<div class="absolute top-2.5 left-2.5 z-30 bg-red-600 text-white text-[9px] font-black px-2.5 py-1 rounded-full shadow-lg animate-bounce">⏰ 마감임박</div>' : (item.is_deal && item.discount_rate > 0 ? `<div class="absolute top-2.5 left-2.5 z-20 bg-amber-500 text-slate-950 text-[9px] font-black px-2.5 py-1 rounded-full shadow-lg">🔥 특가 -${item.discount_rate}%</div>` : '')}
                                
                                <div class="w-full h-32 bg-slate-900/90 overflow-hidden border-b border-slate-800/80 relative flex items-center justify-center p-2.5 cursor-pointer group" onclick='openChartModal(${JSON.stringify(item)})'>
                                    <img src="${item.image}" class="w-full h-full object-cover rounded-2xl group-hover:scale-105 transition-transform duration-500" alt="${item.name}" onerror="this.style.display='none';">
                                    
                                    <!-- 위시리스트(하트) 독립 배치 -->
                                    <div class="absolute top-2.5 right-2.5 z-20" onclick="event.stopPropagation();">
                                        <button onclick="toggleWishlist(${item.id})" class="bg-slate-950/80 hover:bg-slate-900 p-2 rounded-full shadow-md transition-all active:scale-95 border border-slate-800/50 flex items-center justify-center">
                                            <i class="fa-${item.is_wishlist ? 'solid text-rose-500' : 'regular text-slate-400'} fa-heart text-sm"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="p-3.5 cursor-pointer flex flex-col justify-between" onclick='openChartModal(${JSON.stringify(item)})'>
                                    <div>
                                        <h3 class="text-xs font-black text-white tracking-tight truncate">${item.name}</h3>
                                        
                                        ${(isPurchaseTime && !item.is_bought) ? '<div class="my-1.5 bg-emerald-500/20 border border-emerald-500/50 text-emerald-400 text-[10px] font-black px-2 py-1 rounded-lg flex items-center justify-center gap-1.5 shadow-[0_0_10px_rgba(16,185,129,0.2)] animate-pulse whitespace-nowrap"><i class="fa-solid fa-bullseye"></i> 🎯 구매시기 도달! (최적가)</div>' : ''}
                                        
                                        ${item.target_price ? `<div class="mt-1.5 text-[10px] text-emerald-400 font-mono font-bold">희망가: ${item.target_price.toLocaleString()}원</div>` : '<div></div>'}
                                        ${item.is_deal && item.coupon_name ? `<div class="text-[10px] text-amber-300 font-bold truncate mt-1 bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/30 w-fit"><i class="fa-solid fa-ticket"></i> ${item.coupon_name}</div>` : ''}
                                    </div>
                                    
                                    <!-- 구매 및 가격 변경 버튼, 그리고 날짜 배치 -->
                                    <div class="flex flex-col gap-2.5 mt-2.5 border-t border-slate-700/50 pt-3">
                                        
                                        <!-- 가격과 날짜가 한 줄에 나오도록 배치 -->
                                        <div class="flex items-baseline gap-1.5 truncate">
                                            ${item.is_deal && item.discount_rate > 0 ? `<span class="text-[9px] text-slate-400 line-through mr-1">${item.base_price.toLocaleString()}원</span>` : ''}
                                            <span class="text-[13px] font-mono font-black text-cyan-400 drop-shadow-md leading-none">${finalPrice.toLocaleString()}원</span>
                                            <span class="text-[9px] text-slate-400 font-mono leading-none tracking-tight">${item.last_updated ? item.last_updated.replace(' 변동', '') : '등록일'}</span>
                                        </div>

                                        <!-- 알약 형태의 세련된 조작 버튼들 -->
                                        <div class="flex gap-1.5" onclick="event.stopPropagation();">
                                            <button onclick="toggleBuy(${item.id})" class="bg-emerald-500/20 hover:bg-emerald-500/40 text-emerald-400 text-[10px] font-black px-2 py-1.5 rounded-md shadow-sm transition-all active:scale-95 border border-emerald-500/30 flex items-center justify-center gap-1 flex-1">
                                                <i class="fa-solid fa-check"></i> ${item.is_bought ? '구매 취소' : '구매 완료'}
                                            </button>
                                            <button onclick="manualRecord(${item.id})" class="bg-cyan-500/20 hover:bg-cyan-500/40 text-cyan-400 text-[10px] font-black px-2 py-1.5 rounded-md shadow-sm transition-all active:scale-95 border border-cyan-500/30 flex items-center justify-center gap-1 flex-1">
                                                <i class="fa-solid fa-pen"></i> 수정
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="p-2 bg-slate-900/50 grid grid-cols-2 gap-1.5 border-t border-slate-800/80 text-center">
                                    <a href="${naverLink}" target="_blank" class="py-2 bg-[#03C75A]/10 hover:bg-[#03C75A]/20 text-[#03C75A] rounded-xl text-[10px] font-black flex items-center justify-center gap-1.5 transition-all border border-[#03C75A]/20 hover:border-[#03C75A]/50">
                                        <i class="fa-solid fa-n"></i> 네이버
                                    </a>
                                    <a href="${danawaLink}" target="_blank" class="py-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 rounded-xl text-[10px] font-black flex items-center justify-center gap-1.5 transition-all border border-blue-500/20 hover:border-blue-500/50">
                                        <i class="fa-solid fa-d"></i> 다나와
                                    </a>
                                    <a href="${amazonLink}" target="_blank" class="py-2 bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 rounded-xl text-[10px] font-black flex items-center justify-center gap-1.5 transition-all border border-amber-500/20 hover:border-amber-500/50">
                                        <i class="fa-brands fa-amazon"></i> 아마존
                                    </a>
                                    <a href="${aliLink}" target="_blank" class="py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 rounded-xl text-[10px] font-black flex items-center justify-center gap-1.5 transition-all border border-rose-500/20 hover:border-rose-500/50">
                                        <i class="fa-solid fa-bag-shopping"></i> 알리
                                    </a>
                                </div>
                            </div>
                            `;
                        }).join('')}
                    </div>
                </div>
                `;
            }).join('');

            listEl.innerHTML = salesBannerHTML + itemsHTML;
        }
        loadItems();
    </script>
</body>
</html>
