from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# 70만 단어 로드
with open("clean_words.txt", "r", encoding="utf-8") as f:
    WORDS = [line.strip().lower() for line in f if line.strip()]

@app.get("/api/search")
def search(start: str = "", end: str = "", sort: str = "len_desc", limit: int = 500):
    start = start.strip().lower()
    end = end.strip().lower()
    
    results = [
        w for w in WORDS
        if (not start or w.startswith(start)) and (not end or w.endswith(end))
    ]
    
    if sort == "len_desc":
        results.sort(key=lambda x: len(x), reverse=True)
    elif sort == "len_asc":
        results.sort(key=lambda x: len(x))
    elif sort == "az":
        results.sort()
    elif sort == "za":
        results.sort(reverse=True)
        
    return {"count": len(results), "words": results[:limit]}

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Last Letter Library (Offline Pro Edition)</title>
        <style>
            :root {
                --bg: #f4ede2;
                --panel: #fcf9f5;
                --border: #dfd7cc;
                --primary: #8b2635;
                --primary-hover: #701c28;
                --tag-bg: #ffffff;
                --text: #3d352e;
                --text-muted: #8c827a;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 24px 16px;
                display: flex;
                justify-content: center;
            }
            .wrapper {
                width: 100%;
                max-width: 1080px;
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            }
            header {
                text-align: center;
                margin-bottom: 24px;
            }
            h1 {
                font-size: 28px;
                color: var(--primary);
                margin: 0 0 8px 0;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .tagline {
                font-style: italic;
                color: var(--text-muted);
                font-size: 14px;
                margin: 0;
            }
            .nav-tabs {
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-top: 18px;
            }
            .nav-btn {
                background: none;
                border: 1px solid var(--border);
                padding: 8px 18px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
                color: var(--text);
                cursor: pointer;
            }
            .nav-btn.active {
                background: var(--primary);
                color: #fff;
                border-color: var(--primary);
            }
            /* 정렬 바 */
            .sort-bar {
                display: flex;
                gap: 8px;
                align-items: center;
                margin: 20px 0 12px 0;
                font-size: 13px;
                color: var(--text-muted);
            }
            .sort-chip {
                background: #fff;
                border: 1px solid var(--border);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
            }
            .sort-chip.active {
                background: #e8ded2;
                border-color: #baa996;
            }
            /* 검색 입력창 */
            .search-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 14px;
                margin-bottom: 14px;
            }
            .input-group label {
                display: block;
                font-size: 12px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 6px;
            }
            input {
                width: 100%;
                box-sizing: border-box;
                background: #fff;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 12px 14px;
                font-size: 16px;
                outline: none;
            }
            input:focus {
                border-color: var(--primary);
            }
            /* 검색 버튼 (0초 즉시 실행) */
            .action-btn {
                width: 100%;
                background: var(--primary);
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 16px;
                font-weight: 700;
                cursor: pointer;
                transition: background 0.15s;
            }
            .action-btn:hover {
                background: var(--primary-hover);
            }
            /* 트랩 퀵 솔루션 버튼들 */
            .trap-section {
                margin: 18px 0;
                background: #f4ede2;
                border-radius: 8px;
                padding: 12px 16px;
            }
            .trap-title {
                font-size: 12px;
                font-weight: 700;
                color: var(--primary);
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            .trap-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }
            .trap-btn {
                background: #fff;
                border: 1px solid #d4c7b8;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: 700;
                color: #55483d;
                cursor: pointer;
            }
            .trap-btn:hover {
                background: var(--primary);
                color: #fff;
            }
            /* 결과 창 */
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 20px 0 12px 0;
                font-size: 14px;
                font-weight: 600;
                color: var(--text-muted);
            }
            .results-box {
                background: #eee6d8;
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 16px;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                max-height: 480px;
                overflow-y: auto;
            }
            .word-card {
                background: var(--tag-bg);
                border: 1px solid #dcd4c7;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 14px;
                font-weight: 700;
                color: #332d27;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                user-select: text;
            }
            .word-len {
                font-size: 11px;
                color: var(--text-muted);
                margin-left: 6px;
                font-weight: 500;
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <header>
                <h1>Last Letter Library</h1>
                <p class="tagline">"If you have a big enough dictionary, just about everything is a word."</p>
                <div class="nav-tabs">
                    <button class="nav-btn active">Custom Search</button>
                    <button class="nav-btn">700k Lexicon</button>
                    <button class="nav-btn" style="color: #27ae60;">⚡ Zero Cooldown</button>
                </div>
            </header>

            <div class="sort-bar">
                <span>Sort:</span>
                <button class="sort-chip active" id="btnLenDesc" onclick="setSort('len_desc')">Length ↓</button>
                <button class="sort-chip" id="btnLenAsc" onclick="setSort('len_asc')">Length ↑</button>
                <button class="sort-chip" id="btnAZ" onclick="setSort('az')">A-Z ↑</button>
            </div>

            <div class="search-grid">
                <div class="input-group">
                    <label>Starts With</label>
                    <input id="startInput" placeholder="e.g. nona, d, nk" onkeyup="if(event.key==='Enter')doSearch()" />
                </div>
                <div class="input-group">
                    <label>Ends With</label>
                    <input id="endInput" placeholder="e.g. s, tion, dae" onkeyup="if(event.key==='Enter')doSearch()" />
                </div>
            </div>

            <button class="action-btn" onclick="doSearch()">Instant Search</button>

            <!-- 캡처 화면 속 트랩 솔루션 퀵버튼들 -->
            <div class="trap-section">
                <div class="trap-title">🔥 Trap Solves Quick Finder</div>
                <div class="trap-tags">
                    <button class="trap-btn" onclick="quickTrap('nk')">NK-</button>
                    <button class="trap-btn" onclick="quickTrap('rk')">RK-</button>
                    <button class="trap-btn" onclick="quickTrap('dz')">DZ-</button>
                    <button class="trap-btn" onclick="quickTrap('fs')">FS-</button>
                    <button class="trap-btn" onclick="quickTrap('bk')">BK-</button>
                    <button class="trap-btn" onclick="quickTrap('hl')">HL-</button>
                    <button class="trap-btn" onclick="quickTrap('pf')">PF-</button>
                    <button class="trap-btn" onclick="quickTrap('yc')">YC-</button>
                    <button class="trap-btn" onclick="quickTrap('yp')">YP-</button>
                    <button class="trap-btn" onclick="quickTrap('yg')">YG-</button>
                    <button class="trap-btn" onclick="quickTrap('cw')">CW-</button>
                    <button class="trap-btn" onclick="quickTrap('bt')">BT-</button>
                    <button class="trap-btn" onclick="quickTrap('dh')">DH-</button>
                    <button class="trap-btn" onclick="quickTrap('mb')">MB-</button>
                    <button class="trap-btn" onclick="quickTrap('kw')">KW-</button>
                    <button class="trap-btn" onclick="quickTrap('sz')">SZ-</button>
                    <button class="trap-btn" onclick="quickTrap('fd')">FD-</button>
                </div>
            </div>

            <div class="result-header">
                <span id="foundCount">Words: 0 found</span>
                <span id="elapsedTime" style="font-weight: normal; font-size: 12px;"></span>
            </div>

            <div id="resultsBox" class="results-box">
                <div style="color: var(--text-muted); font-size: 14px; width: 100%; text-align: center; padding: 30px;">
                    Enter prefix/suffix above or click a trap button to search instantly.
                </div>
            </div>
        </div>

        <script>
            let currentSort = "len_desc";

            function setSort(s) {
                currentSort = s;
                document.querySelectorAll('.sort-chip').forEach(b => b.classList.remove('active'));
                if (s === 'len_desc') document.getElementById('btnLenDesc').classList.add('active');
                if (s === 'len_asc') document.getElementById('btnLenAsc').classList.add('active');
                if (s === 'az') document.getElementById('btnAZ').classList.add('active');
                doSearch();
            }

            function quickTrap(prefix) {
                document.getElementById('startInput').value = prefix;
                document.getElementById('endInput').value = '';
                doSearch();
            }

            async function doSearch() {
                const s = document.getElementById('startInput').value.trim();
                const e = document.getElementById('endInput').value.trim();
                const countEl = document.getElementById('foundCount');
                const timeEl = document.getElementById('elapsedTime');
                const box = document.getElementById('resultsBox');

                countEl.innerText = "Searching...";
                const t0 = performance.now();

                const res = await fetch(`/api/search?start=${encodeURIComponent(s)}&end=${encodeURIComponent(e)}&sort=${currentSort}&limit=500`);
                const data = await res.json();
                const ms = (performance.now() - t0).toFixed(1);

                countEl.innerText = `Words starting with ${s || 'ALL'}: ${data.count.toLocaleString()} found`;
                timeEl.innerText = `(${ms}ms · showing top ${data.words.length})`;

                if (data.words.length === 0) {
                    box.innerHTML = `<div style="color: #999; text-align: center; width: 100%; padding: 30px;">No matching words found.</div>`;
                    return;
                }

                box.innerHTML = data.words.map(w => `
                    <div class="word-card">
                        <span>${w}</span>
                        <span class="word-len">${w.length}</span>
                    </div>
                `).join('');
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)