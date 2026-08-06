import base64
from flask import Flask, render_template, request
from selenium_logic import search_company

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        company = request.form["company"]
        company_decoration = request.form["company_decoration"]

        company_color = request.form["company_color"]

        color1 = request.form["color1"]
        color2 = request.form["color2"]
        color3 = request.form["color3"]
        color4 = request.form["color4"]
        colors = [color1, color2, color3, color4]

        footer_color = request.form["footer_color"]

        # ★ 로고 이미지 파일 읽기 및 Base64 인코딩
        company_logo_b64 = None
        if "company_logo" in request.files:
            file = request.files["company_logo"]
            if file and file.filename != "":
                company_logo_b64 = base64.b64encode(file.read()).decode("utf-8")

        # search_company 함수에 이미지 Base64 데이터 추가 전달
        results = search_company(
            company,
            company_decoration,
            company_color,
            colors,
            footer_color,
            company_logo_b64,
        )

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)