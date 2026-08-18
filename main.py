import os
import json
import threading
import webbrowser
import uvicorn
import requests
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Desk Setup AI Tracker Master Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY_FILE = "price_history_master.json"
PRODUCTS_FILE = "products_master_final.json"
RECOMMENDATIONS_FILE = "recommendations_master.json"

# Render 환경 변수에서 API 키를 안전하게 불러옴
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MASTER_ITEMS = [
    {"id": 1, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마우스", "name": "Razer Basilisk V3 Pro 35K", "query": "Razer Basilisk V3 Pro 35K", "global_query": "Razer Basilisk V3 Pro 35K", "base_price": 239000, "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800", "icon": "fa-computer-mouse"},
    {"id": 2, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "이어폰", "name": "AZLA SednaEarfit Azel Edition G Gen 3", "query": "아즈라 아젤 에디션 G 3세대", "global_query": "AZLA SednaEarfit Azel Edition G Gen 3", "base_price": 89100, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800", "icon": "fa-headphones"},
    {"id": 3, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마이크", "name": "Maono DM40 Pro", "query": "마오노 DM40 Pro", "global_query": "Maono DM40 Pro", "base_price": 139000, "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800", "icon": "fa-microphone"},
    {"id": 4, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "마이크", "name": "Maono PD200X", "query": "마오노 PD200X", "global_query": "Maono PD200X", "base_price": 89160, "image": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800", "icon": "fa-microphone"},
    {"id": 5, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "오디오 인터페이스", "name": "Maonocaster G1 NEO", "query": "마오노 G1 NEO", "global_query": "Maonocaster G1 NEO", "base_price": 63850, "image": "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=800", "icon": "fa-sliders"},
    {"id": 6, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "게이밍", "sub_group": "키보드/스트림덱", "name": "Elgato Stream Deck Neo", "query": "엘가토 스트림덱 네오", "global_query": "Elgato Stream Deck Neo", "base_price": 133300, "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800", "icon": "fa-keyboard"},
    {"id": 7, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "사무용", "sub_group": "마우스", "name": "Logitech MX Master 4", "query": "로지텍 MX master 4", "global_query": "Logitech MX Master 4", "base_price": 179000, "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800", "icon": "fa-computer-mouse"},
    {"id": 8, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "스피커", "name": "Edifier MR4", "query": "edifier mr4", "global_query": "Edifier MR4", "base_price": 76410, "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800", "icon": "fa-volume-high"},
    {"id": 9, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "포터블 모니터", "name": "Zeuslap Z16P", "query": "제우스랩 Z16P", "global_query": "Zeuslap Z16P", "base_price": 150700, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800", "icon": "fa-display"},
    {"id": 10, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "마우스 패드", "name": "Glorious GMP2 XXL White", "query": "글로리어스 GMP2 화이트 XXL", "global_query": "Glorious GMP2 XXL White", "base_price": 49900, "image": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=800", "icon": "fa-square"},
    {"id": 11, "is_main": True, "is_wishlist": False, "is_deal": False, "is_bought": False, "category": "공용", "sub_group": "데스크 선반", "name": "Desk Shelf (White/Wood)", "query": "데스크 선반 모니터 받침대 원목", "global_query": "Desk Shelf Monitor Stand Timber", "base_price": 30000, "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800", "icon": "fa-table"}
]

RECOMMENDATION_POOL = [
    {"id": 101, "name": "Logitech G Pro X Superlight 2", "sub_group": "마우스", "base_price": 199000, "image": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800"},
    {"id": 102, "name": "Keychron Q1 Pro 무선 키보드", "sub_group": "키보드/스트림덱", "base_price": 229000, "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"},
    {"id": 103, "name": "Sony WH-1000XM5 헤드셋", "sub_group": "이어폰", "base_price": 479000, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"},
    {"id": 104, "name": "Bose Companion 2 Series III 스피커", "sub_group": "스피커", "base_price": 149000, "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"},
    {"id": 105, "name": "Dell UltraSharp U2723QE 모니터", "sub_group": "포터블 모니터", "base_price": 750000, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"}
]

def init_files():
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(MASTER_ITEMS, f, ensure_ascii=False, indent=4)
    if not os.path.exists(RECOMMENDATIONS_FILE):
        with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(RECOMMENDATION_POOL, f, ensure_ascii=False, indent=4)

def load_products():
    init_files()
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return MASTER_ITEMS

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

def load_recommendations():
    init_files()
    try:
        with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return RECOMMENDATION_POOL

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_history(history_data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

@app.on_event("startup")
async def startup_event():
    init_files()
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

@app.get("/api/items")
async def get_items():
    return load_products()

@app.get("/api/recommendations")
async def get_recommendations(sub_group: str = Query(...)):
    recs = load_recommendations()
    matched = [r for r in recs if r["sub_group"] == sub_group]
    if not matched:
        matched = recs[:3]
    return matched

# Bearer 인증 방식으로 수정된 AI 분석 엔드포인트
@app.get("/api/ai-analyze/{item_id}")
async def ai_analyze(item_id: int):
    products = load_products()
    item = next((i for i in products if i["id"] == item_id), None)
    if not item:
        return {"status": "error", "message": "제품을 찾을 수 없습니다."}

    if not GEMINI_API_KEY:
        return {"status": "error", "message": "API 키가 설정되지 않았습니다."}

    # Bearer 토큰(AQ 키 포함)을 위한 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}" 
    }
    
    prompt = f"""
    당신은 전문 IT 장비 및 유통 시장 애널리스트입니다.
    분석 대상 제품: {item['name']}
    기준 가격: {item['base_price']:,}원

    JSON 형식으로만 답변하세요.
    {{
      "trend": "UP 또는 DOWN",
      "keywords": ["키워드1", "키워드2"],
      "future_prediction": "예상 가격(숫자만)",
      "purchase_timing": "구매시기 추천",
      "evidence": "근거 설명"
    }}
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"googleSearch": {}}]
    }

    models_to_try = ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
    
    response_data = None
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                res_json = res.json()
                text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                text = text.replace("```json", "").replace("```", "").strip()
                response_data = json.loads(text)
                break
        except Exception:
            continue

    if not response_data:
        return {"status": "error", "message": "AI 서버 통신 실패 (토큰 형식을 확인하세요)"}

    return {"status": "success", "data": response_data}

@app.post("/api/toggle-wishlist")
async def toggle_wishlist(item_id: int = Query(...)):
    products = load_products()
    for p in products:
        if p["id"] == item_id:
            p["is_wishlist"] = not p.get("is_wishlist", False)
    save_products(products)
    return {"status": "success"}

@app.post("/api/toggle-buy")
async def toggle_buy(item_id: int = Query(...)):
    products = load_products()
    for p in products:
        if p["id"] == item_id:
            p["is_bought"] = not p.get("is_bought", False)
    save_products(products)
    return {"status": "success"}

@app.post("/api/add-item")
async def add_item(
    name: str = Query(...),
    category: str = Query(...),
    sub_group: str = Query("기타"),
    base_price: int = Query(...),
    query: str = Query(...),
    is_wishlist: bool = Query(False),
    is_deal: bool = Query(False),
    discount_rate: int = Query(0),
    coupon_name: str = Query(""),
    expires_at: str = Query("")
):
    products = load_products()
    new_id = max([p["id"] for p in products], default=0) + 1
    new_product = {
        "id": new_id,
        "is_main": not is_deal and not is_wishlist,
        "is_wishlist": is_wishlist,
        "is_deal": is_deal,
        "is_bought": False,
        "discount_rate": discount_rate,
        "coupon_name": coupon_name,
        "expires_at": expires_at,
        "category": category,
        "sub_group": sub_group,
        "name": name,
        "query": query,
        "global_query": name,
        "base_price": base_price,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
        "icon": "fa-box"
    }
    products.append(new_product)
    save_products(products)
    return {"status": "success", "id": new_id}

@app.post("/api/record-price")
async def record_price(item_id: int = Query(...), price: int = Query(...)):
    history_db = load_history()
    products = load_products()
    str_id = str(item_id)
    
    if str_id not in history_db or not isinstance(history_db[str_id], dict):
        history_db[str_id] = {"history": []}
        
    target_item = next((i for i in products if i["id"] == item_id), None)
    if not target_item:
        return {"status": "error"}

    target_item["base_price"] = price
    save_products(products)

    now_date_str = datetime.now().strftime("%Y-%m-%d")
    now_full_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    item_history = history_db[str_id]["history"]
    if item_history and item_history[-1]["date"].startswith(now_date_str):
        item_history[-1]["date"] = now_full_str
        item_history[-1]["user_price"] = price
        item_history[-1]["ai_price"] = price
    else:
        item_history.append({"date": now_full_str, "user_price": price, "ai_price": price})
        
    history_db[str_id]["history"] = item_history
    save_history(history_db)
    return {"status": "success"}

@app.get("/", response_class=HTMLResponse)
async def serve_mobile_ui():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DESK SETUP AI TRACKER MASTER</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { -webkit-tap-highlight-color: transparent; background-color: #030712; }
        .glass-card { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }
        @keyframes urgent-glow {
            0% { border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.7); }
            50% { border-color: #ef4444; box-shadow: 0 0 25px rgba(239, 68, 68, 0.9); }
            100% { border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.7); }
        }
        .urgent-border { animation: urgent-glow 1.5s infinite linear; border-width: 2px !important; }
        .buy-stamp {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-15deg);
            border: 4px solid #ef4444; color: #ef4444; font-weight: 900; font-size: 2rem; padding: 4px 16px;
            letter-spacing: 2px; text-transform: uppercase; pointer-events: none; z-index: 30; opacity: 0.85;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.5); border-radius: 8px;
        }
    </style>
</head>
<body class="text-slate-100 min-h-screen pb-24 font-sans selection:bg-cyan-500/30">
    <header class="sticky top-0 z-30 bg-slate-950/90 backdrop-blur-xl border-b border-slate-800 px-5 py-4 shadow-md flex justify-between items-center">
        <div>
            <h1 class="text-lg font-black text-white flex items-center gap-2 tracking-tight font-mono">
                <i class="fa-solid fa-server text-cyan-400"></i> DESK SETUP PRO
            </h1>
            <p class="text-[11px] text-slate-400 font-mono mt-0.5">보유 자산 총액: <span id="totalAsset" class="text-cyan-400 font-bold">0원</span> | 위시 총액: <span id="wishTotal" class="text-purple-400 font-bold">0원</span></p>
        </div>
        <button onclick="openAddModal()" class="bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 text-xs font-black px-3.5 py-2 rounded-xl shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-1.5 active:scale-95">
            <i class="fa-solid fa-plus text-[11px]"></i> 장비 등록
        </button>
    </header>
    
    <div class="px-5 pt-3.5 pb-2 flex gap-2 bg-slate-950/80 border-b border-slate-900">
        <button onclick="switchView('main')" id="view-main" class="flex-1 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-black text-[11px] shadow-lg shadow-cyan-500/20 transition">보유 셋업</button>
        <button onclick="switchView('wishlist')" id="view-wishlist" class="flex-1 py-2.5 rounded-xl glass-card text-slate-400 font-bold text-[11px] border border-slate-800 transition">위시리스트</button>
        <button onclick="switchView('deals')" id="view-deals" class="flex-1 py-2.5 rounded-xl glass-card text-amber-400 font-bold text-[11px] border border-slate-800 transition">타임딜 & 쿠폰</button>
    </div>

    <div class="px-5 py-2.5 flex gap-2 overflow-x-auto scrollbar-none text-xs bg-slate-950/60 border-b border-slate-900" id="catTabsContainer">
        <button onclick="filterCategory('전체')" id="tab-전체" class="category-btn px-4 py-2 rounded-xl bg-slate-800 text-cyan-400 font-black border border-cyan-500/40 transition shrink-0">전체보기</button>
        <button onclick="filterCategory('게이밍')" id="tab-게이밍" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition shrink-0">게이밍</button>
        <button onclick="filterCategory('사무용')" id="tab-사무용" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition shrink-0">사무용</button>
        <button onclick="filterCategory('공용')" id="tab-공용" class="category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition shrink-0">공용</button>
    </div>

    <main id="itemList" class="p-4 space-y-6 max-w-xl mx-auto"></main>
    
    <!-- 장비 등록 모달 -->
    <div id="addModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-md rounded-3xl p-5 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-circle-plus text-cyan-400"></i> 장비 / 특가 등록</h3>
                <button onclick="closeAddModal()" class="text-slate-400 hover:text-white text-lg px-2"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <form id="addProductForm" onsubmit="submitNewProduct(event)" class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">제품명</label>
                    <input type="text" id="addName" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 로지텍 G102">
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="block text-slate-400 mb-1 font-bold">카테고리</label>
                        <select id="addCategory" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none">
                            <option value="게이밍">게이밍</option>
                            <option value="사무용">사무용</option>
                            <option value="공용">공용</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1 font-bold">서브 그룹</label>
                        <input type="text" id="addSubGroup" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 마우스">
                    </div>
                </div>
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">가격 (원)</label>
                    <input type="number" id="addPrice" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 35000">
                </div>
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">검색 쿼리</label>
                    <input type="text" id="addQuery" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 로지텍 G102">
                </div>
                <div class="space-y-2 pt-1 border-t border-slate-800">
                    <div class="flex items-center gap-2">
                        <input type="checkbox" id="addWishlist" class="w-4 h-4 accent-cyan-500 rounded">
                        <label for="addWishlist" class="text-slate-300 font-bold cursor-pointer">구매 예정 (위시리스트)</label>
                    </div>
                    <div class="flex items-center gap-2">
                        <input type="checkbox" id="addDeal" class="w-4 h-4 accent-amber-500 rounded">
                        <label for="addDeal" class="text-amber-300 font-bold cursor-pointer">타임딜 및 특가 상품 등록</label>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="addDiscount" placeholder="타임할인율(%)" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white outline-none">
                    <input type="text" id="addCoupon" placeholder="쿠폰명" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white outline-none">
                </div>
                <div>
                    <label class="block text-amber-400 mb-1 font-bold">타임딜 마감 일시 (12시간 전 자동 긴급 알림 강조)</label>
                    <input type="datetime-local" id="addExpires" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black py-3 rounded-xl shadow-lg mt-2 transition">제품 등록 완료</button>
            </form>
        </div>
    </div>

    <!-- 그래프, AI 분석 리포트 및 추천 상품 모달 -->
    <div id="chartModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-lg rounded-3xl p-5 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-3 border-b border-slate-800 pb-3">
                <h3 id="modalTitle" class="text-sm font-black text-white truncate pr-2">제품 상세 및 AI 분석 리포트</h3>
                <button onclick="closeChartModal()" class="text-slate-400 hover:text-white text-lg px-2"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <!-- 실시간 AI 분석 호출 버튼 -->
            <button id="aiAnalyzeBtn" onclick="runAiAnalysis()" class="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:opacity-90 text-white font-black py-3 rounded-xl shadow-lg transition mb-3 flex items-center justify-center gap-2 text-xs">
                <i class="fa-solid fa-wand-magic-sparkles"></i> Gemini 실시간 미래 가격 예상 및 구매시기 분석
            </button>

            <!-- AI 분석 결과 출력 박스 -->
            <div id="aiResultBox" class="hidden mb-3 rounded-2xl p-4 border text-xs shadow-inner transition-all duration-300">
                <div class="flex justify-between items-center mb-2">
                    <span id="aiKeywords" class="text-[10px] font-mono font-bold bg-black/30 px-2 py-0.5 rounded">키워드: -</span>
                    <span class="font-mono text-[11px]">예상가: <strong id="aiFuturePrice" class="text-sm">-</strong></span>
                </div>
                <div class="space-y-2 mt-2 pt-2 border-t border-white/20">
                    <div>
                        <strong class="block text-[11px] opacity-90 mb-0.5">💡 적정 구매시기 추천</strong>
                        <p id="aiTimingText" class="text-xs leading-relaxed font-semibold"></p>
                    </div>
                    <div>
                        <strong class="block text-[11px] opacity-90 mb-0.5">📊 확실한 변동 근거 (부품/뉴스/경쟁)</strong>
                        <p id="aiEvidenceText" class="text-[11px] leading-relaxed opacity-95"></p>
                    </div>
                </div>
            </div>
            
            <div class="relative w-full h-40 bg-slate-900/80 rounded-2xl p-3 border border-slate-800 shadow-inner mb-4">
                <canvas id="priceChart"></canvas>
            </div>

            <div class="pt-3 border-t border-slate-800">
                <h4 class="text-xs font-black text-cyan-400 mb-2.5 flex items-center gap-1.5">
                    <i class="fa-solid fa-star text-amber-400"></i> 독립 추천 풀에서 가져온 동급 인기기기 추천
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

        async function loadItems() {
            try {
                const res = await fetch('/api/items');
                items = await res.json();
                
                const total = items.filter(i => i.is_main && !i.is_bought).reduce((sum, i) => sum + i.base_price, 0);
                const wishTotal = items.filter(i => i.is_wishlist).reduce((sum, i) => sum + i.base_price, 0);
                
                document.getElementById('totalAsset').textContent = total.toLocaleString() + '원';
                document.getElementById('wishTotal').textContent = wishTotal.toLocaleString() + '원';
                render();
            } catch(e) { console.error(e); }
        }

        async function toggleWishlist(id) {
            await fetch(`/api/toggle-wishlist?item_id=${id}`, { method: 'POST' });
            await loadItems();
        }

        async function toggleBuy(id) {
            await fetch(`/api/toggle-buy?item_id=${id}`, { method: 'POST' });
            await loadItems();
        }

        function switchView(view) {
            currentView = view;
            const tabContainer = document.getElementById('catTabsContainer');
            
            document.getElementById('view-main').className = "flex-1 py-2.5 rounded-xl glass-card text-slate-400 font-bold text-[11px] border border-slate-800 transition";
            document.getElementById('view-wishlist').className = "flex-1 py-2.5 rounded-xl glass-card text-slate-400 font-bold text-[11px] border border-slate-800 transition";
            document.getElementById('view-deals').className = "flex-1 py-2.5 rounded-xl glass-card text-amber-400 font-bold text-[11px] border border-slate-800 transition";

            if(view === 'main') {
                document.getElementById('view-main').className = "flex-1 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-black text-[11px] shadow-lg shadow-cyan-500/20 transition";
                tabContainer.style.display = 'flex';
            } else if(view === 'wishlist') {
                document.getElementById('view-wishlist').className = "flex-1 py-2.5 rounded-xl bg-purple-600 text-white font-black text-[11px] shadow-lg shadow-purple-500/20 transition";
                tabContainer.style.display = 'flex';
            } else {
                document.getElementById('view-deals').className = "flex-1 py-2.5 rounded-xl bg-amber-500 text-slate-950 font-black text-[11px] shadow-lg shadow-amber-500/20 transition";
                tabContainer.style.display = 'none';
            }
            render();
        }

        function openAddModal() { document.getElementById('addModal').classList.remove('hidden'); }
        function closeAddModal() { document.getElementById('addModal').classList.add('hidden'); }

        async function submitNewProduct(event) {
            event.preventDefault();
            const name = encodeURIComponent(document.getElementById('addName').value);
            const category = encodeURIComponent(document.getElementById('addCategory').value);
            const sub_group = encodeURIComponent(document.getElementById('addSubGroup').value);
            const base_price = document.getElementById('addPrice').value;
            const query = encodeURIComponent(document.getElementById('addQuery').value);
            const is_wishlist = document.getElementById('addWishlist').checked;
            const is_deal = document.getElementById('addDeal').checked;
            const discount_rate = document.getElementById('addDiscount').value || 0;
            const coupon_name = encodeURIComponent(document.getElementById('addCoupon').value || '');
            const expires_at = encodeURIComponent(document.getElementById('addExpires').value || '');

            const url = `/api/add-item?name=${name}&category=${category}&sub_group=${sub_group}&base_price=${base_price}&query=${query}&is_wishlist=${is_wishlist}&is_deal=${is_deal}&discount_rate=${discount_rate}&coupon_name=${coupon_name}&expires_at=${expires_at}`;
            const res = await fetch(url, { method: 'POST' });
            if((await res.json()).status === 'success') {
                closeAddModal();
                document.getElementById('addProductForm').reset();
                await loadItems();
                alert('장비가 성공적으로 등록되었습니다!');
            }
        }

        async function manualRecord(id) {
            const item = items.find(i => i.id === id);
            const val = prompt("현재 시장 정가 입력 (원 단위):", item ? item.base_price : "");
            if(val && !isNaN(val)) {
                const res = await fetch(`/api/record-price?item_id=${id}&price=${val}`, { method: 'POST' });
                if((await res.json()).status === 'success') {
                    await loadItems();
                    alert('가격이 기록되었습니다.');
                }
            }
        }

        async function openChartModal(item) {
            currentItem = item;
            document.getElementById('modalTitle').textContent = item.name;
            document.getElementById('aiResultBox').classList.add('hidden');
            document.getElementById('chartModal').classList.remove('hidden');
            
            const historyDates = ['초기 등록', '현재'];
            const historyPrices = [item.base_price * 0.98, item.base_price];

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
                    <div class="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 flex justify-between items-center">
                        <div class="flex items-center gap-2.5 truncate pr-2">
                            <img src="${rec.image}" class="w-8 h-8 object-cover rounded-lg shrink-0 border border-slate-700/60" onerror="this.style.display='none';">
                            <span class="text-xs font-bold text-slate-200 truncate">${rec.name}</span>
                        </div>
                        <span class="text-xs font-mono font-black text-cyan-400 shrink-0">${rec.base_price.toLocaleString()}원</span>
                    </div>
                `).join('');
            } else {
                recContainer.innerHTML = '<div class="text-[11px] text-slate-500 text-center py-2">독립 추천 풀에 데이터가 없습니다.</div>';
            }
        }

        async function runAiAnalysis() {
            if(!currentItem) return;
            const btn = document.getElementById('aiAnalyzeBtn');
            const resultBox = document.getElementById('aiResultBox');
            
            btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> 실시간 부품 및 시장 분석 중...`;
            btn.disabled = true;

            try {
                const res = await fetch(`/api/ai-analyze/${currentItem.id}`);
                const json = await res.json();
                
                if(json.status === 'success') {
                    const data = json.data;
                    document.getElementById('aiKeywords').textContent = "키워드: " + data.keywords.join(', ');
                    document.getElementById('aiFuturePrice').textContent = Number(data.future_prediction).toLocaleString() + '원';
                    document.getElementById('aiTimingText').textContent = data.purchase_timing;
                    document.getElementById('aiEvidenceText').textContent = data.evidence;

                    if(data.trend === 'UP') {
                        resultBox.className = "mb-3 rounded-2xl p-4 border text-xs shadow-inner bg-red-950/90 border-red-500/60 text-red-100 transition-all duration-300";
                    } else {
                        resultBox.className = "mb-3 rounded-2xl p-4 border text-xs shadow-inner bg-blue-950/90 border-blue-500/60 text-blue-100 transition-all duration-300";
                    }
                    resultBox.classList.remove('hidden');
                } else {
                    alert(json.message);
                }
            } catch(e) {
                alert('통신 오류가 발생했습니다.');
            } finally {
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Gemini 실시간 미래 가격 예상 및 구매시기 분석`;
                btn.disabled = false;
            }
        }

        function closeChartModal() { document.getElementById('chartModal').classList.add('hidden'); }

        function filterCategory(cat) { 
            currentFilter = cat; 
            ['전체', '게이밍', '사무용', '공용'].forEach(t => {
                const btn = document.getElementById('tab-' + t);
                if(btn) {
                    btn.className = (t === cat) ? "category-btn px-4 py-2 rounded-xl bg-slate-800 text-cyan-400 font-black border border-cyan-500/40 transition shrink-0" : "category-btn px-4 py-2 rounded-xl glass-card text-slate-400 font-bold border border-slate-800 transition shrink-0";
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

            const filtered = (currentView === 'deals' || currentFilter === '전체') ? targetItems : targetItems.filter(i => i.category === currentFilter);
            const groups = [...new Set(filtered.map(i => i.sub_group))];
            
            if(groups.length === 0) {
                listEl.innerHTML = '<div class="text-center text-slate-500 py-16 text-xs">등록된 장비가 없습니다.</div>';
                return;
            }

            const nowTime = new Date().getTime();
            listEl.innerHTML = groups.map(g => {
                const groupItems = filtered.filter(i => i.sub_group === g);
                return `
                <div>
                    <h3 class="text-[11px] text-cyan-400 font-black uppercase tracking-wider mb-2.5 ml-1 flex items-center gap-1.5">
                        <i class="fa-solid fa-layer-group text-[10px]"></i> ${g} 그룹
                    </h3>
                    <div class="grid grid-cols-2 gap-3">
                        ${groupItems.map(item => {
                            const naverLink = `https://msearch.shopping.naver.com/search/all?query=${encodeURIComponent(item.query)}`;
                            const danawaLink = `https://www.google.com/search?q=site:danawa.com+${encodeURIComponent(item.query)}`;
                            const amazonLink = `https://www.amazon.com/s?k=${encodeURIComponent(item.global_query)}`;
                            const aliLink = `https://ko.aliexpress.com/w/wholesale-${encodeURIComponent(item.global_query)}.html`;

                            let isUrgent = false;
                            if(item.is_deal && item.expires_at) {
                                const expTime = new Date(item.expires_at).getTime();
                                const diffHours = (expTime - nowTime) / (1000 * 60 * 60);
                                if(diffHours > 0 && diffHours <= 12) { isUrgent = true; }
                            }

                            let cardClass = "glass-card rounded-2xl overflow-hidden flex flex-col justify-between relative border border-slate-800";
                            if(isUrgent) { cardClass = "glass-card rounded-2xl overflow-hidden urgent-border flex flex-col justify-between relative"; }
                            if(item.is_bought) { cardClass += " grayscale opacity-60"; }

                            let finalPrice = item.base_price;
                            if(item.is_deal && item.discount_rate > 0) {
                                finalPrice = Math.round(item.base_price * (1 - item.discount_rate / 100));
                            }

                            return `
                            <div class="${cardClass}">
                                ${item.is_bought ? '<div class="buy-stamp">BUY</div>' : ''}
                                ${isUrgent ? '<div class="absolute top-2 left-2 z-30 bg-red-600 text-white text-[9px] font-black px-2 py-0.5 rounded-full shadow-lg animate-bounce">⏰ 마감 12시간 전!</div>' : (item.is_deal && item.discount_rate > 0 ? `<div class="absolute top-2 left-2 z-20 bg-amber-500 text-slate-950 text-[9px] font-black px-2 py-0.5 rounded-full shadow-lg">🔥 특가 -${item.discount_rate}%</div>` : '')}
                                
                                <div class="w-full h-32 bg-slate-900 overflow-hidden border-b border-slate-800/80 relative flex items-center justify-center p-2 cursor-pointer" onclick='openChartModal(${JSON.stringify(item)})'>
                                    <img src="${item.image}" class="w-full h-full object-cover rounded-xl" alt="${item.name}" onerror="this.style.display='none';">
                                    <div class="absolute top-2 left-2 z-20" onclick="event.stopPropagation();">
                                        <button onclick="toggleWishlist(${item.id})" class="bg-slate-950/80 hover:bg-slate-900 p-2 rounded-full shadow transition active:scale-95">
                                            <i class="fa-${item.is_wishlist ? 'solid text-rose-500' : 'regular text-slate-400'} fa-heart text-xs"></i>
                                        </button>
                                    </div>
                                    <div class="absolute top-2 right-2 z-20 flex gap-1" onclick="event.stopPropagation();">
                                        <button onclick="toggleBuy(${item.id})" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-[10px] font-black px-2 py-1 rounded-lg shadow transition active:scale-95" title="구매 완료 토글"><i class="fa-solid fa-check"></i> ${item.is_bought ? '취소' : '구매완료'}</button>
                                        <button onclick="manualRecord(${item.id})" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-[10px] font-black px-2 py-1 rounded-lg shadow transition active:scale-95"><i class="fa-solid fa-pen"></i> 가격</button>
                                    </div>
                                </div>
                                <div class="p-3 cursor-pointer" onclick='openChartModal(${JSON.stringify(item)})'>
                                    <h3 class="text-xs font-black text-white tracking-tight truncate">${item.name}</h3>
                                    ${item.is_deal && item.coupon_name ? `<div class="text-[10px] text-amber-300 font-bold truncate mt-0.5 bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/30"><i class="fa-solid fa-ticket"></i> ${item.coupon_name}</div>` : ''}
                                    <div class="flex justify-between items-center mt-1">
                                        <div>
                                            ${item.is_deal && item.discount_rate > 0 ? `<span class="text-[9px] text-slate-400 line-through block">${item.base_price.toLocaleString()}원</span>` : ''}
                                            <span class="text-[11px] font-mono font-bold text-cyan-400">${finalPrice.toLocaleString()}원</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="p-2 bg-slate-950/60 grid grid-cols-4 gap-1 border-t border-slate-800/60 text-center">
                                    <a href="${naverLink}" target="_blank" class="py-1 bg-[#03C75A]/15 text-[#03C75A] rounded text-[9px] font-black">네이버</a>
                                    <a href="${danawaLink}" target="_blank" class="py-1 bg-blue-500/15 text-blue-400 rounded text-[9px] font-black">다나와</a>
                                    <a href="${amazonLink}" target="_blank" class="py-1 bg-amber-500/15 text-amber-400 rounded text-[9px] font-black">아마존</a>
                                    <a href="${aliLink}" target="_blank" class="py-1 bg-rose-500/15 text-rose-400 rounded text-[9px] font-black">알리</a>
                                </div>
                            </div>
                            `;
                        }).join('')}
                    </div>
                </div>
                `;
            }).join('');
        }
        loadItems();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
