from flask import Flask, request, render_template
import requests

app = Flask(__name__)


# 建立題庫
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


# 首頁
@app.route('/')
def index():
    return render_template('index.html')


# 競賽
@app.route('/competition')
def competition():
    return render_template('competition.html')


# 中韓字典
@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        question1 = request.form.get('question', '').strip()

        answer1 = zh_ko_dict.get(
            question1,
            "抱歉，我目前沒有這個詞的韓文對應。"
        )

        return render_template(
            'ask.html',
            question=question1,
            answer=answer1
        )

    return render_template(
        'ask.html',
        question="",
        answer=""
    )


# 課外活動
@app.route('/activities', methods=['GET', 'POST'])
def activities():

    if request.method == 'POST':

        question = request.form.get('question', '').strip()

        answer1 = "抱歉，我目前沒有這個詞的韓文對應。"

        return render_template(
            'activities.html',
            question=question,
            answer=answer1
        )

    return render_template(
        'activities.html',
        question="",
        answer=""
    )


# 股票查詢
@app.route('/stock', methods=['GET', 'POST'])
def stock():

    if request.method == 'POST':

        # 取得股票代號
        stock_no = request.form.get('question', '').strip()

        # 股票代號沒輸入
        if stock_no == "":
            return render_template(
                'stock.html',
                question="",
                answer="請輸入股票代號"
            )

        # 台灣證券交易所 API
        url = (
            "https://www.twse.com.tw/exchangeReport/"
            "STOCK_DAY"
            f"?response=json&stockNo={stock_no}"
        )

        try:

            # 發送請求
            res = requests.get(url, timeout=10)

            # 轉成 JSON
            data = res.json()

            # 判斷是否成功
            if data.get("stat") == "OK" and data.get("data"):

                # 最後一筆資料
                last_data = data["data"][-1]

                # 收盤價的位置是第 7 欄，index = 6
                answer = last_data[6]

            else:

                answer = "查無資料，請確認股票代號"

        except Exception as e:

            print("發生錯誤：", e)

            answer = "查詢失敗"

        return render_template(
            'stock.html',
            question=stock_no,
            answer=answer
        )

    return render_template(
        'stock.html',
        question="",
        answer=""
    )


# 幹部經驗
@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# 社團經驗
@app.route('/club')
def club():
    return render_template('club.html')


# 多元選修
@app.route('/electives')
def electives():
    return render_template('electives.html')


# AI 應用
@app.route('/ai')
def ai():
    return render_template('ai.html')


# ★ 棒球頁面
@app.route('/baseball')
def baseball():
    return render_template('baseball.html')


# 啟動 Flask
if __name__ == '__main__':
    app.run(debug=True)
