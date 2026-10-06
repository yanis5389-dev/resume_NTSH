```python
from flask import Flask, request, render_template
import requests

app = Flask(__name__)


# ==============================
# 中韓翻譯題庫
# ==============================

zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}


# ==============================
# 首頁
# ==============================

@app.route('/')
def index():
    return render_template('index.html')


# ==============================
# 競賽經驗
# ==============================

@app.route('/competition')
def competition():
    return render_template('competition.html')


# ==============================
# 課外活動
# ==============================

@app.route('/activities', methods=['GET', 'POST'])
def activities():

    if request.method == 'POST':

        # 讀取學生輸入的問題
        question = request.form.get('question', '').strip()

        # 目前先顯示固定回答
        answer = "抱歉，我目前沒有這個問題的答案。"

        return render_template(
            'activities.html',
            question=question,
            answer=answer
        )

    # GET 時
    return render_template(
        'activities.html',
        question="",
        answer=""
    )


# ==============================
# 中韓字典
# ==============================

@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        # 取得使用者輸入
        question1 = request.form.get('question', '').strip()

        # 查詢字典
        # 使用 get 可以避免輸入不存在的單字時程式直接報錯
        answer1 = zh_ko_dict.get(
            question1,
            "抱歉，我目前沒有這個詞的韓文對應。"
        )

        # 回傳結果
        return render_template(
            'ask.html',
            question=question1,
            answer=answer1
        )

    # GET 時
    return render_template(
        'ask.html',
        question="",
        answer=""
    )


# ==============================
# 股票查詢
# ==============================

@app.route('/stock', methods=['GET', 'POST'])
def stock():

    if request.method == 'POST':

        # 取得使用者輸入的股票代號
        stock_no = request.form.get('question', '').strip()

        # 台灣證券交易所 API
        url = (
            "https://www.twse.com.tw/exchangeReport/"
            f"STOCK_DAY?response=json&stockNo={stock_no}"
        )

        try:

            # 發送 API 請求
            res = requests.get(url, timeout=10)

            # 將回應轉成 JSON
            data = res.json()

            # 判斷 API 是否成功
            if data.get("stat") == "OK" and data.get("data"):

                # 最後一天的收盤價
                answer = data["data"][-1][6]

            else:

                answer = "查無資料，請確認股票代號是否正確。"

        except Exception as e:

            print("股票 API 錯誤：", e)

            answer = "股票資料查詢失敗，請稍後再試。"

        # 回傳結果
        return render_template(
            'stock.html',
            question=stock_no,
            answer=answer
        )

    # GET 時
    return render_template(
        'stock.html',
        question="",
        answer=""
    )


# ==============================
# 幹部經驗
# ==============================

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# ==============================
# 社團經驗
# ==============================

@app.route('/club')
def club():
    return render_template('club.html')


# ==============================
# 多元選修
# ==============================

@app.route('/electives')
def electives():
    return render_template('electives.html')


# ==============================
# AI 應用
# ==============================

@app.route('/ai')
def ai():
    return render_template('ai.html')


# ==============================
# 棒球
# ==============================

@app.route('/baseball')
def baseball():
    return render_template('baseball.html')


# ==============================
# 啟動 Flask
# ==============================

if __name__ == '__main__':
    app.run(debug=True)
```
