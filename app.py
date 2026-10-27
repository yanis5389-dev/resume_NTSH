from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 多國語言字典 (以中文為 Key，存放各國語言對應)
ZH_DICT = {
    "你好": {"ko": "안녕하세요", "ja": "こんにちは", "en": "Hello"},
    "謝謝": {"ko": "감사합니다", "ja": "ありがとう", "en": "Thank you"},
    "對不起": {"ko": "죄송합니다", "ja": "ごめんなさい", "en": "Sorry"},
    "早安": {"ko": "좋은 아침", "ja": "おはようございます", "en": "Good morning"},
    "晚安": {"ko": "안녕히 주무세요", "ja": "おやすみなさい", "en": "Good night"},
    "老師": {"ko": "선생님", "ja": "先生", "en": "Teacher"},
    "學生": {"ko": "학생", "ja": "学生", "en": "Student"},
    "朋友": {"ko": "친구", "ja": "友達", "en": "Friend"},
    "家人": {"ko": "가족", "ja": "家族", "en": "Family"},
    "愛": {"ko": "사랑", "ja": "愛", "en": "Love"},
}


# 首頁
@app.route("/")
def index():
    return render_template("index.html")


# 競賽
@app.route("/competition")
def competition():
    return render_template("competition.html")


# 多國語言字典查詢
@app.route("/ask", methods=["GET", "POST"])
def ask():
    question = ""
    answer = ""
    selected_lang = "ko"  # 預設選擇韓文

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        selected_lang = request.form.get("lang", "ko")  # 取得使用者選擇的目標語言

        # 查表邏輯
        word_data = ZH_DICT.get(question)
        if word_data and selected_lang in word_data:
            answer = word_data[selected_lang]
        else:
            answer = "抱歉，我目前沒有這個詞的對應翻譯。"

    return render_template(
        "ask.html",
        question=question,
        answer=answer,
        selected_lang=selected_lang,
    )


# 課外活動
@app.route("/activities", methods=["GET", "POST"])
def activities():
    question = ""
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = "目前課外活動查詢模組尚未開放。"

    return render_template(
        "activities.html", question=question, answer=answer
    )


# 股票查詢
@app.route("/stock", methods=["GET", "POST"])
def stock():
    question = ""
    answer = ""

    if request.method == "POST":
        stock_no = request.form.get("question", "").strip()
        question = stock_no

        if not stock_no:
            answer = "請輸入股票代號"
        else:
            url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={stock_no}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            try:
                res = requests.get(url, headers=headers, timeout=10)
                data = res.json()

                if data.get("stat") == "OK" and data.get("data"):
                    last_trade = data["data"][-1]
                    date_str = last_trade[0]
                    closing_price = last_trade[6]
                    answer = f"最新收盤價 ({date_str})：${closing_price}"
                else:
                    answer = "查無資料，請確認股票代號"

            except Exception as e:
                print(f"股票查詢錯誤: {e}")
                answer = "查詢失敗"

    return render_template("stock.html", question=question, answer=answer)


# 其他靜態頁面
@app.route("/leadership")
def leadership():
    return render_template("leadership.html")


@app.route("/club")
def club():
    return render_template("club.html")


@app.route("/electives")
def electives():
    return render_template("electives.html")


@app.route("/ai")
def ai():
    return render_template("ai.html")


@app.route("/baseball")
def baseball():
    return render_template("baseball.html")


if __name__ == "__main__":
    app.run(debug=True)
