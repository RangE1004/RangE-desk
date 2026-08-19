import os
import json
import threading
import webbrowser
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Desk Setup Pro V2")

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
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(MASTER_ITEMS, f, ensure_ascii=False, indent=4)
    if not os.path.exists(RECOMMENDATIONS_FILE):
        with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(RECOMMENDATION_POOL, f, ensure_ascii=False, indent=4)

@app.on_event("startup")
async def startup_event():
    init_files()
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

@app.get("/api/items")
async def get_items():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return MASTER_ITEMS

@app.get("/api/recommendations")
async def get_recommendations(sub_group: str = Query(...)):
    if os.path.exists(RECOMMENDATIONS_FILE):
        with open(RECOMMENDATIONS_FILE, "r", encoding="utf-8") as f:
            recs = json.load(f)
    else:
        recs = RECOMMENDATION_POOL
    matched = [r for r in recs if r["sub_group"] == sub_group]
    if not matched:
        matched = recs[:3]
    return matched

@app.get("/", response_class=HTMLResponse)
async def serve_mobile_ui():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DESK SETUP PRO V2</title>
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
        
        /* 구매시기 도달 시 반짝반짝 빛나는 에메랄드 글로우 효과 */
        @keyframes purchase-glow {
            0% { border-color: #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
            50% { border-color: #34d399; box-shadow: 0 0 30px rgba(52, 211, 153, 0.9); }
            100% { border-color: #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
        }
        .purchase-glow-card { animation: purchase-glow 1.5s infinite linear; border-width: 2px !important; }

        .buy-stamp {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-15deg);
            border: 4px solid #ef4444; color: #ef4444; font-weight: 900; font-size: 2rem; padding: 4px 16px;
            letter-spacing: 2px; text-transform: uppercase; pointer-events: none; z-index: 30; opacity: 0.85;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.5); border-radius: 8px;
        }
    </style>
</head>
<body class="text-slate-100 min-h-screen pb-24 font-sans selection:bg-cyan-500/30">
    <header class="sticky top-0 z-30 bg-slate-950/90 backdrop-blur-xl border-b border-slate-800 px-5 py-4 shadow-md">
        <div class="flex justify-between items-center">
            <div>
                <h1 class="text-base font-black text-white flex items-center gap-2 tracking-widest font-mono">
                    <i class="fa-solid fa-server text-cyan-400"></i> DESK SETUP PRO V2
                </h1>
                <p class="text-[11px] text-slate-400 font-mono mt-0.5">제품 총 가격: <span id="totalAsset" class="text-cyan-400 font-bold">0원</span> | 위시 총액: <span id="wishTotal" class="text-purple-400 font-bold">0원</span></p>
            </div>
            <button onclick="openAddModal()" class="bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 text-xs font-black px-3.5 py-2 rounded-xl shadow-lg shadow-cyan-500/25 transition-all flex items-center gap-1.5 active:scale-95">
                <i class="fa-solid fa-plus text-[11px]"></i> 제품 추가
            </button>
        </div>
        <div class="mt-2.5 pt-2 border-t border-slate-800/80">
            <div class="flex justify-between text-[10px] text-slate-400 font-mono mb-1">
                <span>전역 셋업 예산 달성률 (<span id="budgetText">0원 / 1,500,000원</span>)</span>
                <span id="budgetPercent" class="text-cyan-400 font-bold">0%</span>
            </div>
            <div class="w-full bg-slate-900 h-2 rounded-full overflow-hidden border border-slate-800">
                <div id="budgetBar" class="bg-gradient-to-r from-cyan-500 to-emerald-500 h-full transition-all duration-500" style="width: 0%"></div>
            </div>
        </div>
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
    
    <!-- 제품 추가 모달 -->
    <div id="addModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-md rounded-3xl p-5 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-circle-plus text-cyan-400"></i> 새 제품 / 특가 등록</h3>
                <button onclick="closeAddModal()" class="text-slate-400 hover:text-white text-lg px-2"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <form id="addProductForm" onsubmit="submitNewProduct(event)" class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">제품명</label>
                    <input type="text" id="addName" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 로지텍 마우스">
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
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="block text-slate-400 mb-1 font-bold">현재 가격 (원)</label>
                        <input type="number" id="addPrice" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 150000">
                    </div>
                    <div>
                        <label class="block text-emerald-400 mb-1 font-bold">희망 구매가 (원)</label>
                        <input type="number" id="addTargetPrice" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 130000">
                    </div>
                </div>
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">검색 쿼리</label>
                    <input type="text" id="addQuery" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none" placeholder="예: 로지텍 마우스">
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
                    <label class="block text-amber-400 mb-1 font-bold">타임딜 마감 일시</label>
                    <input type="datetime-local" id="addExpires" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white outline-none">
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black py-3 rounded-xl shadow-lg mt-2 transition">제품 추가 완료</button>
            </form>
        </div>
    </div>

    <!-- 가격 및 희망가 동시 수정 모달 -->
    <div id="editModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-sm rounded-3xl p-5 relative border border-slate-700 shadow-2xl">
            <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-3">
                <h3 class="text-sm font-black text-white flex items-center gap-2"><i class="fa-solid fa-pen text-cyan-400"></i> 가격 변경 및 희망가 설정</h3>
                <button onclick="closeEditModal()" class="text-slate-400 hover:text-white text-lg px-2"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1 font-bold">현재 가격 변경 (원)</label>
                    <input type="number" id="editPriceInput" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none font-mono font-bold">
                </div>
                <div>
                    <label class="block text-emerald-400 mb-1 font-bold">희망 구매가 설정 (원)</label>
                    <input type="number" id="editTargetInput" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-white outline-none font-mono font-bold">
                </div>
                <div class="flex gap-2 pt-2">
                    <button onclick="saveEditedPrice()" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 flex-1 py-2.5 rounded-xl font-black text-xs transition">수정 완료</button>
                    <button onclick="closeEditModal()" class="bg-slate-700 hover:bg-slate-600 text-white flex-1 py-2.5 rounded-xl text-xs transition">취소</button>
                </div>
            </div>
        </div>
    </div>

    <!-- 상세 정보 및 AI 원터치 분석 모달 -->
    <div id="chartModal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-lg rounded-3xl p-5 relative border border-slate-700 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-3 border-b border-slate-800 pb-3">
                <h3 id="modalTitle" class="text-sm font-black text-white truncate pr-2">제품 상세 및 AI 팩트 체크 분석</h3>
                <button onclick="closeChartModal()" class="text-slate-400 hover:text-white text-lg px-2"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <div class="mb-4">
                <label class="block text-purple-400 text-[11px] font-bold mb-1.5"><i class="fa-solid fa-wand-magic-sparkles"></i> AI 팩트 기반 가격 예측 및 타이밍 분석 (누적 갱신 & 전역 1~1.4년 타임라인)</label>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="openAiSearch('Gemini')" class="bg-blue-600 hover:bg-blue-500 text-white font-black py-2.5 rounded-xl text-xs shadow transition flex items-center justify-center gap-1">
                        <i class="fa-solid fa-gem"></i> Gemini
                    </button>
                    <button onclick="openAiSearch('ChatGPT')" class="bg-emerald-600 hover:bg-emerald-500 text-white font-black py-2.5 rounded-xl text-xs shadow transition flex items-center justify-center gap-1">
                        <i class="fa-solid fa-robot"></i> ChatGPT
                    </button>
                    <button onclick="openAiSearch('Perplexity')" class="bg-purple-600 hover:bg-purple-500 text-white font-black py-2.5 rounded-xl text-xs shadow transition flex items-center justify-center gap-1">
                        <i class="fa-solid fa-compass"></i> Perplexity
                    </button>
                </div>
            </div>
            
            <div class="relative w-full h-40 bg-slate-900/80 rounded-2xl p-3 border border-slate-800 shadow-inner mb-4">
                <canvas id="priceChart"></canvas>
            </div>

            <div class="pt-3 border-t border-slate-800">
                <h4 class="text-xs font-black text-cyan-400 mb-2.5 flex items-center gap-1.5">
                    <i class="fa-solid fa-star text-amber-400"></i> 추천 제품 풀 (인기 데스크 셋업 베스트)
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
        const TOTAL_BUDGET = 1500000;

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
                    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
                }
                updateTotalsAndRender();
            } catch(e) { console.error(e); }
        }

        function saveAndRender() {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
            updateTotalsAndRender();
        }

        function updateTotalsAndRender() {
            const total = items.filter(i => i.is_main && !i.is_bought).reduce((sum, i) => sum + i.base_price, 0);
            const wishTotal = items.filter(i => i.is_wishlist).reduce((sum, i) => sum + i.base_price, 0);
            
            document.getElementById('totalAsset').textContent = total.toLocaleString() + '원';
            document.getElementById('wishTotal').textContent = wishTotal.toLocaleString() + '원';

            const percent = Math.min(Math.round((total / TOTAL_BUDGET) * 100), 100);
            document.getElementById('budgetText').textContent = `${total.toLocaleString()}원 / ${TOTAL_BUDGET.toLocaleString()}원`;
            document.getElementById('budgetPercent').textContent = `${percent}%`;
            document.getElementById('budgetBar').style.width = `${percent}%`;

            render();
        }

        function toggleWishlist(id) {
            const item = items.find(i => i.id === id);
            if(item) {
                item.is_wishlist = !item.is_wishlist;
                saveAndRender();
            }
        }

        function toggleBuy(id) {
            const item = items.find(i => i.id === id);
            if(item) {
                item.is_bought = !item.is_bought;
                saveAndRender();
            }
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
            alert('새 제품이 성공적으로 추가되었습니다!');
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
            item.last_updated = `${now.getMonth() + 1}월 ${now.getDate()}일 변동`;

            saveAndRender();
            closeEditModal();

            if(item.target_price && item.base_price <= item.target_price) {
                alert('🎉 축하합니다! 설정하신 희망 구매가 이하로 가격이 도달하여 지금이 최적의 구매시기입니다!');
            } else {
                alert('가격 및 희망 구매가와 변동 일자가 업데이트되었습니다.');
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

            localStorage.setItem(contextKey, `직전 분석가: ${currentItem.base_price}원, 목표가: ${currentItem.target_price || 0}원 반영됨.`);

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
                    <div class="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 flex justify-between items-center">
                        <div class="flex items-center gap-2.5 truncate pr-2">
                            <img src="${rec.image}" class="w-8 h-8 object-cover rounded-lg shrink-0 border border-slate-700/60" onerror="this.style.display='none';">
                            <span class="text-xs font-bold text-slate-200 truncate">${rec.name}</span>
                        </div>
                        <span class="text-xs font-mono font-black text-cyan-400 shrink-0">${rec.base_price.toLocaleString()}원</span>
                    </div>
                `).join('');
            } else {
                recContainer.innerHTML = '<div class="text-[11px] text-slate-500 text-center py-2">추천 제품이 없습니다.</div>';
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
                <div class="glass-card rounded-2xl p-4 border border-amber-500/30 mb-4 bg-amber-950/20">
                    <h3 class="text-xs font-black text-amber-400 mb-2.5 flex items-center gap-1.5">
                        <i class="fa-solid fa-calendar-days"></i> 글로벌 대형 세일 예상 D-Day 캘린더
                    </h3>
                    <div class="grid grid-cols-2 gap-2">
                        ${salesEvents.map(ev => {
                            const diffDays = Math.ceil((ev.date - now) / (1000 * 60 * 60 * 24));
                            return `
                                <div class="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 flex justify-between items-center">
                                    <span class="text-[11px] font-bold text-slate-300 truncate pr-1">${ev.name}</span>
                                    <span class="text-xs font-mono font-black text-amber-400 shrink-0">${diffDays > 0 ? `D-${diffDays}` : '진행중/종료'}</span>
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
                listEl.innerHTML = salesBannerHTML + '<div class="text-center text-slate-500 py-16 text-xs">등록된 제품이 없습니다.</div>';
                return;
            }

            const nowTime = new Date().getTime();
            const itemsHTML = groups.map(g => {
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

                            // 구매시기 도달 여부 판별 (현재가 <= 희망구매가)
                            const isPurchaseTime = item.target_price && item.base_price <= item.target_price;

                            let isUrgent = false;
                            if(item.is_deal && item.expires_at) {
                                const expTime = new Date(item.expires_at).getTime();
                                const diffHours = (expTime - nowTime) / (1000 * 60 * 60);
                                if(diffHours > 0 && diffHours <= 12) { isUrgent = true; }
                            }

                            // 카드 전체 빛나는 효과 (purchase-glow-card) 적용
                            let cardClass = "glass-card rounded-2xl overflow-hidden flex flex-col justify-between relative border border-slate-800";
                            if(isUrgent) { 
                                cardClass = "glass-card rounded-2xl overflow-hidden urgent-border flex flex-col justify-between relative"; 
                            } else if(isPurchaseTime) {
                                cardClass = "glass-card rounded-2xl overflow-hidden purchase-glow-card flex flex-col justify-between relative";
                            }
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
                                        <button onclick="toggleBuy(${item.id})" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-[10px] font-black px-2 py-1 rounded-lg shadow transition active:scale-95"><i class="fa-solid fa-check"></i> ${item.is_bought ? '취소' : '구매완료'}</button>
                                        <button onclick="manualRecord(${item.id})" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-[10px] font-black px-2 py-1 rounded-lg shadow transition active:scale-95"><i class="fa-solid fa-pen"></i> 가격 변경</button>
                                    </div>
                                </div>
                                <div class="p-3 cursor-pointer" onclick='openChartModal(${JSON.stringify(item)})'>
                                    <h3 class="text-xs font-black text-white tracking-tight truncate">${item.name}</h3>
                                    
                                    <!-- 버튼들과 겹치지 않는 본문 영역에 배치된 구매시기 알람 배너 -->
                                    ${isPurchaseTime ? '<div class="my-1 bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 text-[9px] font-black px-2 py-1 rounded-lg flex items-center gap-1 shadow animate-pulse"><i class="fa-solid fa-bullseye"></i> 🎯 [구매시기 도달!] 지금 사기 좋은 때</div>' : ''}

                                    ${item.target_price ? `<div class="text-[10px] text-emerald-400 font-mono mt-0.5">희망 구매가: ${item.target_price.toLocaleString()}원</div>` : ''}
                                    <div class="text-[9px] text-slate-400 font-mono mt-0.5">최근 변동: ${item.last_updated || '정보 없음'}</div>
                                    ${item.is_deal && item.coupon_name ? `<div class="text-[10px] text-amber-300 font-bold truncate mt-0.5 bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/30"><i class="fa-solid fa-ticket"></i> ${item.coupon_name}</div>` : ''}
                                    <div class="flex justify-between items-center mt-1">
                                        <div>
                                            ${item.is_deal && item.discount_rate > 0 ? `<span class="text-[9px] text-slate-400 line-through block">${item.base_price.toLocaleString()}원</span>` : ''}
                                            <span class="text-[11px] font-mono font-bold text-cyan-400">${finalPrice.toLocaleString()}원</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="p-2 bg-slate-950/80 grid grid-cols-2 gap-1.5 border-t border-slate-800 text-center">
                                    <a href="${naverLink}" target="_blank" class="py-1.5 bg-[#03C75A]/20 hover:bg-[#03C75A]/30 text-[#03C75A] rounded-lg text-[10px] font-black flex items-center justify-center gap-1 transition">
                                        <i class="fa-solid fa-n"></i> 네이버
                                    </a>
                                    <a href="${danawaLink}" target="_blank" class="py-1.5 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg text-[10px] font-black flex items-center justify-center gap-1 transition">
                                        <i class="fa-solid fa-d"></i> 다나와
                                    </a>
                                    <a href="${amazonLink}" target="_blank" class="py-1.5 bg-amber-500/20 hover:bg-amber-500/30 text-amber-400 rounded-lg text-[10px] font-black flex items-center justify-center gap-1 transition">
                                        <i class="fa-brands fa-amazon"></i> 아마존
                                    </a>
                                    <a href="${aliLink}" target="_blank" class="py-1.5 bg-rose-500/20 hover:bg-rose-500/30 text-rose-400 rounded-lg text-[10px] font-black flex items-center justify-center gap-1 transition">
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
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
